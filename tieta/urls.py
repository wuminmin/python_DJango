from django.urls import path

from . import views

urlpatterns = [
    path('tou_piao', views.images),
    path('image', views.images, name='image'),
    path('dl/', views.dl),
    path('dl_2/', views.dl_2),
    path('submit_ban_shi',views.提交办事申请),
]