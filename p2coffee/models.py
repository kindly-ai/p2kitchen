from datetime import timedelta, datetime

from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from django.templatetags.static import static
from django.utils import timezone
from django.utils.timesince import timesince
from django_extensions.db.models import TimeStampedModel
import uuid

from p2coffee.emojis import EMOJI_MAP
from p2coffee.slack_messages import brew_started_message, brew_update_message, brew_finished_message


class SensorEvent(TimeStampedModel):
    class Name(models.TextChoices):
        SWITCH = "power-switch", "Power switched"
        METER_HAS_CHANGED = "power-meter-has-changed", "Power meter changed"
        METER = "power-meter", "Power metered"

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=254, choices=Name.choices)
    value = models.CharField(max_length=254)
    id = models.CharField(max_length=254, help_text="Device ID")
    machine = models.ForeignKey("p2coffee.Machine", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.uuid)

    class Meta:
        verbose_name = "Sensor event"
        verbose_name_plural = "Sensor events"
        index_together = ["created", "modified"]
        ordering = ["created"]


# FIXME: Migrate existing CoffeePotEvents to Brews
class CoffeePotEvent(TimeStampedModel):
    class EventType(models.TextChoices):
        BREWING_STARTED = "brew_started", "I started brewing"
        BREWING_FINISHED = "brew_finished", "I'm done brewing"

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = models.CharField(max_length=254, choices=EventType.choices)
    machine = models.ForeignKey("p2coffee.Machine", on_delete=models.SET_NULL, blank=True, null=True)

    slack_channel = models.CharField(max_length=64, null=True, blank=True)
    slack_ts = models.CharField(max_length=64, null=True, blank=True)

    def as_text(self):
        return self.as_slack_text()

    def as_slack_text(self):
        return "{} {}{}".format(self.__str__(), naturaltime(self.created), self._get_duration())

    def _get_duration(self):
        duration = ""

        if self.type == CoffeePotEvent.EventType.BREWING_STARTED.value:
            brew_time = timedelta(minutes=settings.BREWTIME_AVG_MINUTES)
            expected_brewtime = naturaltime(self.created + brew_time)
            duration = f" and should be done {expected_brewtime}"

        elif self.type == CoffeePotEvent.EventType.BREWING_FINISHED.value:
            events_started = CoffeePotEvent.objects.filter(type=CoffeePotEvent.EventType.BREWING_STARTED.value)
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


class SlackProfile(TimeStampedModel):
    user_id = models.CharField(max_length=255, primary_key=True)
    display_name = models.CharField(max_length=255, blank=True, default="")
    real_name = models.CharField(max_length=255, blank=True, default="")
    image_original = models.CharField(max_length=255, blank=True, default="")

    def image(self, size=48):
        if size not in [24, 32, 48, 72, 192, 512, 1024]:
            raise ValueError("Invalid image size")
        return self.image_original.replace("_original", f"_{size}")

    def sync_profile(self, save=True):
        sync_fields = ["display_name", "real_name", "image_original"]
        from p2coffee.slack import users_profile_get

        profile = users_profile_get(self.user_id)
        for field_name in sync_fields:
            value = getattr(profile["profile"], field_name, "")
            setattr(self, field_name, value)

        if save:
            self.save()

    def __str__(self):
        return self.user_id


def _day_range_tuple(dt=None) -> (datetime, datetime):
    if dt is None:
        dt = timezone.now()
    return dt.replace(hour=0, minute=0, second=0), dt.replace(hour=23, minute=59, second=59)


class BrewManager(models.Manager):
    def today(self):
        today_start, today_end = _day_range_tuple()
        return self.filter(finished_event__created__gte=today_start, finished_event__created__lte=today_end)

    def yesterday(self):
        today_start, today_end = _day_range_tuple(timezone.now() - timedelta(days=1))
        return self.filter(finished_event__created__gte=today_start, finished_event__created__lte=today_end)


class Brew(TimeStampedModel):
    class Status(models.TextChoices):
        BREWING = "brewing", "Brewing"
        FINISHED = "finished", "Finished"

    started_event = models.ForeignKey(SensorEvent, on_delete=models.CASCADE, related_name="brews_started")
    finished_event = models.ForeignKey(
        SensorEvent, on_delete=models.CASCADE, related_name="brews_finished", blank=True, null=True
    )
    status = models.CharField(choices=Status.choices, max_length=8, default=Status.BREWING.value)
    machine = models.ForeignKey("p2coffee.Machine", on_delete=models.CASCADE, related_name="brews")

    brewer = models.ForeignKey(SlackProfile, on_delete=models.SET_NULL, blank=True, null=True)

    slack_channel = models.CharField(max_length=64, null=True, blank=True)
    slack_ts = models.CharField(max_length=64, null=True, blank=True)

    objects = BrewManager()

    def __str__(self):
        return self.get_status_display()

    @property
    def progress(self):
        if self.finished_event:
            return 100

        seconds_elapsed = (timezone.now() - self.started_event.created).seconds
        avg_brewtime = settings.BREWTIME_AVG_SECONDS

        if seconds_elapsed > avg_brewtime:
            return 100

        return int(100 * (seconds_elapsed / avg_brewtime))

    def started_message(self):
        return brew_started_message(self)

    def update_message(self):
        return brew_update_message(self)

    def finished_message(self):
        return brew_finished_message(self)


class BrewReaction(TimeStampedModel):
    brew = models.ForeignKey(Brew, on_delete=models.CASCADE, related_name="reactions")
    reaction = models.CharField(max_length=255)
    is_custom_reaction = models.BooleanField(default=False, blank=True)
    user = models.ForeignKey(SlackProfile, on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def emoji(self):
        return EMOJI_MAP.get(self.reaction, self.reaction)

    def __str__(self):
        return self.reaction


class Machine(TimeStampedModel):
    class Status(models.TextChoices):
        BREWING = "brewing", "Brewing"
        IDLE = "idle", "Idle"

    name = models.CharField(max_length=255)
    device_name = models.CharField(max_length=255, unique=True)
    volume = models.DecimalField(max_digits=4, decimal_places=2, default=1.25, blank=True)
    status = models.CharField(choices=Status.choices, max_length=7, default=Status.IDLE.value)
    avatar_path = models.CharField(max_length=500, blank=True, default="")

    @property
    def avatar_url(self):
        return static(self.avatar_path) if self.avatar_path else ""

    def __str__(self):
        return self.name
