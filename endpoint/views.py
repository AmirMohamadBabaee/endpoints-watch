from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from django.contrib.auth import get_user_model

from .serializers import UserSerializer, EndpointSerializer, RequestSerializer
from .models import Endpoint, Request


class CreateUserView(CreateAPIView):

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer


class CreateEndpointView(CreateAPIView):

    model = Endpoint
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EndpointSerializer


class ListUserEndpointView(ListAPIView):

    model = Endpoint
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EndpointSerializer

    def get_queryset(self):

        user = self.request.user
        return user.endpoints.all()



