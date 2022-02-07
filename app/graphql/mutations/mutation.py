import graphene
from app.db.database import session
from app.graphql.types.type import EventType, StatusType, UserType
from app.models.model import User, Event, Status


def return_object_list_of_users(number_list):
    object_list = []
    for number in number_list:
        object_list.append(session.query(User).get(number))
    return object_list


class EventInput(graphene.InputObjectType):
    title = graphene.String(required=True)

    description = graphene.String(required=True)

    active = graphene.Boolean()

    participants = graphene.List(graphene.Int)

    author_id = graphene.Int()

    status_id = graphene.Int()

    date_event = graphene.DateTime()


class UpdateEventInput(EventInput):
    id = graphene.Int(required=True)

    title = graphene.String()

    description = graphene.String()


class UpdateEvent(graphene.Mutation):
    class Arguments:
        event_data = UpdateEventInput(required=True)

    event = graphene.Field(EventType)

    def mutate(self, info, event_data):
        event = session.query(Event).get(event_data.id)

        if event_data.title:
            event.title = event_data.title

        if event_data.description:
            event.description = event_data.description

        if event_data.date_event:
            event.date_event = event_data.date_event

        if event_data.author_id:
            event.author_id = event_data.author_id

        if event_data.participants:
            event.participants = return_object_list_of_users(event_data.participants)

        if event_data.status_id:
            event.status_id = event_data.status_id

        session.commit()

        return UpdateEvent(event=event)



class CreateEvent(graphene.Mutation):
    class Arguments:
        event_data = EventInput(required=True)

    event = graphene.Field(EventType)

    def mutate(self, info, event_data):
        new_event = Event(
            title=event_data.title,
            
            description=event_data.description,
            
            author_id=event_data.author_id,
            
            participants=return_object_list_of_users(event_data.participants),

            date_event=event_data.date_event,

            status_id=event_data.status_id,

            active=event_data.active,
        )

        session.add(new_event)

        session.commit()

        return CreateEvent(event=new_event)


class DeleteEventInput(graphene.InputObjectType):
    id = graphene.Int()


class DeleteEvent(graphene.Mutation):
    class Arguments:
        event_data = DeleteEventInput(required=True)

    event = graphene.Boolean()

    def mutate(self, info, event_data):
        session.query(Event).filter(Event.id == event_data.id).delete()
        
        session.commit()
        
        return DeleteEvent(event=True)
    

class StatusInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    
    active = graphene.Boolean()


class CreateStatus(graphene.Mutation):
    class Arguments:
        status_data = StatusInput(required=True)

    status = graphene.Field(StatusType)

    def mutate(self, info, status_data):
        status = Status(
            name=status_data.name,
        
            active=status_data.active
        )
        session.add(status)
        
        session.commit()
        
        return CreateStatus(status=status)


class CreateUserInput(graphene.InputObjectType):
    name = graphene.String(required=True)

    active = graphene.Boolean()


class CreateUser(graphene.Mutation):
    class Arguments:
        user_data = CreateUserInput(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, user_data):
        user = User(
            name=user_data.name,

            active=user_data.active
        )

        session.add(user)

        session.commit()

        return CreateUser(user=user)



class Mutation(graphene.ObjectType):
    create_status_mutation = CreateStatus.Field()
    
    delete_event_mutation = DeleteEvent.Field()
    
    create_event_mutation = CreateEvent.Field()

    update_event_mutation = UpdateEvent.Field()

    create_user_mutation = CreateUser.Field()

