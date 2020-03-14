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
    path('rd_xia_zai_tabs_by_ban_kuai2',views.rd_xia_zai_tabs_by_ban_kuai2),
    path('upload_img', views.upload_img),
    path('tian_qi_xia_zai',views.天气下载),
    path('get_header_menu_list_data',views.get_headermenu_list_data),
    path('get_header_menu_list_data2',views.get_headermenu_list_data2),
    path('login',views.login),
    path('upload_img2', views.upload_img2),
    path('get_tablei_data_by_lan_mu_key',views.get_tablei_data_by_lan_mu_key),
    path('get_tablei_data_by_lanmu',views.get_tablei_data_by_lanmu),
    path('delete_wz',views.delete_wz),
    
]