from django.db import models
from django.contrib.auth.models import User

from faketagram.models import TimeStampedModel


class UserFollow(TimeStampedModel):
    follower = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE)
    followable = models.ForeignKey(
        User, related_name='followers', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.follower.username} follows {self.followable.username}"
