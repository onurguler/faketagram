from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def notification_list_view(request):
    return render(request, 'notifications/notification_list.html')
