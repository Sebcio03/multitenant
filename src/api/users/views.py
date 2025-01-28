from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from api.users.serializers import SignupUserSerializer
from database.users.models import AppUser


class SignupUserView(CreateAPIView):
    queryset = AppUser.objects.all()
    serializer_class = SignupUserSerializer
    permission_classes = [AllowAny]
