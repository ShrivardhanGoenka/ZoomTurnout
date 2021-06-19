from django.db import models

# Create your models here.
from django.db import models
from django.contrib import auth
from django.utils import timezone
# Create your models here.
from django.contrib.auth.models import AbstractUser



class User(auth.models.User,auth.models.PermissionsMixin):
#this is called here so that attribute can be set at the application load time
    def __str__(self):
        return "@{}".format(self.username)
