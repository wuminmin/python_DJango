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
    path('wx_create_organization',views.wx_create_organization), #创建组织
    path('wx_get_organizationInfo_list',views.wx_get_organizationInfo_list), #查询用户属于的组织
    path('wx_swicth_organization',views.wx_swicth_organization), #切换组织
    path('wx_get_apply_for_join_organization',views.wx_get_apply_for_join_organization), #查询加入组织的申请
    path('wx_appral_apply_for_join_organization',views.wx_appral_apply_for_join_organization), #审批加入组织的申请
    path('wx_create_supplier',views.wx_create_supplier), #创建供应商
    path('wx_create_supplier_department',views.wx_create_supplier_department), #创建供应商某部门
    path('wx_get_supplierInfo_list',views.wx_get_supplierInfo_list), #查询用户属于的供应商
    path('wx_swicth_supplier',views.wx_swicth_supplier), #切换供应商
    path('wx_get_my_wx_supplier_department_info_list',views.wx_get_my_wx_supplier_department_info_list), #查询相关的供应商部门列表

    path('login',manage_views.login), #vue管理后台登录
    path('info',manage_views.info), #vue后台获取用户信息
    path('logout',manage_views.logout), #vue后台退出登录
    path('upload_canteen_list',manage_views.upload_canteen_list), #vue上传excel
    path('export_canteen_data',manage_views.export_canteen_data), #vue下载excel

]
