from django.db import models

class PostReaction(models.Model):
    reaction = models.ForeignKey('Reaction', on_delete=models.CASCADE, related_name='post_react_reactions')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='post_react_users')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_react_posts')
