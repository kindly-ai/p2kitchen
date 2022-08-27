from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

GROUP_NAME = "default"
MESSAGE_TYPE = "kitchen.all"


def send_group_message(message_type=GROUP_NAME, group_name=GROUP_NAME, **kwargs):
    channel_layer = get_channel_layer()
    sync_group_send = async_to_sync(channel_layer.group_send)
    sync_group_send(group_name, {"type": message_type, **kwargs})
