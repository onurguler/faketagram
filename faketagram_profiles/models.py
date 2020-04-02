from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from faketagram.models import TimeStampedModel


class Profile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='photos/profile_photos/%Y/%m/%d',
                              default='defaults/photos/default_profile_photo.png')
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

    @property
    def followers(self):
        return self.user.followers.all().count()

    @property
    def following(self):
        return self.user.following.all().count()

    def get_followers(self):
        followers = []
        for follow in self.user.followers.all():
            followers.append(follow.follower)
        return followers

    def get_following(self):
        following = []
        for follow in self.user.following.all():
            following.append(follow.followable)
        return following


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
