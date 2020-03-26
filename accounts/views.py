from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from accounts.forms import SignUpForm, LoginForm

from django.contrib.auth.models import User
from accounts.models import Profile


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('core:index')

    form = SignUpForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        user.refresh_from_db()

        user.save()

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')

        user = authenticate(username=username, password=password)
        login(request, user)

        messages.success(
            request, f'Registration successful as {user.username}.')

        return redirect('core:index')

    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:index')

    form = LoginForm(request.POST or None)

    if request.POST and form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            messages.success(
                request, f'Successful login user as {user.username}.')
            return redirect('core:index')

        form.add_error(
            'username',
            'Sorry, your username or password incorrect.' +
            'Please double-check your username and password.')

    return render(request, 'accounts/login.html', context={'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('accounts:login')


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    context = {'profile': user.profile}
    return render(request, 'accounts/profile.html', context)
