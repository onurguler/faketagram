from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User


def profile_view(request, username):
    user = get_object_or_404(User, username=username)

    context = {'profile': user.profile}

    context['can_follow'] = True if username != request.user.username else False
    if request.user.is_authenticated and context['can_follow']:
        result = user.followers.filter(
            follower__username=request.user.username)
        context['followed'] = True if result else False

    photos = user.photos.all()

    context['photos'] = photos

    return render(request, 'profiles/profile_detail.html', context)
