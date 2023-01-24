from rest_framework import permissions
from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListAPIView
from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404

from .serializers import (
    UserSerializer, 
    EndpointCreateSerializer, 
    EndpointListSerializer, 
    EndpointRequestSerializer,
    EndpointWarningSerializer,
)
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
    serializer_class = EndpointCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListUserEndpointView(ListAPIView):

    model = Endpoint
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EndpointListSerializer

    def get_queryset(self):

        user = self.request.user
        return user.endpoint_set.all()


class EndpointRequestListView(RetrieveAPIView):

    model = Endpoint
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EndpointRequestSerializer

    def get_object(self):
        
        return get_object_or_404(Endpoint, pk=self.kwargs['pk'])


class EndpointWarningView(ListAPIView):

    model = Endpoint
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EndpointWarningSerializer
