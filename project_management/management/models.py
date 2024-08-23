from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Client(models.Model):
    client_name = models.CharField(max_length=250)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Project(models.Model):
    project_name=models.CharField(max_length=250)
    client=models.ForeignKey(Client,on_delete=models.CASCADE,related_name='projects')
    users=models.ManyToManyField(User,related_name='assigned_projects')
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateField(auto_now_add=True)
    
