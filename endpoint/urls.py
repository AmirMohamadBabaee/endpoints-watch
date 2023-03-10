from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (
    CreateUserView, 
    CreateEndpointView, 
    ListUserEndpointView, 
    EndpointRequestListView,
    EndpointWarningView
)

urlpatterns = [
    path('user/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('user/create/', CreateUserView.as_view(), name='create_user'),
    path('endpoint/create/', CreateEndpointView.as_view(), name='create_endpoint'),
    path('endpoint/list/', ListUserEndpointView.as_view(), name='list_user_endpoints'),
    path('endpoint/requests/<int:pk>/', EndpointRequestListView.as_view(), name='requests_status_list'),
    path('endpoint/warnings/', EndpointWarningView.as_view(), name='endpoint_warning_view')
]
