from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    followers = models.ManyToManyField('self', blank=True, related_name='following', symmetrical=False)
    posts = models.ManyToManyField('Posts', blank=True, related_name='user_posts')

    @property
    def follower_count(self):
        return self.followers.count()

    def __str__(self):
        return self.username

class Posts(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_posts")
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("User", blank=True, related_name="post_likes")

    @property
    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.user} posted {self.content or self.image} on {self.timestamp}"