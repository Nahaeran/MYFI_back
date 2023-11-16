from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=300)
    progile_img = models.ImageField(blank=True, null=True)
    financial_products = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    money = models.IntegerField(blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'


