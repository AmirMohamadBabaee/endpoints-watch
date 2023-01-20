from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Endpoint, Request

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = UserModel
        fields = ( "id", "username", "password", )


class EndpointSerializer(serializers.ModelSerializer):

    def validate(self, data):

        print('data:', data)
        user_endpoints = Endpoint.objects.filter(user==data['user'])
        
        if len(user_endpoints) > 20:
            raise serializers.ValidationError("the user exceed endpoint creation limitation")

        return data

    class Meta:
        model = Endpoint
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = '__all__'