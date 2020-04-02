from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from photos.views import get_feed


@login_required
def index_view(request):
    feed = get_feed(request.user)
    return render(request, 'core/index.html', context={'feed': feed})
