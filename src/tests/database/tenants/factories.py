from factory import fuzzy
from factory.django import DjangoModelFactory

from database.tenants import models


class TenantFactory(DjangoModelFactory):
    class Meta:
        model = models.Tenant

    domain = fuzzy.FuzzyText(length=63, chars="abcdefghijklmnopqrstuvwxyz")


class Tenant2UserFactory(DjangoModelFactory):
    class Meta:
        model = models.Tenant2User
