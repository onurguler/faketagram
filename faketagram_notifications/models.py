from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from faketagram.models import TimeStampedModel
from faketagram_photos.models import PhotoLike
from faketagram_follows.models import UserFollow


class Notification(TimeStampedModel):
    notifiable = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications')
    read = models.BooleanField(default=False)

    FOLLOW = 'F'
    PHOTO_LIKE = 'PL'

    NOTIFICATION_TYPES = (
        (FOLLOW, 'Follow'),
        (PHOTO_LIKE, 'Photo Like'),
    )

    notification_type = models.CharField(
        max_length=5, choices=NOTIFICATION_TYPES)

    # Generic relation types
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return f'{self.notifiable.username} - {self.created_at}'


class UserFollowNotification(TimeStampedModel):
    notification = GenericRelation(
        Notification, related_name='follow_notifications')
    user_follow = models.ForeignKey(UserFollow, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_follow.follower} started following {self.user_follow.followable}'


class PhotoLikeNotification(TimeStampedModel):
    notification = GenericRelation(
        Notification, related_name='photo_like_notifications')
    photo_like = models.ForeignKey(PhotoLike, on_delete=models.CASCADE)

    def __str__(self):
        return self.photo_like
