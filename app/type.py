from .models import Status, Event, User

from graphene_sqlalchemy import SQLAlchemyObjectType


class EventType(SQLAlchemyObjectType):
    class Meta:
        model = Event


class StatusType(SQLAlchemyObjectType):
    class Meta:
        model = Status


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User
