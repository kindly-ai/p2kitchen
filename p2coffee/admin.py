from django.contrib import admin
from django.templatetags.tz import localtime
from django.utils.formats import date_format

from p2coffee.models import SensorEvent, CoffeePotEvent, Brew, BrewReaction, Machine


def format_datetime(dt, dt_format="Y-m-d H:i:s"):
    return date_format(localtime(dt), dt_format)


class CreatedPreciseMixin:
    def created_precise(self, obj):
        return format_datetime(obj.created)

    created_precise.admin_order_field = "created"
    created_precise.short_description = "Created"


class CoffeePotEventAdmin(admin.ModelAdmin, CreatedPreciseMixin):
    list_display = ["type", "created_precise"]
    list_filter = ["type", "created"]
    readonly_fields = ["uuid", "created"]
    ordering = ["-created"]


class SensorEventAdmin(admin.ModelAdmin, CreatedPreciseMixin):
    list_display = ["uuid", "name", "id", "value", "created_precise"]
    list_filter = ["name", "id", "created"]
    readonly_fields = ["uuid", "created"]
    fields = ["name", "id", "value", "uuid", "created"]
    ordering = ["-created"]


class MachineAdmin(admin.ModelAdmin):
    list_display = ["name", "device_name", "status"]
    list_filter = ["status"]


class BrewAdmin(admin.ModelAdmin, CreatedPreciseMixin):
    list_display = ["id", "started_event", "finished_event", "status", "brewer_slack_username", "created_precise"]
    list_filter = ["status", "created", "brewer_slack_username"]
    search_fields = ["brewer_slack_username"]
    ordering = ["-created"]


class BrewReactAdmin(admin.ModelAdmin, CreatedPreciseMixin):
    list_display = ["reaction", "slack_username", "created_precise"]
    list_filter = ["created", "slack_username"]
    search_fields = ["reaction", "slack_username"]
    ordering = ["-created"]


admin.site.register(CoffeePotEvent, CoffeePotEventAdmin)
admin.site.register(SensorEvent, SensorEventAdmin)

admin.site.register(Machine, MachineAdmin)
admin.site.register(Brew, BrewAdmin)
admin.site.register(BrewReaction, BrewReactAdmin)
