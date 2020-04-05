from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from faketagram_accounts.forms import SignUpForm, LoginForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('core:index')

    form = SignUpForm(request.POST or None)

    if form.is_valid():
        user = form.save()

        user.refresh_from_db()
        user.profile.full_name = form.cleaned_data.get('full_name')
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
            'Sorry, your username or password incorrect. ' +
            'Please double-check your username and password.')

    return render(request, 'accounts/login.html', context={'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('accounts:login')


def search_accounts_view(request):
    if request.POST:
        # TODO: dynamic search accounts
        pass

    accounts = User.objects.all()

    context = {'accounts': accounts}

    return render(request, 'accounts/search.html', context)
