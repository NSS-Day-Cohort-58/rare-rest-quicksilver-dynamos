from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    bio = models.CharField(max_length=1000)
    profile_image_url = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def num_of_subscribers(self):
        return self.__num_of_subscribers

    @num_of_subscribers.setter
    def num_of_subscribers(self, value):
        self.__num_of_subscribers = value

