from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
import os

from faketagram.models import TimeStampedModel


class Photo(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='photos')
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d')
    published = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.created_at}'


@receiver(models.signals.post_delete, sender=Photo)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(models.signals.pre_save, sender=Photo)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
