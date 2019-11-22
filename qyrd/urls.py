from django.urls import path

from . import views

urlpatterns = [
    path('rdyw', views.人大要闻),
    path('rd_updata', views.上传新闻),
    path('image', views.images),
    path('rd_xia_zai',views.新闻下载),
    path('rd_xia_zai_list',views.新闻列表下载),
]