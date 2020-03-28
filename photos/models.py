from django.db import models
from django.contrib.auth.models import User

from faketagram.models import TimeStampedModel


class Photo(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d')

    def __str__(self):
        return f'{self.user.username} - {self.created_at}'
