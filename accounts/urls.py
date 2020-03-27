from django.urls import path
from accounts import views


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('<username>/', views.profile_view, name='profile'),
    path('<username>/follow/', views.follow_view, name='follow'),
    path('<username>/unfollow/', views.unfollow_view, name='unfollow'),
    path('<username>/followers/', views.followers_list_view, name='followers'),
    path('<username>/followings/', views.followings_list_view, name='followings'),
]
