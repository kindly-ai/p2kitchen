from argparse import ArgumentParser
from datetime import timedelta

from django.core.management import BaseCommand

from p2kitchen.models import Brew, CoffeePotEvent, Machine, SensorEvent


def migrate(dry_run):
    events = CoffeePotEvent.objects.all()
    brew_data_list = []
    last_brew_data = None
    for event in events:
        brew_data = {}
        # Find SensorEvent triggering CoffeePotEvent
        one_second = timedelta(seconds=1)
        try:
            sensor_event = SensorEvent.objects.get(
                name=SensorEvent.Name.METER_HAS_CHANGED,
                created__gte=event.created - one_second,
                created__lte=event.created + one_second,
            )
        except SensorEvent.DoesNotExist:
            ts = event.created.isoformat()
            print(f"FIXME: [{event.uuid}] No SensorEvent for same second (+/-1s) created={ts}")
            continue
        except SensorEvent.MultipleObjectsReturned:
            ts = event.created.isoformat()
            print(f"FIXME: [{event.uuid}] Multiple SensorEvents for same second (+/-1s) created={ts}")
            continue

        if event.type == CoffeePotEvent.EventType.BREWING_STARTED.value:
            brew_data["started_event"] = sensor_event
            brew_data["created"] = event.created
            brew_data["slack_channel"] = event.slack_channel
            brew_data["slack_ts"]: event.slack_ts
        elif event.type == CoffeePotEvent.EventType.BREWING_FINISHED.value:
            brew_data["finished_event"] = sensor_event
            brew_data["status"] = Brew.Status.FINISHED.value
        else:
            print(f"FIXME: [{event.uuid}] Invalid {event.type=}")
            continue

        # machine
        # FIXME: extract dev-name from sensor id. ie ZWayVDev_zway_2-0-49-4 -> dev2
        sensor_id = sensor_event.id
        try:
            brew_data["machine"] = Machine.objects.get(device_name=sensor_id)
        except Machine.DoesNotExist:
            brew_data["machine__device_name"] = sensor_id

        # Join brew data
        if last_brew_data and "started_event" in last_brew_data and "finished_event" in brew_data:
            brew_data_list.append(last_brew_data | brew_data)
            last_brew_data = None
        else:
            last_brew_data = brew_data

    if dry_run:
        print(f"Would create {len(brew_data_list)} brews from {len(events)} coffee pot events")
        return

    brew_obj_list = []
    for brew in brew_data_list:
        device_name = brew.pop("machine__device_name", None)
        if device_name:
            machine, created = Machine.objects.get_or_create(device_name=device_name, defaults={"name": device_name})
            brew["machine"] = machine
        obj = Brew.objects.create(**brew)
        brew_obj_list.append(obj)
    print(f"Created {len(brew_obj_list)} brews from {len(events)} coffee pot events")


class Command(BaseCommand):
    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, dry_run=False, **options):
        migrate(dry_run)
