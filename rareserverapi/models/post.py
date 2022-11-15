from django.db import models

class Post(models.Model):
    author = models.ForeignKey("Member", on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=100)
    publication_date = models.CharField(max_length=30)
    image_url = models.CharField(max_length=200)
    content = models.CharField(max_length=1000)
    approved = models.BooleanField(default=False)
    reactions = models.ManyToManyField('Reaction', through='PostReaction')
    tags = models.ManyToManyField('Tag', through='PostTag')