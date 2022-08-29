import os
import threading
from collections.abc import AsyncGenerator

import strawberry
from asgiref.sync import sync_to_async
from strawberry.types import Info

from p2kitchen import models
from p2kitchen.messaging import GROUP_NAME, MESSAGE_TYPE
from p2kitchen.types import Machine


@strawberry.type
class MachineUpdate:
    machines: list[Machine] = strawberry.django.field()


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def machine_update(self, info: Info) -> AsyncGenerator[MachineUpdate, None]:
        """Any update on machines"""

        @sync_to_async
        def machines_query(machine_ids):
            return list(models.Machine.objects.filter(pk__in=machine_ids))

        req = info.context.request
        channel_layer = req.channel_layer
        await channel_layer.group_add(GROUP_NAME, req.channel_name)
        async for channel_msg in req.channel_listen("machine.update", groups=[GROUP_NAME]):
            machines = await machines_query(channel_msg["machine_ids"])
            yield MachineUpdate(machines=machines)
