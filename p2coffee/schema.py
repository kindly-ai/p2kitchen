import strawberry

from typing import List

from asgiref.sync import sync_to_async
from strawberry.types import Info

from p2coffee import models
from p2coffee.types import Machine, TopUser


@strawberry.type
class Query:
    machines: List[Machine] = strawberry.django.field()
    top_users: List[TopUser] = strawberry.django.field()

    # FIXME: Why not?
    # @strawberry.field
    # async def top_users(self, info: Info) -> List[TopUser]:
    #     @sync_to_async
    #     def get_top_users():
    #         return models.SlackProfile.objects.all()
    #
    #     return await get_top_users()


schema = strawberry.Schema(query=Query)
