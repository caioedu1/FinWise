from django.db import models
from django.contrib.auth.models import AbstractUser

def user_avatar_path(instance, filename):
    return f"avatars/user_{instance.id}/{filename}"

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, default="static/imgs/avatar.png")
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]
