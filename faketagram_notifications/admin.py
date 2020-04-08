from django.contrib import admin

from faketagram_notifications.models import Notification, UserFollowNotification, PhotoLikeNotification


admin.site.register(Notification)
admin.site.register(UserFollowNotification)
admin.site.register(PhotoLikeNotification)
