
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager

from django.contrib.auth import get_user_model
User = get_user_model()

# https://www.youtube.com/watch?v=KO8n02g-Ezc
 
class CustomUser(AbstractUser):

    
    username = models.EmailField(('Username'), max_length=150, unique=True)
    name = models.CharField(('Name'), max_length=150, blank=True)
    email = models.EmailField(('Email Address'), blank=False, unique = True)


    objects = UserManager()

   # EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email',]


    def __str__(self):
        return self.email

        #Hello Pulkit