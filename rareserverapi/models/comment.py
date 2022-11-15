from django.db import models

class Comment(models.Model):
    author = models.ForeignKey('Member', on_delete=models.CASCADE, related_name='comment_authors')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comment_posts')
    content = models.CharField(max_length=1000)