import graphene
from app.controllers.event.event_controller import EventController
from app.controllers.status.status_controller import StatusController
from app.graphql.types.type import EventType, StatusType, UserType
from app.controllers.user.user_controllers import UserControllers


class InputEvent(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    author_id = graphene.Int(required=True)
    date_event = graphene.DateTime(required=True)
    status_id = graphene.Int(required=True)
    participants = graphene.List(graphene.Int)


class UpdateInputEvent(graphene.InputObjectType):
    id = graphene.Int(required=True)
    title = graphene.String()
    description = graphene.String()
    status_id = graphene.Int()
    date_event = graphene.DateTime()
    participants = graphene.List(graphene.Int)


class UpdateEvent(graphene.Mutation):
    class Arguments:
        data_event = UpdateInputEvent(required=True)
    event = graphene.Field(EventType)

    def mutate(self, info, data_event):
        event = EventController().update_event(data_event.id, data_event.title, data_event.description, data_event.date_event, data_event.status_id, data_event.participants)
        return UpdateEvent(event=event)


class CreateEvent(graphene.Mutation):
    class Arguments:
        data_event = InputEvent(required=True)

    event = graphene.Field(EventType)

    def mutate(self, info, data_event):
        new_event = EventController().create_event(
            title=data_event.title,
            description=data_event.description,
            date_event=data_event.date_event,
            author_id=data_event.author_id,
            participants=data_event.participants,
            status_id=data_event.status_id
        )
        return CreateEvent(event=new_event)


class DeleteEvent(graphene.Mutation):
    class Arguments:
        event_id = graphene.Int(required=True)
    event_deleted = graphene.Boolean()

    def mutate(self, info, event_id):
        event_status = EventController().delete_event(event_id)
        return DeleteEvent(event_deleted=event_status)


class CreateStatus(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
    status = graphene.Field(StatusType)

    def mutate(self, info, name):
        status = StatusController().create_status(name=name)
        return CreateStatus(status=status)


class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
    user = graphene.Field(UserType)

    def mutate(self, info, name):
        user = UserControllers().create_user(name=name)
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_status_mutation = CreateStatus.Field()

    delete_event_mutation = DeleteEvent.Field()

    create_event_mutation = CreateEvent.Field()

    update_event_mutation = UpdateEvent.Field()

    create_user_mutation = CreateUser.Field()
