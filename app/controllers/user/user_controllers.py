from typing import List, Dict
from app.controllers import Controller
from app.models.model import User
from app.utils.utils import is_valid_instance_id


class UserControllers(Controller):
    def get_object_list_of_users(self, list_ids: List[int]) -> List[User]:
        list_user_objects = []
        for user_id in list_ids:
            if user := is_valid_instance_id(user_id, User):
                list_user_objects.append(user)
        return list_user_objects

    def create_user(self, name: str) -> User:
        if not(name and len(name) > 3):
            raise Exception('Informe um nome de usuário valido.')

        user = User(name=name)

        self.session.add(user)
        self.session.commit()
        return user

    def get_users(self) -> List[User]:
        return self.session.query(User).all()

    def get_user_by_id(self, user_id: int) -> User:
        return self.session.query(User).get(user_id)
