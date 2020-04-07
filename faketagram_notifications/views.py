from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def notification_list_view(request):
    notifications = request.user.notifications.order_by('-updated_at')
    context = {'notifications': notifications}
    return render(request, 'notifications/notification_list.html', context)
