import graphene

from .database import session

from .type import UserType, EventType, StatusType


class Mutation(graphene.ObjectType):
    pass

# def resolve_remove_event(self, info, id):
#         del session.query(Event).get(id)