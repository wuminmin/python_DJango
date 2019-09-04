from django.urls import path

from . import views

urlpatterns = [
    path('', views.zc, name='zc'),
]