from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    content = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Follow(models.Model):
    follower = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="follower")
    followed_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="followed_user")
