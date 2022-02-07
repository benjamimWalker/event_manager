import graphene
from app.db.database import session
from app.graphql.types.type import StatusType, UserType, EventType
from app.models.model import Status, User, Event



class StatusesQuery(graphene.ObjectType):
    items = graphene.List(StatusType)

    def resolve_items(self, info):
        return session.query(Status).all()


class UsersQuery(graphene.ObjectType):
    items = graphene.List(UserType)

    def resolve_items(self, info):
        return session.query(User).all()


class EventsQuery(graphene.ObjectType):
    all = graphene.List(EventType)
    item = graphene.Field(EventType, id_event=graphene.Argument(type_=graphene.Int))

    def resolve_item(self, info, id_event):
        return session.query(Event).filter(Event.id == id_event).one()

    def resolve_all(self, info):
        return session.query(Event).order_by(Event.date_event).all()



class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.Argument(type_=graphene.String))

    statuses = graphene.Field(StatusesQuery, resolver=lambda _, __: StatusesQuery)

    users = graphene.Field(UsersQuery, resolver=lambda _, __: UsersQuery)

    events = graphene.Field(EventsQuery, resolver=lambda _, __: EventsQuery)

    def resolve_hello(self, info, name):
        if name:
            return 'hello'

        return f"hello, {name}!!!"
