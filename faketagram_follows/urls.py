from django.urls import path
from faketagram_follows import views


app_name = 'faketagram_follows'

urlpatterns = [
    path('<username>/follow/', views.follow_view, name='follow_user'),
    path('<username>/unfollow/', views.unfollow_view, name='unfollow_user'),
    path('<username>/followers/', views.followers_list_view, name='user_followers'),
    path('<username>/followings/',
         views.following_list_view, name='user_following'),
]
