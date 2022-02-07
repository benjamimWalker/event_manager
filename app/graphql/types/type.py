from graphene_sqlalchemy import SQLAlchemyObjectType
from app.models.model import Event, Status, User


class EventType(SQLAlchemyObjectType):
    class Meta:
        model = Event


class StatusType(SQLAlchemyObjectType):
    class Meta:
        model = Status


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User
