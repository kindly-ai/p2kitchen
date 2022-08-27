import os
import threading
from collections.abc import AsyncGenerator

import strawberry
from strawberry.types import Info

from p2kitchen.messaging import GROUP_NAME, MESSAGE_TYPE


@strawberry.type
class KitchenEvent:
    type: str
    message: str


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def connect_to_kitchen_events(self, info: Info) -> AsyncGenerator[KitchenEvent, None]:
        """Join and subscribe to global kitchen events."""
        req = info.context.request
        channel_layer = req.channel_layer
        await channel_layer.group_add(GROUP_NAME, req.channel_name)

        message = f"process: {os.getpid()} thread: {threading.current_thread().name}"
        await channel_layer.group_send(GROUP_NAME, {"type": MESSAGE_TYPE, "message": message})

        async for channel_msg in req.channel_listen(MESSAGE_TYPE, groups=[GROUP_NAME]):
            yield KitchenEvent(type=channel_msg["type"], message=channel_msg["message"])
