from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model
from config.settings import USER_ENDPOINT_CREATION_LIMIT
from .models import Endpoint, Request
from datetime import datetime, timedelta

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

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, data):

        user_endpoints = Endpoint.objects.filter(user=data['user'].id)
        
        if len(user_endpoints) > USER_ENDPOINT_CREATION_LIMIT:
            raise serializers.ValidationError("the user exceed endpoint creation limit")

        return data

    class Meta:
        model = Endpoint
        read_only_fields = ['fail_times']
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Endpoint.objects.all(),
                fields=['user', 'endpoint'],
                message='The user has already monitored this endpoint'
            )
        ]


class EndpointListSerializer(serializers.ModelSerializer):

    user = UserProfileSerializer()
    fail_times = serializers.SerializerMethodField()

    class Meta:
        model = Endpoint
        fields = '__all__'
        depth = 1
        read_only_fields = ['fail_times']

    def get_fail_times(self, instance):
        return instance.get_fail_times()


class EndpointBaseSerializer(serializers.ModelSerializer):

    fail_times = serializers.SerializerMethodField()

    class Meta:
        model = Endpoint
        fields = ['id', 'endpoint', 'threshold', 'fail_times']

    def get_fail_times(self, instance):
        return instance.get_fail_times()


class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = '__all__'


class EndpointRequestSerializer(serializers.ModelSerializer):

    requests = serializers.SerializerMethodField()
    fail_times = serializers.SerializerMethodField()

    class Meta:
        model = Endpoint
        depth = 1
        fields = ['id', 'endpoint', 'created_at', 'updated_at', 'threshold', 'fail_times', 'requests']

    def get_fail_times(self, instance):
        return instance.get_fail_times()

    def get_requests(self, obj):
        datetime_24_hours_ago = datetime.now() - timedelta(days=1)
        return RequestSerializer(obj.request_set.filter(created_at__gte=datetime_24_hours_ago), many=True).data


class EndpointWarningSerializer(serializers.ModelSerializer):

    fail_times = serializers.SerializerMethodField()

    class Meta:
        model = Endpoint
        fields = ['endpoint', 'created_at', 'updated_at', 'threshold', 'fail_times']

    def get_fail_times(self, instance):
        return instance.get_fail_times()