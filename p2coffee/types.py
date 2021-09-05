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
    image: str

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
    last_brew: Brew
    created: str
    modified: str

    @strawberry.field
    async def last_brew(self, info: Info) -> Optional[Brew]:
        @sync_to_async
        def get_last_brew(machine_id):
            return models.Brew.objects.filter(machine_id=machine_id).order_by("-modified").last()

        return await get_last_brew(self.id)


@strawberry.django.type(models.SlackProfile)
class TopUser:
    user_id: auto
    liters_total: int

    @strawberry.field
    async def liters_total(self, info: Info) -> int:
        @sync_to_async
        def get_last_brew(user_id):
            return int(models.Brew.objects.filter(brewer_id=user_id).count() * 1.25)

        return await get_last_brew(self.user_id)
