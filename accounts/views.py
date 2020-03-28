from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib import messages

from accounts.forms import SignUpForm, LoginForm

from accounts.models import UserFollow


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

    context['can_follow'] = True if username != request.user.username else False
    if request.user.is_authenticated and context['can_follow']:
        result = user.followers.filter(
            follower__username=request.user.username)
        context['followed'] = True if result else False

    return render(request, 'accounts/profile.html', context)


@login_required
def follow_view(request, username):
    followable = get_object_or_404(User, username=username)

    if followable != request.user:
        _, created = UserFollow.objects.get_or_create(
            follower=request.user, followable=followable)

        if created:
            messages.success(
                request, f'You have successfully followed {followable.username}.')
        else:
            messages.warning(
                request, f'You have already followed {followable.username}.')
    else:
        messages.warning(request, 'You cannot follow yourself.')

    return redirect('accounts:profile', username=followable.username)


@login_required
def unfollow_view(request, username):
    followable = get_object_or_404(User, username=username)

    if followable != request.user:
        follow = get_object_or_404(
            UserFollow, follower=request.user, followable=followable)
        follow.delete()
        messages.success(
            request, f'You have just unfollowed {followable.username}')
    else:
        messages.warning(request, 'You cannot unfollow yourself.')

    return redirect('accounts:profile', username=followable.username)


def followers_list_view(request, username):
    user = get_object_or_404(User, username=username)
    user_followings = None

    if user.is_authenticated:
        user_followings = request.user.profile.get_followings()

    context = {'follows': user.followers.all(),
               'mode': 'Followers',
               'user_followings': user_followings}

    return render(request, 'accounts/followers_list.html', context)


def followings_list_view(request, username):
    user = get_object_or_404(User, username=username)
    user_followings = None

    if user.is_authenticated:
        user_followings = request.user.profile.get_followings()

    context = {'follows': user.followings.all(),
               'mode': 'Followings',
               'user_followings': user_followings}

    return render(request, 'accounts/followings_list.html', context)


def search_accounts_view(request):
    if request.POST:
        # TODO: dynamic search accounts
        pass

    accounts = User.objects.all()

    context = {'accounts': accounts}

    return render(request, 'accounts/search.html', context)
