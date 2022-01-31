import graphene

from .models import Status, Event, User

from .database import session

from .type import StatusType, EventType, UserType

'''
Todos os dias temos diversos eventos acontecendo na puzzl, desde cerimônias do scrum a reuniões de guilda, sua missão é criar uma api que tem a missão de gerenciar eventos, onde os membros da puzzl possam cadastrar eventos em datas/horários especificos, cumprindo os seguintes objetivos.

- uma forma de cadastrar novos eventos no sistema
- uma forma de listar todos os eventos existentes no sistema (ordenados pela data do evento)
- uma forma de remover um evento da lista
- uma forma de alterar um evento

'''


class StatusesQuery(graphene.ObjectType):
    items = graphene.List(StatusType)

    def resolve_items(self, info):
        return session.query(Status).all()


class UsersQuery(graphene.ObjectType):
    items = graphene.List(UserType)

    def resolve_items(self, info):
        return session.query(User).all()


class EventsQuery(graphene.ObjectType):
    items = graphene.List(EventType)

    def resolve_items(self, info):
        return session.query(Event).order_by(Event.date_event)


class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.Argument(type_=graphene.String, required=False, ))

    statuses = graphene.Field(StatusesQuery, resolver=lambda _, __: StatusesQuery)

    users = graphene.Field(UsersQuery, resolver=lambda _, __: UsersQuery)

    events = graphene.Field(EventsQuery, resolver=lambda _, __: EventsQuery)

    def resolve_hello(self, info, name):
        if name:
            return 'hello'

        return f"hello, {name}!!!"
