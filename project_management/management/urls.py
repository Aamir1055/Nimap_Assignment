from django.urls import path
from . import views


urlpatterns = [
    # Client-related URLs
    path('clients/', views.list_clients, name='list_clients'),  # GET: List all clients
    path('create_clients/', views.create_client, name='create_client'),  # POST: Create a new client
    path('clients/<int:client_id>/', views.retrieve_client, name='retrieve_client'),  # GET: Retrieve a specific client's info
    path('clients/update/<int:client_id>/', views.update_client, name='update_client'),  # PUT/PATCH: Update a client's info
    path('clients/delete/<int:client_id>/', views.delete_client, name='delete_client'),  # DELETE: Delete a client
    
    # Project-related URLs
    path('projects/', views.create_project, name='create_project'),  # POST: Create a new project and assign users
    path('list_projects/', views.list_user_projects, name='list_user_projects'),  # GET: List all projects assigned to the logged-in user
    path('projects/<int:project_id>/', views.delete_project, name='delete_project'),  # DELETE: Delete a project




    #User related URLS
    path('register/', views.register_user, name='register_user'),
    path('login/',views.login_user, name='login_user'),
]
