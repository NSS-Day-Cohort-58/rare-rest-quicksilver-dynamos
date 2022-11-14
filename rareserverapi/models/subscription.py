from django.db import models

class Subscription(models.Model):
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name='subscription_followers')
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name='subscription_authors')
    created = models.DateField(null=False, blank=False)
