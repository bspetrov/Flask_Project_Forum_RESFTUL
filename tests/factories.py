import factory

from db import db
from models import ForumUserModel, UserRole, ForumManagerModel


class BaseFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        object = super().create(**kwargs)
        db.session.add(object)
        db.session.flush()
        return object


class ForumUserFactory(BaseFactory):
    class Meta:
        model = ForumUserModel

    id = factory.Sequence(lambda n: n)
    username = factory.Faker("user_name")
    password = factory.Faker("password")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    role = UserRole.simple_user


class ManagerUserFactory(BaseFactory):
    class Meta:
        model = ForumManagerModel

    id = factory.Sequence(lambda n: n)
    username = factory.Faker("user_name")
    password = factory.Faker("password")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    role = UserRole.manager
