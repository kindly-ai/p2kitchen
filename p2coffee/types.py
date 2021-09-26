import strawberry
from asgiref.sync import sync_to_async
from strawberry.django import auto
from typing import List, Optional

from strawberry.types import Info

from . import models


@strawberry.django.type(models.SlackProfile)
class SlackProfile:
    user_id: auto
    real_name: auto
    display_name: auto
    image_original: auto

    @strawberry.field
    async def liters_total(self, info: Info) -> int:
        @sync_to_async
        def get_liters_total(user_id):
            # FIXME: Just uses a hardcoded machine volumen for now
            return int(models.Brew.objects.filter(brewer_id=user_id).count() * 1.25)

        return await get_liters_total(self.user_id)

    @strawberry.field
    async def image(self, info: Info, size: int = 48) -> str:
        return self.image(size)


@strawberry.django.type(models.BrewReaction)
class BrewReaction:
    id: auto
    reaction: auto
    is_custom_reaction: auto
    user: SlackProfile
    brew: "Brew"
    emoji: str


@strawberry.django.type(models.Brew)
class Brew:
    id: auto
    machine: "Machine"
    brewer: SlackProfile
    reactions: List[BrewReaction]
    status: auto
    progress: int
    created: str
    modified: str


@strawberry.django.type(models.Machine)
class Machine:
    id: auto
    name: auto
    status: auto
    avatar_url: str
    created: str
    modified: str

    @strawberry.field
    async def liters_total(self, info: Info) -> int:
        @sync_to_async
        def get_liters_total(machine_id, volume: int):
            brews = models.Brew.objects.filter(machine_id=machine_id).exclude(status=models.Brew.Status.INVALID.value)
            return int(brews.count() * volume)

        return await get_liters_total(self.id, self.volume)

    @strawberry.field
    async def last_brew(self, info: Info) -> Optional[Brew]:
        @sync_to_async
        def get_last_brew(machine_id):
            brews = models.Brew.objects.filter(machine_id=machine_id).exclude(status=models.Brew.Status.INVALID.value)
            return brews.order_by("modified").last()

        return await get_last_brew(self.id)


@strawberry.type
class Stats:
    @strawberry.field
    async def liters_today(self) -> int:
        @sync_to_async
        def get_liters_today():
            return int(models.Brew.objects.today().count() * 1.25)

        return await get_liters_today()

    @strawberry.field
    async def liters_yesterday(self) -> int:
        @sync_to_async
        def get_liters_yesterday():
            return int(models.Brew.objects.yesterday().count() * 1.25)

        return await get_liters_yesterday()
