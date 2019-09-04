"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path,include
from mysite import views, ding_can_views, yi_cha_views, chou_jiang_views, cai_ji_views, xiao_shou_views, jdgt_views,wxyy_views

urlpatterns = {

    path('wow/', include('wow.urls')),
    path('dzzwzx/', include('dzzwzx.urls')),

    # 验证码---------------------
    url(r'^$', views.index),
    url(r'^wx$', views.wx),

    url(r'^jian_cha_jing_wei_du/$', views.检查经纬度),

    # 易查199----------------------
    url(r'^yi_cha_login_check/$', yi_cha_views.登录检查),
    url(r'^yi_cha_send_sms_code/$', yi_cha_views.发送验证码),
    url(r'^yi_cha_check_sms_code/$', yi_cha_views.校验验证码),
    url(r'^yi_cha_get_home_data/$', yi_cha_views.下载主界面数据),
    url(r'^yi_cha_get_zcxc_data/$', yi_cha_views.下载政策宣传主界面数据),
    url(r'^yi_cha_get_page_data/$', yi_cha_views.下载试卷),
    url(r'^yi_cha_send_page_data/$', yi_cha_views.交卷),
    url(r'^yi_cha_get_toast_data/$', yi_cha_views.下载toast数据),

    # 食堂订餐123--------------
    url(r'^ding_can_login_check/$', ding_can_views.订餐登录检查),
    url(r'^ding_can_send_sms_code/$', ding_can_views.订餐发送验证码),
    url(r'^ding_can_check_sms_code/$', ding_can_views.订餐校验验证码),
    url(r'^ding_can_get_home_data/$', ding_can_views.订餐下载主界面数据),
    url(r'^get_ding_can_data/$', ding_can_views.下载订餐模版),
    url(r'^get_ding_can_data2/$', ding_can_views.下载订餐模版2),
    url(r'^send_ding_can_data/$', ding_can_views.上传订餐结果),
    url(r'^send_ding_can_data2/$', ding_can_views.上传订餐结果2),
    url(r'^ding_can_tong_ji_zhong_can/$', ding_can_views.订餐统计),
    url(r'^ding_can_xia_zai_he_xiao_ma/$', ding_can_views.订餐下载核销码),
    url(r'^ding_can_xia_zai_mp3/$', ding_can_views.订餐下载核销码mp3),
    url(r'^ding_can_sao_he_xiao_ma/$', ding_can_views.订餐扫核销码2),
    url(r'^ding_can_qu_xiao/$', ding_can_views.订餐取消),
    url(r'^ding_can_ding_dan/$', ding_can_views.订餐订单),
    url(r'^ding_can_cai_dan_init/$', ding_can_views.订餐菜单初始化),
    url(r'^ding_can_cai_dan_fen_ye/$', ding_can_views.订餐菜单点击分页),
    url(r'^ding_can_cai_ji_init/$', ding_can_views.订餐采集初始化),
    url(r'^ding_can_ping_jia_init/$', ding_can_views.订餐评价初始化),
    url(r'^ding_can_image/$', ding_can_views.订餐评价初始化图片),
    url(r'^ding_can_upload_ping_jia/$', ding_can_views.订餐上传评价),

    # 快乐抽奖888----------------------
    url(r'^chou_jiang_tui_song/$', chou_jiang_views.抽奖推送微信验证),
    url(r'^chou_jiang_login_check/$', chou_jiang_views.抽奖登录检查),
    url(r'^chou_jiang_send_sms_code/$', chou_jiang_views.抽奖发送验证码),
    url(r'^chou_jiang_check_sms_code/$', chou_jiang_views.抽奖校验验证码),
    url(r'^chou_jiang_get_home_data/$', chou_jiang_views.抽奖下载主界面数据),
    url(r'^chou_jiang_get_page_data/$', chou_jiang_views.抽奖下载名单),
    url(r'^chou_jiang_guan_li/$', chou_jiang_views.抽奖管理初始化),
    url(r'^chou_jiang_form_id/$', chou_jiang_views.抽奖获得form_id),
    url(r'^chou_jiang_btn/$', chou_jiang_views.抽奖按钮),
    url(r'^chou_jiang_cai_ji_chu_shi_hua/$', chou_jiang_views.采集初始化),
    url(r'^chou_jiang_jian_zhu_wu_ming_cheng/$', chou_jiang_views.下载建筑物名称),
    url(r'^chou_jiang_xiu_gai_ji_ban_xin_xi/$', chou_jiang_views.修改基本信息),
    url(r'^chou_jiang_cai_ji_nei_rong/$', chou_jiang_views.下载采集内容),
    url(r'^chou_jiang_shang_chuang_jie_guo/$', chou_jiang_views.上传采集结果),
    url(r'^chou_jiang_shang_chuang_tu_pian/$', chou_jiang_views.上传图片),
    url(r'^chou_jiang_xia_zai_tu_pian/$', chou_jiang_views.下载图片),
    url(r'^chou_jiang_lu_ru/$', chou_jiang_views.下载录入数据),
    url(r'^chou_jiang_fen_ye/$', chou_jiang_views.录入分页),
    url(r'^chou_jiang_mail/$', chou_jiang_views.两高采集表发邮件),

    # 采集
    url(r'^cai_ji_tui_song/$', cai_ji_views.采集推送微信验证),
    url(r'^cai_ji_login_check/$', cai_ji_views.采集登录检查),
    url(r'^cai_ji_send_sms_code/$', cai_ji_views.采集发送验证码),
    url(r'^cai_ji_check_sms_code/$', cai_ji_views.采集校验验证码),
    url(r'^cai_ji_get_home_data/$', cai_ji_views.采集下载主界面数据),
    url(r'^cai_ji_cai_ji_chu_shi_hua/$', cai_ji_views.采集初始化),

    # 销售
    url(r'^xiao_shou_tui_song/$', xiao_shou_views.销售推送微信验证),
    url(r'^xiao_shou_login_check/$', xiao_shou_views.销售登录检查),
    url(r'^xiao_shou_send_sms_code/$', xiao_shou_views.销售发送验证码),
    url(r'^xiao_shou_check_sms_code/$', xiao_shou_views.销售校验验证码),
    url(r'^xiao_shou_get_home_data/$', xiao_shou_views.销售下载主界面数据),
    url(r'^xiao_shou_xia_zai_lu_ru/$', xiao_shou_views.下载录入数据),
    url(r'^xiao_shou_xia_zai_lou_yu/$', xiao_shou_views.下载楼宇信息),
    url(r'^xiao_shou_xiu_gai_lou_yu/$', xiao_shou_views.修改楼宇状态),
    url(r'^xiao_shou_xiu_gai_tong_ji/$', xiao_shou_views.下载小区统计),
    url(r'^xiao_shou_lu_ru_init/$', xiao_shou_views.录入页面初始化),
    url(r'^xiao_shou_shang_chuang_lu_ru/$', xiao_shou_views.上传录入数据),
    url(r'^xiao_shou_shang_chuang_tu_pian/$', xiao_shou_views.上传图片),
    url(r'^xiao_shou_xia_zai_tu_pian/$', xiao_shou_views.下载图片),

    # 结对共拓支撑平台
    url(r'^jdgt_login_check/$', jdgt_views.结对共拓登录检查),
    url(r'^jdgt_send_sms_code/$', jdgt_views.结对共拓发送验证码),
    url(r'^jdgt_check_sms_code/$', jdgt_views.结对共拓校验验证码),
    url(r'^jdgt_get_home_data/$', jdgt_views.结对共拓下载主界面数据),
    # url(r'^jdgt_get_data/$', jdgt_views.下载订餐模版),
    # url(r'^jdgt_send_data/$', jdgt_views.上传订餐结果),
    # url(r'^jdgt_tong_ji_zhong_can/$', jdgt_views.订餐统计中餐),
    # url(r'^jdgt_xia_zai_he_xiao_ma/$', jdgt_views.订餐下载核销码),
    # url(r'^jdgt_xia_zai_mp3/$', jdgt_views.订餐下载核销码mp3),
    # url(r'^jdgt_sao_he_xiao_ma/$', jdgt_views.订餐扫核销码2),
    # url(r'^jdgt_qu_xiao/$', jdgt_views.订餐取消),
    # url(r'^jdgt_ding_dan/$', jdgt_views.订餐订单),
    # url(r'^jdgt_cai_dan_init/$', jdgt_views.订餐菜单初始化),
    # url(r'^jdgt_cai_dan_fen_ye/$', jdgt_views.订餐菜单点击分页),
    # url(r'^jdgt_cai_ji_init/$', jdgt_views.订餐采集初始化),
    # url(r'^jdgt_ping_jia_init/$', jdgt_views.订餐评价初始化),
    # url(r'^jdgt_upload_ping_jia/$', jdgt_views.订餐上传评价),
    url(r'^jdgt_dwmc/$', jdgt_views.客户经理上报单位信息),
    url(r'^jdgt_khjl_init/$', jdgt_views.部门主任选择客户经理初始化),
    url(r'^jdgt_dwmc_init/$', jdgt_views.部门主任选择单位初始化),
    url(r'^jdgt_bmzr_upload_data/$', jdgt_views.部门主任上传数据),
    url(r'^jdgt_bmzr_upload_imge/$', jdgt_views.部门主任上传图片),
    url(r'^jdgt_hszf_init/$', jdgt_views.客户经理核实走访初始化),
    url(r'^jdgt_hszf_detail/$', jdgt_views.客户经理政企校园查询详情),
    url(r'^jdgt_hszf_imge/$', jdgt_views.客户经理核实走访下载图片),
    url(r'^jdgt_hszf_agree/$', jdgt_views.客户经理同意走访任务),
    url(r'^jdgt_hszf_refuse/$', jdgt_views.客户经理不同意走访任务),
    url(r'^jdgt_zqxy_init/$', jdgt_views.政企校园录入积分初始化),
    url(r'^jdgt_zqxy_upload/$', jdgt_views.政企校园录打分),
    url(r'^jdgt_dqb_init/$', jdgt_views.党群部审核初始化),
    url(r'^jdgt_cxrw_init/$', jdgt_views.查询任务初始化),
    url(r'^jdgt_dqb_detail/$', jdgt_views.党群部查询详情),
    url(r'^jdgt_dqb_agree/$', jdgt_views.党群部同意走访任务),
    url(r'^jdgt_cxrw_detail/$', jdgt_views.查询任务详情),
    url(r'^jdgt_dqb_refuse/$', jdgt_views.党群部不同意走访任务),
    url(r'^jdgt_bmzr_jfxj_init/$', jdgt_views.部门主任机房巡检出初始化),
    url(r'^jdgt_bmzr_upload_jfzf_caogao/$', jdgt_views.部门主任上传机房走访草稿),
    url(r'^jdgt_bmzr_upload_jfzf_data/$', jdgt_views.部门主任上传机房走访数据),
    url(r'^jdgt_bmzr_upload_jfzf_images/$', jdgt_views.部门主任上传机房走访图片),
    url(r'^jdgt_cgx_jfxj_init/$', jdgt_views.部门主任草稿箱机房巡检初始化),
    url(r'^jdgt_hszf_jfxj_init/$', jdgt_views.客户经理核实机房巡检初始化),
    url(r'^jdgt_cgx_jfxj_detail/$', jdgt_views.部门主任草稿箱查询详情),
    url(r'^jdgt_hszf_jfxj_detail/$', jdgt_views.客户经理核实机房巡检查询详情),
    url(r'^jdgt_jfxj_agree/$', jdgt_views.客户经理同意机房巡检任务),
    url(r'^jdgt_jfxj_refuse/$', jdgt_views.客户经理不同意机房巡检任务),
    url(r'^jdgt_jfxj_zqxy_upload/$', jdgt_views.政企校园机房巡检打分),
    url(r'^jdgt_jfxj_dqb_agree/$', jdgt_views.党群部同意机房巡检任务),
    url(r'^jdgt_jfxj_dqb_refuse/$', jdgt_views.党群部不同意机房巡检任务),

    #微信公众号
    url(r'^wow_login/$', wxyy_views.注册),
    url(r'^yy/$', wxyy_views.预约),
    url(r'^gly/$', wxyy_views.管理员),
}
