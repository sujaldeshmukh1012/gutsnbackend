from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ('id', 'username', 'email')

# Register Serializer


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        user = UserSerializer(many=False)
        fields = ('id', 'user', 'first_name', 'last_name', 'location',
                  'url', 'profile_info', 'created', 'favorites', 'picture')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'])

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class ProfileRequestSerializer(serializers.Serializer):
    class Meta:
        model = Profile
        fields = ('user')

    def get(self, user):
        profile = Profile.objects.get(user=user['user'])
        return profile
