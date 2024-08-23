from django.urls import path
from .views import (
    RegisterUserView,
    LoginUserView,
    ClientListView,
    CreateClientView,
    ClientDetailView,
    UserProjectListView,
    CreateProjectView,
    ProjectDetailView,
)

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/create/', CreateClientView.as_view(), name='create_client'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('projects/', UserProjectListView.as_view(), name='user_project_list'),
    path('projects/create/', CreateProjectView.as_view(), name='create_project'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
]
