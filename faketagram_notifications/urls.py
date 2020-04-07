from django.urls import path
from faketagram_notifications import views

app_name = 'faketagram_notifications'

urlpatterns = [
    path('', views.notification_list_view, name='notification_list'),
]
