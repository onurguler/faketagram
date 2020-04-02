from django.contrib import admin

from faketagram_photos.models import Photo, Like


admin.site.register(Photo)
admin.site.register(Like)
