from django.urls import path
from faketagram_core import views

app_name = 'core'

urlpatterns = [
    path('', views.index_view, name='index'),
]
