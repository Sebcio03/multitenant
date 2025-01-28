from django.contrib.auth.models import AbstractUser


class AppUser(AbstractUser):
    class Meta:
        db_table = 'public"."database_users_appuser'
