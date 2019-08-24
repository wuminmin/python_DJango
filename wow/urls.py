from django.urls import path

from . import views

urlpatterns = [
    path('', views.wow_login, name='wow_login'),
]