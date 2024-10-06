from typing import Tuple, Dict

from django.contrib.auth import login, authenticate
from rest_framework import serializers

from applications.users.models import User
from applications.users.utils import get_tokens_for_user


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def login(self, request) -> Tuple[bool, Dict[str, str]]:
        email = self.validated_data['email']
        password = self.validated_data['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            return True, auth_data
        return False, {}


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={'input_type': 'password'}, required=True)
    new_password = serializers.CharField(style={'input_type': 'password'}, required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({'current_password': 'Does not match'})
        return value


# Google Authorization
class InputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(required=False, default='')
    last_name = serializers.CharField(required=False, default='')
