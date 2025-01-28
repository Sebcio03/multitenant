from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from api.customers.serializers import CustomerSerializer
from database.customers.models import Customer


class CustomerViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        department = self.request.query_params.get("department", None)
        if department is None or not department.isdigit():
            return Customer.objects.none()
        return Customer.objects.filter(department_id=int(department))
