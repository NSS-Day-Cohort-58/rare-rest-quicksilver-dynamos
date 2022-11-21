from django.db import models

class Comment(models.Model):
    author = models.ForeignKey('Member', on_delete=models.CASCADE, related_name='comment_authors')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comment_posts')
    content = models.CharField(max_length=1000)
    subject = models.CharField(max_length=100)
    created = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    
