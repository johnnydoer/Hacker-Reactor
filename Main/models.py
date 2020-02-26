from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here
class User(AbstractUser):
    is_blogger = models.BooleanField(default=False)
    birth_date = models.DateField(null=True)
