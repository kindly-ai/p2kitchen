from datetime import timedelta

from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from django.utils.timesince import timesince
from django_extensions.db.models import TimeStampedModel
import uuid


class SensorName(models.TextChoices):
    SWITCH = "power-switch", "Power switched"
    METER_HAS_CHANGED = "power-meter-has-changed", "Power meter changed"
    METER = "power-meter", "Power metered"


class SensorEvent(TimeStampedModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=254, choices=SensorName.choices)
    value = models.CharField(max_length=254)
    id = models.CharField(max_length=254)
    machine = models.ForeignKey("p2coffee.Machine", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.uuid)

    class Meta:
        verbose_name = "Sensor event"
        verbose_name_plural = "Sensor events"
        index_together = ["created", "modified"]
        ordering = ["created"]


class CoffeePotEventType(models.TextChoices):
    BREWING_STARTED = "brew_started", "I started brewing"
    BREWING_FINISHED = "brew_finished", "I'm done brewing"


class CoffeePotEvent(TimeStampedModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = models.CharField(max_length=254, choices=CoffeePotEventType.choices)
    machine = models.ForeignKey("p2coffee.Machine", on_delete=models.SET_NULL, blank=True, null=True)

    slack_channel = models.CharField(max_length=64, null=True, blank=True)
    slack_ts = models.CharField(max_length=64, null=True, blank=True)

    def as_text(self):
        return self.as_slack_text()

    def as_slack_text(self):
        return "{} {}{}".format(self.__str__(), naturaltime(self.created), self._get_duration())

    def _get_duration(self):
        duration = ""

        if self.type == CoffeePotEventType.BREWING_STARTED.value:
            brew_time = timedelta(minutes=settings.BREWTIME_AVG_MINUTES)
            expected_brewtime = naturaltime(self.created + brew_time)
            duration = f" and should be done {expected_brewtime}"

        elif self.type == CoffeePotEventType.BREWING_FINISHED.value:
            events_started = CoffeePotEvent.objects.filter(type=CoffeePotEventType.BREWING_STARTED.value)
            last_started_event = events_started.exclude(uuid=self.uuid).last()

            if last_started_event:
                actual_brew_time = timesince(last_started_event.created, self.created)
                duration = f", took only {actual_brew_time}"

        return duration

    def __str__(self):
        return self.get_type_display()

    class Meta:
        verbose_name = "Coffee pot event"
        verbose_name_plural = "Coffee pot events"
        index_together = ["created", "modified"]
        ordering = ["created"]


class Brew(TimeStampedModel):
    started_event = models.ForeignKey(CoffeePotEvent, on_delete=models.CASCADE, related_name="brews_started")
    finished_event = models.ForeignKey(CoffeePotEvent, on_delete=models.CASCADE, related_name="brews_finished")
    machine = models.ForeignKey("p2coffee.Machine", on_delete=models.CASCADE, related_name="brews")
    brewer_slack_username = models.CharField(max_length=255, blank=True, default="")


class BrewReaction(TimeStampedModel):
    brew = models.ForeignKey(Brew, on_delete=models.CASCADE, related_name="reactions")
    reaction = models.CharField(max_length=255)
    is_custom_reaction = models.BooleanField(default=False, blank=True)
    slack_username = models.CharField(max_length=255)


class MachineStatus(models.TextChoices):
    BREWING = "brewing", "Brewing"
    IDLE = "idle", "Idle"


class Machine(TimeStampedModel):
    name = models.CharField(max_length=255)
    device_name = models.CharField(max_length=255)
    volume = models.DecimalField(max_digits=4, decimal_places=2, default=1.25, blank=True)
    status = models.CharField(choices=MachineStatus.choices, max_length=7, default=MachineStatus.IDLE.value)

    def __str__(self):
        return self.name
