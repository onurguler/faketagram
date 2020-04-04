from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from faketagram_photos.views import handle_ajax_home_feed


@login_required
def index_view(request):
    if request.is_ajax():
        return handle_ajax_home_feed(request)
    return render(request, 'core/index.html')
