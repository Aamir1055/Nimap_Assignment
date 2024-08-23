from rest_framework import generics,serializers
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

# Register a new user
class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not username or not password or not email:
            return Response({'error': 'Username, password, and email are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)

# Login a user and return JWT tokens
class LoginUserView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
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
class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

# Create a new client
class CreateClientView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# Retrieve, Update, or Delete a client
class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        client = self.get_object()
        if client.created_by != self.request.user:
            raise PermissionDenied("You don't have permission to edit this client.")
        serializer.save()

    def perform_destroy(self, instance):
        client = self.get_object()
        if client.created_by != self.request.user:
            raise PermissionDenied("You don't have permission to delete this client.")
        instance.delete()

# List all projects assigned to the logged-in user
class UserProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(users=self.request.user)

# Create a new project
User = get_user_model()
class CreateProjectView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        client_id = self.request.data.get('client_id')
        user_ids = self.request.data.get('users')

        # Validate client ID
        if not client_id or not Client.objects.filter(id=client_id).exists():
            raise serializers.ValidationError({'client_id': 'Client does not exist.'})

        client = Client.objects.get(id=client_id)

        # Validate users
        if not user_ids:
            raise serializers.ValidationError({'users': 'At least one user must be assigned to the project.'})

        users = User.objects.filter(id__in=user_ids)
        if users.count() != len(user_ids):
            raise serializers.ValidationError({'users': 'Some users do not exist.'})

        # Create the project instance
        project = serializer.save(
            created_by=self.request.user,
            client=client
        )

       
        project.users.set(users)
        project.save()

        
        serializer = self.get_serializer(project)
        return Response(serializer.data)
    
# Retrieve,Delete a project
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]


    def perform_destroy(self, instance):
        project = self.get_object()
        if project.created_by != self.request.user:
            raise PermissionDenied("You don't have permission to delete this project.")
        instance.delete()
