from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=1000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    