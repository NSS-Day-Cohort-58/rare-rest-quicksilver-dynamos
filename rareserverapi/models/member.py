from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    bio = models.CharField(max_length=1000)
    profile_image_url = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    
