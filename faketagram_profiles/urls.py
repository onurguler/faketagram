from django.urls import path
from faketagram_profiles import views


app_name = 'faketagram_profiles'

urlpatterns = [
    path('<username>/', views.profile_view, name='profile_detail'),
]
