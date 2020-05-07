from django.conf.urls import url
from django.urls import path, include
from . import views
from . import manage_views
urlpatterns = [

    # 食堂订餐123--------------
    url(r'^ding_can_login_check/$', views.订餐登录检查),
    url(r'^ding_can_send_sms_code/$', views.订餐发送验证码),
    url(r'^ding_can_check_sms_code/$', views.订餐校验验证码),
    url(r'^ding_can_get_home_data/$', views.订餐下载主界面数据),
    url(r'^get_ding_can_data/$', views.下载订餐模版),
    url(r'^get_ding_can_data2/$', views.下载订餐模版2),
    url(r'^send_ding_can_data/$', views.上传订餐结果),
    url(r'^send_ding_can_data2/$', views.上传订餐结果2),
    url(r'^ding_can_tong_ji_zhong_can/$', views.订餐统计),
    url(r'^ding_can_xia_zai_he_xiao_ma/$', views.订餐下载核销码),
    url(r'^ding_can_xia_zai_mp3/$', views.订餐下载核销码mp3),
    # url(r'^ding_can_sao_he_xiao_ma/$', views.订餐扫核销码2),
     url(r'^ding_can_sao_he_xiao_ma2/$', views.ding_can_sao_he_xiao_ma2), #扫描核销
    url(r'^ding_can_qu_xiao/$', views.订餐取消),
    url(r'^ding_can_ding_dan/$', views.订餐订单),
    url(r'^ding_can_cai_dan_init/$', views.订餐菜单初始化),
    url(r'^ding_can_cai_dan_fen_ye/$', views.订餐菜单点击分页),
    url(r'^ding_can_cai_ji_init/$', views.订餐采集初始化),
    url(r'^ding_can_ping_jia_init/$', views.订餐评价初始化),
    url(r'^ding_can_image/$', views.订餐评价初始化图片),
    url(r'^ding_can_upload_ping_jia/$', views.订餐上传评价),

    path('wx_pay_success',views.wx_pay_success),
    path('userInfoUpload',views.userInfoUpload),
    path('get_ding_dan',views.get_ding_dan), # 下载需要预定的订单
    path('get_none_prep_ding_dan',views.get_none_prep_ding_dan), #下载非预定的订单
    path('buy_product',views.buy_product), #非预定情况直接购买产品
    # path('wx_user_commit_order',views.wx_user_commit_order), #用户提交订单

    path('login',manage_views.login), #vue管理后台登录
    path('info',manage_views.info), #vue后台获取用户信息
    path('logout',manage_views.logout), #vue后台退出登录
    path('upload_canteen_list',manage_views.upload_canteen_list), #vue上传excel
    path('export_canteen_data',manage_views.export_canteen_data), #vue下载excel

]
