from django.urls import path

from . import views

urlpatterns = [
    path('', views.zc, name='zc'),
    path('wx', views.wx),
    path('dl/', views.dl),
    path('dl_2/', views.dl_2),
    path('sendSms', views.sendSms),
]