from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

from django.contrib import messages

from accounts.forms import SignUpForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('core:index')

    form = SignUpForm(request.POST or None)

    if form.is_valid():
        form.save()

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')

        user = authenticate(username=username, password=password)
        login(request, user)

        messages.success(
            request, f'Registration successful as {user.username}')

        return redirect('core:index')

    return render(request, 'accounts/signup.html', {'form': form})
