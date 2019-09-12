from django.urls import path

from . import views

urlpatterns = [
    path('image', views.images, name='image'),
]