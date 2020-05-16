from django.conf.urls import url
from django.urls import path, include
from . import views
from . import manage_views
urlpatterns = [

    path('login',manage_views.login), #vue管理后台登录
    path('info',manage_views.info), #vue后台获取用户信息
    path('logout',manage_views.logout), #vue后台退出登录
    # path('upload_canteen_list',manage_views.upload_canteen_list), #vue上传excel
    # path('export_canteen_data',manage_views.export_canteen_data), #vue下载excel
    path('base_table_fetchList',manage_views.base_table_fetchList), #下载基本信息数据
    # path('upload_excel_data',manage_views.upload_excel_data), #upload_excel_data

]
