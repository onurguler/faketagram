from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/profile_photos/%Y/%m/%d',
                              default='defaults/photos/default_profile_photo.png')
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

    @property
    def followers(self):
        return self.user.followers.all().count()

    @property
    def followings(self):
        return self.user.followings.all().count()

    def get_followers(self):
        followers = []
        for follow in self.user.followers.all():
            followers.append(follow.follower)
        return followers

    def get_followings(self):
        followings = []
        for follow in self.user.followings.all():
            followings.append(follow.followable)
        return followings


class UserFollow(models.Model):
    follower = models.ForeignKey(
        User, related_name='followings', on_delete=models.CASCADE)
    followable = models.ForeignKey(
        User, related_name='followers', on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
