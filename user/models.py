from django.db import models
from django.contrib.auth.models import AbstractUser

class Custom_user(AbstractUser):

    def __str__(self):
        return self.username

