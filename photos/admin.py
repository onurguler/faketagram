from django.contrib import admin

from photos.models import Photo, Like


admin.site.register(Photo)
admin.site.register(Like)
