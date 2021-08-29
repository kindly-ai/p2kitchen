import strawberry
from strawberry.django import auto
from typing import List
from . import models


@strawberry.django.type(models.BrewReaction)
class BrewReaction:
    id: auto
    reaction: auto
    slack_username: auto
    brew: "Brew"


@strawberry.django.type(models.Brew)
class Brew:
    id: auto
    machine: "Machine"
    brewer_slack_username: auto
    reactions: List[BrewReaction]


@strawberry.django.type(models.Machine)
class Machine:
    id: auto
    name: auto
    brews: List[Brew]
