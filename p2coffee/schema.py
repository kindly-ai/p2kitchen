import strawberry

from typing import List

from p2coffee.types import Machine


@strawberry.type
class Query:
    machines: List[Machine] = strawberry.django.field()


schema = strawberry.Schema(query=Query)
