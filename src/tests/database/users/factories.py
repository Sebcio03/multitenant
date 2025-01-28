import factory
from factory.django import DjangoModelFactory

from database.users import models


class AppUserFactory(DjangoModelFactory):
    class Meta:
        model = models.AppUser

    username = factory.Sequence(lambda n: f"user-{n}")
