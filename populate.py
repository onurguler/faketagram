import os
import time
import random
import requests
import django
from faker import Faker


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'faketagram.settings')
django.setup()

# Faker.seed(0)

try:
    from django.core.files import File
    from django.core.files.temp import NamedTemporaryFile
    from django.contrib.auth.models import User
    from faketagram_photos.models import Photo, Like, IMAGE_FILTER_CHOICES
    from faketagram_follows.models import UserFollow
except ImportError:
    exit(1)


def save_image_from_url(model_image, url):
    response = requests.get(url)

    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(response.content)
    img_temp.flush()

    model_image.save("image.jpg", File(img_temp), save=True)


def populate_users(count=10):
    fake = Faker()

    password = '123qwe123qwe'
    rnd_profile_photo_url = 'https://source.unsplash.com/random?people'

    for _ in range(int(count)):
        fake_profile = fake.profile()

        new_user = User(
            username=fake_profile['username'], email=fake_profile['mail'])
        new_user.set_password(password)
        new_user.save()

        user = User.objects.get(username=fake_profile['username'])
        user.refresh_from_db()
        user.profile.full_name = fake_profile['name']
        user.profile.bio = fake_profile['address']
        user.save()

        save_image_from_url(user.profile.photo, rnd_profile_photo_url)

        print('CREATED USER:', user)

        time.sleep(1)


def populate_photos(count=10):
    fake = Faker()
    rnd_photo_url = 'https://source.unsplash.com/random'

    for _ in range(int(count)):
        user = User.objects.order_by('?').first()
        caption = fake.text()
        image_filter = random.choice(IMAGE_FILTER_CHOICES)[0]
        published_at = fake.date_time_between(start_date='-1y')

        photo = Photo.objects.create(user=user, caption=caption, image_filter=image_filter,
                                     published=True, published_at=published_at)

        save_image_from_url(photo.image, rnd_photo_url)

        print('CREATED PHOTO:', photo)

        time.sleep(1)


def populate_likes(count=10):
    for _ in range(int(count)):
        user = User.objects.order_by('?').first()
        photo = Photo.objects.order_by('?').first()

        like = Like.objects.get_or_create(user=user, photo=photo)[0]

        print('CREATED LIKE:', like)


def populate_follows(count=10):
    for _ in range(int(count)):
        follower = User.objects.order_by('?').first()
        followable = User.objects.order_by('?').first()

        if follower != followable:
            follow, created = UserFollow.objects.get_or_create(
                follower=follower, followable=followable)

            if created:
                print('CREATED FOLLOW:', follow)


def populate_admin(generate='no'):
    if generate == 'yes':
        user = User(username='admin', is_staff=True, is_superuser=True)
        user.set_password('123456')
        user.save()


if __name__ == '__main__':
    print('Recommended no')
    populate_admin(input('Generate admin (yes, no): ') or 'no')
    print('Recommended user count is 10')
    populate_users(input('User count: ') or 10)
    print('Recommended photo count is 10')
    populate_photos(input('Photo count: ') or 10)
    print('Recommended like count is 10')
    populate_likes(input('Like count: ') or 10)
    print('Recommended follow count is 10')
    populate_follows(input('Follow count: ') or 10)
