from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from p2kitchen.models import Machine

GROUP_NAME = "default"
MESSAGE_TYPE = "kitchen.all"


def send_group_message(message_type=GROUP_NAME, group_name=GROUP_NAME, **kwargs):
    channel_layer = get_channel_layer()
    sync_group_send = async_to_sync(channel_layer.group_send)
    sync_group_send(group_name, {"type": message_type, **kwargs})


def send_full_machine_update():
    send_group_message(message_type="machine.update", machine_ids=list(Machine.objects.values_list("id", flat=True)))
