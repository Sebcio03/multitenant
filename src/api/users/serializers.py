from rest_framework import serializers

from database.users.models import AppUser


class SignupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ["email", "password", "first_name", "last_name", "username"]

    def create(self, validated_data):
        user = AppUser.objects.create_user(**validated_data)
        return user
