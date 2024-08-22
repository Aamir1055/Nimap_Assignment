from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Client, Project
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
# Register a new user
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data = JSONParser().parse(request)
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return Response({'error': 'Username, password, and email are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    user.save()

    return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)

# Login a user and return JWT tokens
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    data = JSONParser().parse(request)
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })

# List of all clients
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_clients(request):
    clients = Client.objects.all()
    client_list = [
        {
            'id': client.id,
            'client_name': client.client_name,
            'created_at': client.created_at,
            'created_by': client.created_by.username if client.created_by else None
        }
        for client in clients
    ]
    return JsonResponse(client_list, safe=False)

# Create a new client
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_client(request):
    data = JSONParser().parse(request)
    client_name = data.get('client_name')
    if not client_name:
        return Response({'error': 'Client name is required'}, status=status.HTTP_400_BAD_REQUEST)

    client = Client.objects.create(
        client_name=client_name,
        created_by=request.user
    )

    client_info = {
        'id': client.id,
        'client_name': client.client_name,
        'created_at': client.created_at,
        'created_by': client.created_by.username
    }

    return JsonResponse(client_info, status=status.HTTP_201_CREATED)

# Get client info along with their projects
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    client_info = {
        'id': client.id,
        'client_name': client.client_name,
        'projects': [
            {
                'id': project.id,
                'name': project.project_name
            } for project in client.projects.all()
        ],
        'created_at': client.created_at,
        'created_by': client.created_by.username if client.created_by else None,
        'updated_at': client.updated_at
    }
    return JsonResponse(client_info)

# Update Client info
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)

    if client.created_by != request.user:
        raise PermissionDenied("You don't have permission to edit this client")

    data = JSONParser().parse(request)
    client.client_name = data.get('client_name', client.client_name)
    client.save()

    client_info = {
        'id': client.id,
        'client_name': client.client_name,
        'created_at': client.created_at,
        'created_by': client.created_by.username if client.created_by else None,
        'updated_at': client.updated_at
    }

    return JsonResponse(client_info, status=status.HTTP_200_OK)

# Delete client
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)

    if client.created_by != request.user:
        raise PermissionDenied("You don't have permission to delete this client.")

    client.delete()
    return HttpResponse(status=status.HTTP_204_NO_CONTENT)

# Create a new Project and assign it to the users
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt  # Consider using token-based auth instead
def create_project(request):
    data = JSONParser().parse(request)
    project_name = data.get('project_name')
    client_id = data.get('client_id')
    user_ids = data.get('users', [])

    client = get_object_or_404(Client, pk=client_id)
    users = User.objects.filter(id__in=user_ids)

    project = Project.objects.create(
        project_name=project_name,
        client=client,
        created_by=request.user
    )
    project.users.set(users)
    project_info = {
        'id': project.id,
        'project_name': project.project_name,
        'client': project.client.client_name,
        'users': [{'id': user.id, 'name': user.username} for user in project.users.all()],
        'created_at': project.created_at,
        'created_by': project.created_by.username
    }

    return JsonResponse(project_info, status=status.HTTP_201_CREATED)

# List all projects assigned to the logged-in user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user_projects(request):
    projects = Project.objects.filter(users=request.user)
    project_list = [
        {
            'id': project.id,
            'project_name': project.project_name,
            'client_name': project.client.client_name,
            'created_at': project.created_at,
            'created_by': project.created_by.username if project.created_by else None
        }
        for project in projects
    ]
    return JsonResponse(project_list, safe=False)

# Delete a project
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if project.created_by != request.user:
        raise PermissionDenied("You don't have permission to delete this project.")

    project.delete()
    return HttpResponse(status=status.HTTP_204_NO_CONTENT)
