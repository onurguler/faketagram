from django.urls import path
from photos import views


app_name = 'photos'

urlpatterns = [
    path('add/', views.add_view, name='add'),
    path('create/style/', views.create_style_view, name='create_style'),
]
