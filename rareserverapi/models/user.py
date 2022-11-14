from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    bio = models.CharField(max_length=1000)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    profile_image_url = models.CharField(max_length=200)
    created = models.DateField(null=False, blank=False)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)

    
