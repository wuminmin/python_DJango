from django.urls import path

from . import views

urlpatterns = [
    path('rdyw', views.人大要闻),
    path('rd_updata', views.上传新闻),
    path('image', views.images),
    path('rd_xia_zai',views.新闻下载),
    path('rd_xia_zai_list',views.新闻列表下载),
    path('rd_xia_zai_by_tittle',views.根据标题下载文章),
    path('rd_xia_zai_time_by_tittle',views.根据标题下载时间),
    path('rd_xia_zai_by_lan_mu',views.根据栏目下载目录),
    path('rd_xia_zai_tabs_by_ban_kuai',views.根据板块下载表格),
    path('get_user_info',views.获取用户信息),
    path('upload',views.兑现激励上传文件),
    path('get_tittle_list',views.获得活动列表),
    path('get_tables_by_tittle',views.获得兑现详单),
    path('upload_img', views.upload_img),
    path('upload_img2', views.upload_img2),
    path('get_caidan_by_bankuai',views.get_caidan_by_bankuai),
    path('get_imggrid_by_lanmu',views.get_imggrid_by_lanmu),
    path('delete_img',views.delete_img),
    path('delete_wz',views.delete_wz),

]