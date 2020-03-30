from django import forms
from photos.models import Photo


class PhotoAddForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ("image",)


class PhotoCreateStyleForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ("image_filter", )


class PhotoCreateDetailForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ("caption",)
