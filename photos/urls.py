from django.urls import path
from photos import views


app_name = 'photos'

urlpatterns = [
    path('add/', views.add_view, name='add'),
    path('create/style/', views.create_style_view, name='create_style'),
    path('create/style/cancel/', views.create_style_cancel_view,
         name='create_style_cancel'),
    path('create/detail/', views.create_detail_view, name='create_detail'),
    path('<int:pk>', views.PhotoDetailView.as_view(), name='photo_detail'),
]
