from django.conf.urls import url
from django.urls import path, include
from . import views
from . import manage_views
urlpatterns = [

    # path('wx_pay_success',views.wx_pay_success),
    # path('userInfoUpload',views.userInfoUpload),
    # path('get_ding_dan',views.get_ding_dan), # 下载需要预定的订单
    # path('get_none_prep_ding_dan',views.get_none_prep_ding_dan), #下载非预定的订单
    # path('buy_product',views.buy_product), #非预定情况直接购买产品

    path('wx_login',views.wx_login), #wx登录
    path('wx_register',views.wx_register), #wx注册
    path('wx_send_sms',views.wx_send_sms), #wx 发短信
    path('wx_search_organization',views.wx_search_organization), #搜索组织
    path('wx_joinDepartment',views.wx_joinDepartment), #加入部门
    path('wx_createDepartment',views.wx_createDepartment), #创建组织

    path('login',manage_views.login), #vue管理后台登录
    path('info',manage_views.info), #vue后台获取用户信息
    path('logout',manage_views.logout), #vue后台退出登录
    path('upload_canteen_list',manage_views.upload_canteen_list), #vue上传excel
    path('export_canteen_data',manage_views.export_canteen_data), #vue下载excel

]
