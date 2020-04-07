from django.contrib import admin

from faketagram_photos.models import Photo, PhotoLike


admin.site.register(Photo)
admin.site.register(PhotoLike)
