from django.urls import path

from . import views

urlpatterns = [
    path('rdyw', views.人大要闻),
]