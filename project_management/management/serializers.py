from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Username and password are required.")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by']

    def get_created_by(self, obj):
        return obj.created_by.username if obj.created_by else None

class ProjectSerializer(serializers.ModelSerializer):
    client_name = serializers.ReadOnlyField(source='client.client_name')
    users = UserSerializer(many=True, read_only=True) 
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client_name', 'users', 'created_at', 'created_by']
        read_only_fields = ['created_at', 'created_by']

    def get_created_by(self, obj):
        return obj.created_by.username if obj.created_by else None
