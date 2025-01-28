from factory.django import DjangoModelFactory

from database.organizations import models


class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = models.Organization
