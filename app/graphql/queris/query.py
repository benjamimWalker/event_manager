from typing import List
import graphene
from app.controllers.event.event_controller import EventController
from app.controllers.status.status_controller import StatusController
from app.graphql.types.type import StatusType, UserType, EventType
from app.controllers.user.user_controllers import UserControllers
from app.models.model import Event, User


class StatusesQuery(graphene.ObjectType):
    items = graphene.List(StatusType)

    def resolve_items(self, info) -> List[Event]:
        return StatusController().get_statuses()


class UsersQuery(graphene.ObjectType):
    all = graphene.List(UserType)
    item = graphene.Field(UserType, user_id=graphene.Argument(type_=graphene.Int))

    def resolve_all(self, info) -> List[User]:
        return UserControllers().get_users()

    def resolve_item(self, info, user_id) -> User:
        return UserControllers().get_user_by_id(user_id=user_id)


class EventsQuery(graphene.ObjectType):
    all = graphene.List(EventType)
    item = graphene.Field(EventType, event_id=graphene.Argument(type_=graphene.Int))

    def resolve_item(self, info, event_id) -> Event:
        return EventController().get_event_by_id(event_id=event_id)

    def resolve_all(self, info) -> List[Event]:
        return EventController().get_events()


class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.Argument(type_=graphene.String))

    statuses = graphene.Field(StatusesQuery, resolver=lambda _, __: StatusesQuery)

    users = graphene.Field(UsersQuery, resolver=lambda _, __: UsersQuery)

    events = graphene.Field(EventsQuery, resolver=lambda _, __: EventsQuery)

    def resolve_hello(self, info, name):
        if name:
            return 'hello'

        return f"hello, {name}!!!"
