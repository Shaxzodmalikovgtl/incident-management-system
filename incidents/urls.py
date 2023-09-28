from django.urls import path
from .views import (
    UserCreateView,
    UserListView, UserUpdateView, UserDeleteView,
    IncidentCreateView, IncidentListView, IncidentUpdateView,
    IncidentDeleteView, GetInfofromPin
)

urlpatterns = [
    path('users/register/', UserCreateView.as_view(), name='user-create'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserUpdateView.as_view(), name='user-detail'), 
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),

    path('incidents/create/', IncidentCreateView.as_view(), name='incident-create'),
    path('incidents/', IncidentListView.as_view(), name='incident-list'),
    path('incidents/update/', IncidentUpdateView.as_view(), name='incident-update'), 
    path('incidents/delete/', IncidentDeleteView.as_view(), name='incident-delete'),

    path('pincode/<str:pincode>/', GetInfofromPin.as_view(), name='get-pincode-info'),
]
