from django.urls import path
from faketagram_accounts import views


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_accounts_view, name='search'),
    path('edit/', views.edit_view, name='edit'),
]
