from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=100, help_text='Please tell us your name (Optional).')
    email = forms.EmailField(
        required=True, max_length=200, label='Email Address', help_text='Required. Please provide a email address.')

    class Meta:
        model = User
        fields = ('full_name', 'username',
                  'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(
                'A user with that email already exists.')
        return self.cleaned_data['email']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
