import datetime
from typing import List
from app.controllers import Controller
from app.models.model import Event, User, Status
from app.utils.utils import is_valid_instance_id


class EventController(Controller):
    def get_events(self) -> List[Event]:
        return self.session.query(Event).all()

    def get_event_by_id(self, event_id: int) -> Event:
        return self.session.query(Event).filter(Event.id == event_id).one_or_none()

    def delete_event(self, event_id: int) -> bool:
        if is_valid_instance_id(event_id, Event):
            self.session.query(Event).filter(Event.id == event_id).delete()
            self.session.commit()
            return True
        return False

    def create_event(self, title: str,
                     description: str,
                     date_event: str,
                     author_id: int,
                     status_id: int,
                     participants: List[int]
                     ) -> Event:

        if not (title and len(title) > 5):
            raise Exception('Informe um titulo válido.')

        if not (description and len(description) > 10):
            raise Exception('Informe uma descrição válida.')

        if not (author_id and is_valid_instance_id(author_id, User)):
            raise Exception('Informe um author válido.')

        if not date_event:
            raise Exception("Informe uma data válida.")

        if not (status_id and is_valid_instance_id(status_id, Status)):
            raise Exception('Informe um status válido.')

        event = Event(
            title=title,
            description=description,
            author_id=author_id,
            status_id=status_id,
            date_event=date_event,
            participants=[]
        )

        if participants:
            for user_id in participants:
                if user := is_valid_instance_id(user_id, User):
                    event.participants.append(user)
                else:
                    raise Exception(f"O id: {user_id} não é válido.")

        self.session.add(event)
        self.session.commit()

        return event

    def update_event(self,
                     id: int,
                     title: str,
                     description: str,
                     date_event: str,
                     status_id: int,
                     participants: List[int]
                     ) -> Event:

        event = self.session.query(Event).get(id)

        if title:
            if not (len(title) > 5):
                raise Exception("Informe um titulo válido.")
            event.title = title

        if description:
            if not (len(description) > 10):
                raise Exception("Informe uma descrição válida.")
            event.description = description

        if date_event:
            #if not ((date_event - datetime.datetime.today()).days() == 1):
            #    raise Exception("Informe uma data válida.")
            event.date_event = date_event

        if status_id:
            if not (is_valid_instance_id(status_id, User)):
                raise Exception("Informe um status válido.")
            event.status_id = status_id

        if participants:
            event.participants.clear()
            self.session.commit()
            for user_id in participants:
                if user := is_valid_instance_id(user_id, User):
                    event.participants.append(user)
                else:
                    raise Exception(f"O Id: {user_id} não é válido.")

        self.session.commit()

        return event
