from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User

from faketagram_follows.models import UserFollow
from faketagram_notifications.models import Notification, FollowNotification


@login_required
def handle_ajax_follow(request, username):
    followable = get_object_or_404(User, username=username)

    if followable == request.user:
        return JsonResponse({'result': 'error'})

    user_follow_qs = request.user.following.filter(followable=followable)

    if not user_follow_qs.exists():
        UserFollow.objects.create(follower=request.user, followable=followable)
        result = "follow"

        # Send notification to followable
        follow_notification = FollowNotification.objects.create(
            follower=request.user)
        Notification.objects.create(
            notification_type=Notification.FOLLOW,
            notifiable=followable,
            content_object=follow_notification)
    else:
        user_follow = user_follow_qs[0]
        user_follow.delete()
        result = "unfollow"

    return JsonResponse({
        'result': result,
        'followers': followable.followers.count(),
        'following': followable.following.count()
    })


@login_required
def follow_view(request, username):
    if request.is_ajax():
        return handle_ajax_follow(request, username)

    followable = get_object_or_404(User, username=username)

    if followable != request.user:
        _, created = UserFollow.objects.get_or_create(
            follower=request.user, followable=followable)

        if created:
            messages.success(
                request, f'You have successfully followed {followable.username}.')

            # Send notification to followable
            follow_notification = FollowNotification.objects.create(
                follower=request.user)
            Notification.objects.create(
                user=request.user, notifiable=followable, content_object=follow_notification)
        else:
            messages.warning(
                request, f'You have already followed {followable.username}.')
    else:
        messages.warning(request, 'You cannot follow yourself.')

    return redirect('profiles:profile_detail', username=followable.username)


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

    return redirect('profiles:profile_detail', username=followable.username)


def followers_list_view(request, username):
    user = get_object_or_404(User, username=username)
    user_following = None

    if request.user.is_authenticated:
        user_following = request.user.profile.get_following()

    context = {'followers': user.followers.order_by('-created_at'),
               'user_following': user_following,
               'profile_username': username}

    return render(request, 'follows/followers_list.html', context)


def following_list_view(request, username):
    user = get_object_or_404(User, username=username)
    user_following = None

    if request.user.is_authenticated:
        user_following = request.user.profile.get_following()

    context = {'following': user.following.order_by('-created_at'),
               'user_following': user_following,
               'profile_username': username}

    return render(request, 'follows/following_list.html', context)
