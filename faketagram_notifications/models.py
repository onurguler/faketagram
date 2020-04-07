from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from faketagram.models import TimeStampedModel


class Notification(TimeStampedModel):
    notifiable = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications')
    read = models.BooleanField(default=False)

    FOLLOW = 'F'

    NOTIFICATION_TYPES = (
        (FOLLOW, 'Follow'),
    )

    notification_type = models.CharField(
        max_length=5, choices=NOTIFICATION_TYPES)

    # Generic relation types
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return f'{self.notifiable.username} - {self.created_at}'


class FollowNotification(TimeStampedModel):
    notification = GenericRelation(
        Notification, related_name='follow_notifications')
    follower = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return u'%s started follow you.' % self.follower.username
