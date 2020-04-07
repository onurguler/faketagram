from django.contrib import admin

from faketagram_notifications.models import Notification, FollowNotification


admin.site.register(Notification)
admin.site.register(FollowNotification)
