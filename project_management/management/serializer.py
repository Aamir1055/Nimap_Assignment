from rest_framework import serializers
from .models import Client,Project

class ClientSerializer(serializers.ModelSerializer):
    class meta:
        model = Client
        fields=__all__
    
class ProjectSerializer(serializers.ModelSerializers):
    class meta:
        models=Project
        fields=__all__
        

