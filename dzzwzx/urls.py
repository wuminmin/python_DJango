from django.urls import path

from . import views

urlpatterns = [
    path('', views.zc, name='zc'),
    # path('wx', views.wx),
    path('dl/', views.dl),
    path('dl_2/', views.dl_2),
    path('sendSms', views.sendSms),
    path('zhuce', views.zhuce),
    path('grzc/', views.grzc),
    path('grzc2/', views.grzc2),
    path('frzc/', views.frzc),
    path('frzc2/', views.frzc2),
    path('yy/', views.yy),
    path('yy2/', views.yy2),
    path('icon',views.icon),
    path('xia_zai_bu_men',views.下载部门列表),
    path('submit_ban_shi',views.提交办事申请),
    path('xia_zai_yu_yue_list',views.下载预约列表),
    path('xia_zai_li_shi_yu_yue_list',views.下载历史预约列表),
    path('zn/', views.zn),
    path('xia_zai_ban_shi', views.下载办事列表),
    path('xia_zai_ban_shi_hui_zong',views.下载办事汇总列表),
    path('submit_qu_xiao_ban_shi',views.取消办事预约),
    path('hdjl/',views.互动交流),
    path('hdjl2/',views.互动交流2),

    path('wst_dl/', views.wst_dl),
    path('wst_yy/', views.wst_yy),


]