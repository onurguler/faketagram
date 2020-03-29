from django import forms

from photos.models import Photo


class PhotoForm(forms.Form):
    image = forms.ImageField()
    caption = forms.CharField(widget=forms.Textarea(), required=False)
