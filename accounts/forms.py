from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True, max_length=200, label='Email Address')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            # self.add_error('email', 'A user with that email already exists.')
            raise forms.ValidationError(
                'A user with that email already exists.')
        return self.cleaned_data['email']
