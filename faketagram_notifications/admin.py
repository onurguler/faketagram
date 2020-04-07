from django.contrib import admin

from faketagram_notifications.models import Notification, FollowNotification, PhotoLikeNotification


admin.site.register(Notification)
admin.site.register(FollowNotification)
admin.site.register(PhotoLikeNotification)
