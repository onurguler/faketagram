from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.utils import timezone
from django.template.loader import render_to_string

from faketagram_photos.forms import PhotoAddForm, PhotoCreateStyleForm, PhotoCreateDetailForm
from faketagram_photos.models import Photo, Like


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
        photo.published_at = timezone.now()
        photo.save()

        return redirect('photos:photo_detail', pk=photo.pk)

    context = {'form': form, 'photo': photo}

    return render(request, 'photos/create_detail.html', context)


class PhotoDetailView(DetailView):
    model = Photo
    template_name = "photos/photo_detail.html"

    def get_queryset(self):
        qs = super().get_queryset().filter(published=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["liked"] = False

        if self.request.user.is_authenticated:
            like_qs_exists = self.object.likes.filter(
                user=self.request.user).exists()
            context['liked'] = like_qs_exists

        return context


@login_required
def like_view(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id, published=True)
    like_qs = photo.likes.filter(user=request.user)

    if not like_qs.exists():
        Like.objects.create(user=request.user, photo=photo)

    return redirect('photos:photo_detail', pk=photo.pk)


@login_required
def unlike_view(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id, published=True)
    like_qs = photo.likes.filter(user=request.user)

    if like_qs.exists():
        like = like_qs[0]
        like.delete()

    return redirect('photos:photo_detail', pk=photo.pk)


def like_list_view(request, photo_id):
    # TODO: html sayfası yok
    # TODO: likeları son eklenene göre sırala
    photo = get_object_or_404(Photo, pk=photo_id, published=True)
    likes = photo.likes.order_by('-created_at')

    if likes.count() <= 0:
        return redirect('photos:photo_detail', pk=photo.pk)

    user_following = None

    if request.user.is_authenticated:
        user_following = request.user.profile.get_following()

    context = {'likes': likes, 'photo_id': photo_id,
               'user_following': user_following}

    return render(request, 'photos/like_list.html', context)


def get_feed(user):
    photos = Photo.objects.filter(
        user__followers__follower=user, published=True).order_by('-published_at')

    user_likes = []
    for like in user.likes.all():
        user_likes.append(like.photo.pk)

    return render_to_string(
        'photos/feed.html', context={'photos': photos, 'user_likes': user_likes})
