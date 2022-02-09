from typing import List
from app.controllers import Controller
from app.models.model import Status


class StatusController(Controller):
    def create_status(self, name: str) -> Status:
        if not (name and len(name) > 3):
            raise Exception("Informe um novo status.")

        status = Status(name=name)

        self.session.add(status)
        self.session.commit()
        return status

    def get_statuses(self) -> List[Status]:
        return self.session.query(Status).all()
