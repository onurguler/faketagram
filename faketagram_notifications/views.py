from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def notification_list_view(request):
    notifications = request.user.notifications.order_by('-updated_at')
    user_following = request.user.profile.get_following()
    context = {'notifications': notifications,
               'user_following': user_following}
    return render(request, 'notifications/notification_list.html', context)
