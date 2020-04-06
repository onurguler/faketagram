from django import forms

from faketagram_profiles.models import Profile


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("photo", "full_name", "bio")
