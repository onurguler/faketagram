import base64

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from photos.forms import PhotoForm
from photos.models import Photo


@login_required
def add_view(request):
    form = PhotoForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        photo = Photo.objects.get_or_create(
            user=request.user, published=False)[0]
        photo.image = form.cleaned_data.get('image')
        photo.save()

        return redirect('photos:create_style')

    return redirect('core:index')


@login_required
def create_style_view(request):
    # # TODO: Work with image without save db
    # form = PhotoForm(request.POST or None, request.FILES or None)

    # context = {'form': form, 'photo': None}

    # if form.is_valid():
    #     form_photo = form.save(commit=False)
    #     photo = Photo.objects.get_or_create(
    #         user=request.user, published=False)[0]
    #     photo.image = form_photo.image
    #     # TODO: Make Image Fılter Effects
    #     photo.save()
    #     context['photo'] = photo
    # else:
    #     return HttpResponse(status=204)
    photo_qs = request.user.photos.filter(published=False)

    if not photo_qs.exists():
        return redirect('core:index')

    photo = photo_qs[0]

    context = {'photo': photo}

    return render(request, 'photos/create_style.html', context)
