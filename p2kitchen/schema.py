from typing import List

import strawberry

from p2kitchen.subscriptions import Subscription
from p2kitchen.types import Machine, SlackProfile, Stats


# This is needed since stats is a type on the root Query and the default resolver is getattr
# Ref: https://discordapp.com/channels/689806334337482765/773519351423827978/884389613714669568
def resolve_stats() -> Stats:
    return Stats()


@strawberry.type
class Query:
    machines: list[Machine] = strawberry.django.field()
    users: list[SlackProfile] = strawberry.django.field()
    stats: Stats = strawberry.field(resolve_stats)


schema = strawberry.Schema(query=Query, subscription=Subscription)
