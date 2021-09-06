import strawberry

from typing import List

from p2coffee.types import Machine, SlackProfile


@strawberry.type
class Query:
    machines: List[Machine] = strawberry.django.field()
    users: List[SlackProfile] = strawberry.django.field()


schema = strawberry.Schema(query=Query)
