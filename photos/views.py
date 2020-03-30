from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from photos.forms import PhotoAddForm, PhotoCreateStyleForm, PhotoCreateDetailForm
from photos.models import Photo


@login_required
def add_view(request):
    # TODO: published=False data oluşturmadan resmi
    # session'da saklayarak fotoğraf yükleme adımlarını yap
    photo = Photo.objects.get_or_create(
        user=request.user, published=False)[0]
    form = PhotoAddForm(request.POST or None,
                        request.FILES or None, instance=photo)

    if form.is_valid():
        photo = form.save(commit=False)
        photo.image_filter = photo._meta.get_field('image_filter').default
        photo.save()
        return redirect('photos:create_style')

    return redirect('core:index')


@login_required
def create_style_view(request):
    photo_qs = request.user.photos.filter(published=False)

    if not photo_qs.exists():
        return redirect('core:index')

    photo = photo_qs[0]

    form = PhotoCreateStyleForm(request.POST or None, instance=photo)

    if form.is_valid():
        form.save()

        return redirect('photos:create_detail')

    context = {'photo': photo, 'form': form}

    return render(request, 'photos/create_style.html', context)


@login_required
def create_style_cancel_view(request):
    photo_qs = request.user.photos.filter(published=False)

    if photo_qs.exists():
        photo = photo_qs[0]
        photo.delete()

    return redirect('core:index')


@login_required
def create_detail_view(request):
    photo_qs = request.user.photos.filter(published=False)

    if not photo_qs.exists():
        return redirect('core:index')

    photo = photo_qs[0]

    form = PhotoCreateDetailForm(request.POST or None, instance=photo)

    if form.is_valid():
        photo = form.save(commit=False)
        photo.published = True
        photo.save()

        # TODO: return redirect('photos:photo_detail' photo_id=photo.pk)
        return redirect('core:index')

    context = {'form': form, 'photo': photo}

    return render(request, 'photos/create_detail.html', context)
