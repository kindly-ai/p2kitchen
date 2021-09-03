import strawberry
from asgiref.sync import sync_to_async
from strawberry.django import auto
from typing import List, Optional

from strawberry.types import Info

from . import models


@strawberry.django.type(models.BrewReaction)
class BrewReaction:
    id: auto
    reaction: auto
    is_custom_reaction: auto
    slack_username: auto
    brew: "Brew"
    emoji: str


@strawberry.django.type(models.Brew)
class Brew:
    id: auto
    machine: "Machine"
    brewer_slack_username: auto
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
        def _get_last_brew(machine_id):
            return models.Brew.objects.filter(machine_id=machine_id).order_by("-modified").last()

        get_last_brew = sync_to_async(_get_last_brew)

        return await get_last_brew(self.id)
