from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from api.users.views import SignupUserView

urlpatterns = [
    path("signin/", obtain_auth_token),
    path("signup/", SignupUserView.as_view()),
]
