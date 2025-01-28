from factory.django import DjangoModelFactory

from database.departments import models


class DepartmentFactory(DjangoModelFactory):
    class Meta:
        model = models.Department
