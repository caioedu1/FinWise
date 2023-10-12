from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=200, null=False)
    last_name = models.CharField(max_length=200, null=False)
    email = models.EmailField(unique=True, null=False)
    cash = models.DecimalField(max_digits=10, decimal_places=2, default=10000)

    

