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
        fields = ("username", "password", )


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'date_joined')


class EndpointCreateSerializer(serializers.ModelSerializer):

    def validate(self, data):

        print('data:', self.context['request'].user.id)
        user_endpoints = Endpoint.objects.filter(user=self.context['request'].user.id)
        
        if len(user_endpoints) > 20:
            raise serializers.ValidationError("the user exceed endpoint creation limitation")

        return data

    class Meta:
        model = Endpoint
        exclude = ('fail_times', 'user')


class EndpointListSerializer(serializers.ModelSerializer):

    user = UserProfileSerializer()

    class Meta:
        model = Endpoint
        fields = '__all__'
        depth = 1
        read_only_fields = ['fail_times']


class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = '__all__'