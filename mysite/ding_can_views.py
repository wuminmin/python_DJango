import datetime
import json
import traceback
import uuid

import os

import pandas
import requests
import time
from django.http import HttpResponse, FileResponse

import myConfig
from mysite.chou_jiang_mongo import 建筑物主键分隔符
from mysite.demo_sms_send import send_sms
from myConfig import appid, secret, grant_type, django_root_path, ding_can_appid, ding_can_secret, ding_can_grant_type, sign_name, \
    template_code
from mysite.ding_can_mongo import 订餐食堂模版表, 订餐结果表, 订餐主界面表, 订餐用户表, 订餐登录状态表, 订餐验证码表, 没吃, 吃过, 中餐统计, 晚餐统计, 订餐核销码表, \
    取消, 订餐部门表, 订餐统计结果, 订餐菜单分页, 订餐菜单表, 菜单分隔符, 订餐菜单模版表, 订餐菜单评价表, 订餐评论表, 早餐统计
import sys

from mysite.schedule_tool import 启动订餐提醒定时器
from mysite.settings import 订餐微信小程序审核开关, 订餐新界面开关


#异步函数
def deprecated_async(f):
    def wrapper(*args, **kwargs):
        from threading import Thread
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

启动订餐提醒定时器()

def 订餐登录检查(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': ding_can_appid, 'secret': ding_can_secret, 'js_code': js_code,
                   'grant_type': ding_can_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        查询结果 = 订餐用户表.objects(openid=r_json['openid']).first()
        if 查询结果 == None:
            自定义登录状态 = "{\"描述\":\"用户不存在\",\"会话\":\"\"}"
            return HttpResponse(自定义登录状态)
        elif 订餐新界面开关:
            自定义登录状态 = "{\"描述\":\"新界面\",\"会话\":\"123456\"}"
            return HttpResponse(自定义登录状态)
        else:
            r = 订餐登录状态表(session_key=r_json['session_key'], openid=r_json['openid']).save()
            自定义登录状态 = "{\"描述\":\"验证通过\",\"会话\":\"" + str(r.id) + "\"}"
            return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')


def 订餐下载主界面数据(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': ding_can_appid, 'secret': ding_can_secret, 'js_code': js_code,
                   'grant_type': ding_can_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 订餐用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            自定义登录状态 = {'描述': '未注册手机号', '姓名': '', '当前日期': '', '类型': ''}
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            手机号 = 用户.手机号
            主界面 = 订餐主界面表.objects(手机号=用户.手机号).first()
            if 主界面 == None:
                if 订餐微信小程序审核开关:
                    创建时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    描述 = '下载成功'
                    主页标题 = '食堂订餐'
                    主页描述 = '食堂订餐'
                    验证码标题 = ''
                    验证码描述 = ''
                    二级部门 = '测试'
                    三级部门 = '测试'
                    四级部门 = '测试'
                    姓名 = '测试用户'
                    主界内容 = [
                        {
                            'id': 'dingcan',
                            'name': '食堂订餐',
                            'open': False,
                            'pages': [
                                {
                                    'url': 'dingcan',
                                    'page_name': '市公司食堂',
                                    'page_desc': '订餐'
                                },
                                {
                                    'url': 'sao_ma',
                                    'page_name': '市公司食堂',
                                    'page_desc': '扫码'
                                },
                                {
                                    'url': 'ding_dan',
                                    'page_name': '市公司食堂',
                                    'page_desc': '订单'
                                }
                            ]
                        },
                        {
                            'id': 'shi_tang_guan_li',
                            'name': '食堂管理',
                            'open': False,
                            'pages': [
                                {
                                    'url': 'shi_tang_guan_li_url',
                                    'page_name': '市公司食堂',
                                    'page_desc': '晚餐统计'
                                },
                                {
                                    'url': 'shi_tang_guan_li_url',
                                    'page_name': '市公司食堂',
                                    'page_desc': '中餐统计'
                                }
                            ]
                        }
                    ]
                    订餐主界面表_save = 订餐主界面表(手机号=str(用户.手机号), 描述=str(描述), 创建时间=str(创建时间),
                           主页标题=str(主页标题),主页描述=str(主页描述), 验证码标题=str(验证码标题),
                           验证码描述=str(验证码描述), 二级部门=二级部门, 三级部门=三级部门, 四级部门=四级部门, 姓名=姓名,
                           主界内容=主界内容).save()
                    自定义登录状态 = 订餐主界面表_save.to_json().encode('utf-8').decode('unicode_escape')
                    return HttpResponse(自定义登录状态)
                自定义登录状态 = "{\"描述\":\"没有数据\",\"会话\":\"" + r_json['session_key'] + "\"}"
                return HttpResponse(自定义登录状态)
            else:
                自定义登录状态 = 主界面.to_json().encode('utf-8').decode('unicode_escape')
                return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')


def 下载订餐模版(request):
    try:
        # 主菜单name = request.GET['name']
        子菜单page_name = request.GET['page_name']
        子菜单page_desc = request.GET['page_desc']
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': ding_can_appid, 'secret': ding_can_secret, 'js_code': js_code,
                   'grant_type': ding_can_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        print(r_json)
        用户 = 订餐用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            自定义登录状态 = "{\"描述\":\"用户不存在\",\"会话\":\"" + r_json['session_key'] + "\"}"
            return HttpResponse(自定义登录状态)
        else:
            手机号 = 用户.手机号
            订餐主界面表first = 订餐主界面表.objects(手机号=手机号).first()
            if 订餐主界面表first == None:
                自定义登录状态 = "{\"描述\":\"用户未授权\",\"会话\":\"" + r_json['session_key'] + "\"}"
                return HttpResponse(自定义登录状态)

            订餐模版表_one = 订餐食堂模版表.objects( 子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc).first()
            if 订餐模版表_one == None:
                自定义登录状态 = "{\"描述\":\"没有食堂\",\"会话\":\"" + r_json['session_key'] + "\"}"
                return HttpResponse(自定义登录状态)
            else:
                食堂地址 = 订餐模版表_one.食堂地址
                主菜单name = 订餐模版表_one.主菜单name
                用餐日期 = time.strftime('%Y-%m-%d', time.localtime(time.time() ))
                预订开始日期 = time.strftime('%Y-%m-%d', time.localtime(time.time() ))
                预订结束日期 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 864000))
                会话 = r_json['session_key']
                描述 = '下载成功'
                if 订餐主界面表first.二级部门 == '青阳分公司':
                    countries = ['无', '预定1份','预定2份','预定3份']
                else:
                    countries = ['无', '预定1份']
                if 订餐主界面表first.二级部门 == '青阳分公司':
                    accounts = ['无', '预定1份','预定2份','预定3份']
                else:
                    accounts = ['无', '预定1份']
                if 订餐主界面表first.二级部门 == '青阳分公司':
                    accounts2 = ['无', '预定1份','预定2份','预定3份']
                else:
                    accounts2 = ['无', '预定1份']

                自定义登录状态 = {
                    '描述': 描述,
                    '会话': 会话,
                    '预订开始日期': 预订开始日期,
                    '预订结束日期': 预订结束日期,
                    '主菜单name': 主菜单name,
                    '子菜单page_name': 子菜单page_name,
                    '子菜单page_desc': 子菜单page_desc,
                    '食堂地址': 食堂地址,
                    '用餐日期': 用餐日期,
                    'countries':countries,
                    'accounts':accounts,
                    'accounts2':accounts2,
                }
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')


def 上传订餐结果(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': ding_can_appid, 'secret': ding_can_secret, 'js_code': js_code,
                   'grant_type': ding_can_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        # r_json = {'openid':'oPngn4yfqDljEh7wvTMD0NHddOOQ','session_key':'session_key'}
        当前时间戳 = time.time()
        当前时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        当前日期加一天 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400))
        当前日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        订餐用户表_one = 订餐用户表.objects(openid=r_json['openid']).first()
        手机号 = 订餐用户表_one.手机号
        订餐主界面表_first = 订餐主界面表.objects(手机号=手机号).first()
        食堂就餐订餐选项 = [0,1,2,3]
        食堂就餐订餐有效选项 = [1,2,3]
        if 订餐用户表_one == None:
            自定义登录状态 = "{\"描述\":\"用户不存在\",\"会话\":\"\"}"
            return HttpResponse(自定义登录状态)
        else:
            if request.GET.get('countryIndex'):
                早餐食堂 = request.GET['countryIndex']
            else:
                早餐食堂 = None
            if request.GET.get('zhong_can_shi_tang'):
                中餐食堂 = request.GET['zhong_can_shi_tang']
            else:
                中餐食堂 = None
            if request.GET.get('wan_can_shi_tang'):
                晚餐食堂 = request.GET['wan_can_shi_tang']
            else:
                晚餐食堂 = None
            if request.GET.get('zhong_can_wai_dai'):
                中餐外带 = request.GET['zhong_can_wai_dai']
            else:
                中餐外带 = None
            if request.GET.get('wan_can_wai_dai'):
                晚餐外带 = request.GET['wan_can_wai_dai']
            else:
                晚餐外带 = None
            主菜单name = request.GET['name']
            子菜单page_name = request.GET['page_name']
            子菜单page_desc = request.GET['page_desc']
            用餐日期 = request.GET['date']
            if 用餐日期 < 当前日期:
                自定义登录状态 = "{\"描述\":\"预订日期不正确\",\"会话\":\"\"}"
                return HttpResponse(自定义登录状态)
            try:
                早餐食堂 = int(早餐食堂)
                中餐食堂 = int(中餐食堂)
                晚餐食堂 = int(晚餐食堂)
                中餐外带 = int(中餐外带)
                晚餐外带 = int(晚餐外带)
            except:
                自定义登录状态 = "{\"描述\":\"预订数量必须是数字\",\"会话\":\"\"}"
                return HttpResponse(自定义登录状态)
            手机号 = 订餐用户表_one.手机号
            订餐食堂模版表_one = 订餐食堂模版表.objects(主菜单name=主菜单name
                                          , 子菜单page_name=子菜单page_name
                                          , 子菜单page_desc=子菜单page_desc
                                          ).first()
            if 订餐食堂模版表_one == None:
                描述 = '没有食堂数据'
                自定义登录状态 = {'描述': 描述, '会话': r_json['session_key']
                           }
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
            else:
                早餐就餐时间 = 用餐日期 + ' ' + 订餐食堂模版表_one.早餐就餐时间
                中餐就餐时间 = 用餐日期 + ' ' + 订餐食堂模版表_one.中餐就餐时间
                晚餐就餐时间 = 用餐日期 + ' ' + 订餐食堂模版表_one.晚餐就餐时间
                预定早餐提前秒 = 订餐食堂模版表_one.预定早餐提前秒
                预定中餐提前秒 = 订餐食堂模版表_one.预定中餐提前秒
                预定晚餐提前秒 = 订餐食堂模版表_one.预定晚餐提前秒
                取消早餐提前秒 = 订餐食堂模版表_one.取消早餐提前秒
                取消中餐提前秒 = 订餐食堂模版表_one.取消中餐提前秒
                取消晚餐提前秒 = 订餐食堂模版表_one.取消晚餐提前秒
                预定早餐提前截止时间 = time.mktime(time.strptime(早餐就餐时间, "%Y-%m-%d %H:%M:%S")) - 预定早餐提前秒
                预定中餐提前截止时间 = time.mktime(time.strptime(中餐就餐时间, "%Y-%m-%d %H:%M:%S")) - 预定中餐提前秒
                预定晚餐提前截止时间 = time.mktime(time.strptime(晚餐就餐时间, "%Y-%m-%d %H:%M:%S")) - 预定晚餐提前秒

                订餐结果表_one = 订餐结果表.objects(手机号=手机号, 主菜单name=主菜单name, 子菜单page_name=子菜单page_name
                                          , 子菜单page_desc=子菜单page_desc, 用餐日期=用餐日期).first()
                # if 订餐结果表_one == None:
                早餐食堂就餐预订数 = 0
                中餐食堂就餐预订数 = 0
                中餐食堂外带预订数 = 0
                晚餐食堂就餐预订数 = 0
                晚餐食堂外带预订数 = 0
                if 早餐食堂 in 食堂就餐订餐选项:
                    if 早餐食堂 in 食堂就餐订餐有效选项:
                        if 当前时间戳 < 预定早餐提前截止时间:
                            早餐食堂就餐预订数 = 早餐食堂
                        else:
                            自定义登录状态 = "{\"描述\":\"已过期，不接收早餐预定\",\"会话\":\"\"}"
                            return HttpResponse(自定义登录状态)
                else:
                    自定义登录状态 = "{\"描述\":\"预订数量超限制\",\"会话\":\"\"}"
                    return HttpResponse(自定义登录状态)
                if 中餐食堂 in 食堂就餐订餐选项:
                    if 中餐食堂 in 食堂就餐订餐有效选项:
                        if 当前时间戳 < 预定中餐提前截止时间:
                            中餐食堂就餐预订数 = 中餐食堂
                        else:
                            自定义登录状态 = "{\"描述\":\"已过期，不接收中餐预定\",\"会话\":\"\"}"
                            return HttpResponse(自定义登录状态)
                else:
                    自定义登录状态 = "{\"描述\":\"预订数量超限制\",\"会话\":\"\"}"
                    return HttpResponse(自定义登录状态)
                # if 当前时间戳 < 预定中餐提前截止时间:
                #     中餐食堂外带预订数 = 中餐外带
                # else:
                #     自定义登录状态 = "{\"描述\":\"已过期，不接收中餐预定\",\"会话\":\"\"}"
                #     return HttpResponse(自定义登录状态)
                if 晚餐食堂 in 食堂就餐订餐选项:
                    if 晚餐食堂 in 食堂就餐订餐有效选项:
                        if 当前时间戳 < 预定晚餐提前截止时间:
                            晚餐食堂就餐预订数 = 晚餐食堂
                        else:
                            自定义登录状态 = "{\"描述\":\"已过期，不接收晚餐预定\",\"会话\":\"\"}"
                            return HttpResponse(自定义登录状态)
                else:
                    自定义登录状态 = "{\"描述\":\"预订数量超限制\",\"会话\":\"\"}"
                    return HttpResponse(自定义登录状态)
                # if 当前时间戳 < 预定晚餐提前截止时间:
                #     晚餐食堂外带预订数 = 晚餐外带
                # else:
                #     自定义登录状态 = "{\"描述\":\"已过期，不接收晚餐预定\",\"会话\":\"\"}"
                #     return HttpResponse(自定义登录状态)
                if 早餐食堂就餐预订数 == 0 and 中餐食堂就餐预订数 == 0 and 中餐食堂外带预订数 == 0 and 晚餐食堂就餐预订数 == 0 and 晚餐食堂外带预订数 == 0:
                    自定义登录状态 = "{\"描述\":\"至少选择一项订餐\",\"会话\":\"\"}"
                    return HttpResponse(自定义登录状态)
                else:
                    if 订餐结果表_one == None:
                        早餐食堂就餐签到 = ''
                        早餐订餐时间 = ''
                        中餐食堂就餐签到 = ''
                        中餐订餐时间 = ''
                        晚餐食堂就餐签到 = ''
                        晚餐订餐时间 = ''
                        if 早餐食堂就餐预订数 > 0:
                            早餐食堂就餐签到 = 没吃
                            早餐订餐时间 = 当前时间
                        if 中餐食堂就餐预订数 > 0:
                            中餐食堂就餐签到 = 没吃
                            中餐订餐时间 = 当前时间
                        if 晚餐食堂就餐预订数 > 0:
                            晚餐食堂就餐签到 = 没吃
                            晚餐订餐时间 = 当前时间
                        订餐结果表(
                            手机号=手机号,
                            主菜单name=主菜单name,
                            子菜单page_name=子菜单page_name,
                            子菜单page_desc=子菜单page_desc,
                            用餐日期=用餐日期,
                            #
                            早餐食堂就餐预订数=早餐食堂就餐预订数,
                            早餐食堂就餐签到=早餐食堂就餐签到,
                            早餐订餐时间=早餐订餐时间,
                            #
                            中餐食堂就餐预订数=中餐食堂就餐预订数,
                            中餐食堂就餐签到=中餐食堂就餐签到,
                            中餐订餐时间=中餐订餐时间,
                            #
                            晚餐食堂就餐预订数=晚餐食堂就餐预订数,
                            晚餐食堂就餐签到=晚餐食堂就餐签到,
                            晚餐订餐时间=晚餐订餐时间
                        ).save()
                        订餐结果表_first = 订餐结果表.objects(手机号=手机号, 主菜单name=主菜单name, 子菜单page_name=子菜单page_name
                                                    , 子菜单page_desc=子菜单page_desc, 用餐日期=用餐日期).first()
                        描述 = '上传成功'
                        订餐结果描述 = '早餐食堂就餐预订数' + str(订餐结果表_first.早餐食堂就餐预订数) \
                                + ',中餐食堂就餐预订数' + str(订餐结果表_first.中餐食堂就餐预订数)\
                                + ',晚餐食堂就餐预订数' + str(订餐结果表_first.晚餐食堂就餐预订数)
                        自定义登录状态 = {'描述': 描述, '会话': r_json['session_key']
                            , '订餐结果描述': 订餐结果描述}
                        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                        自定义登录状态 = str(自定义登录状态)
                        异步计算订餐结果(子菜单page_name,订餐主界面表_first.二级部门)
                        return HttpResponse(自定义登录状态)
                    else:
                        if 早餐食堂就餐预订数 > 0:
                            if 订餐结果表_one.早餐食堂就餐预订数 > 0:
                                自定义登录状态 = "{\"描述\":\"不能重复订餐\",\"会话\":\"\"}"
                                return HttpResponse(自定义登录状态)
                            else:
                                订餐结果表_one.update(
                                    早餐食堂就餐预订数=早餐食堂就餐预订数,
                                    早餐食堂就餐签到=没吃,
                                    早餐订餐时间=当前时间,
                                    早餐取消时间=''
                                )
                        if 中餐食堂就餐预订数 > 0:
                            if 订餐结果表_one.中餐食堂就餐预订数 > 0:
                                自定义登录状态 = "{\"描述\":\"不能重复订餐\",\"会话\":\"\"}"
                                return HttpResponse(自定义登录状态)
                            else:
                                订餐结果表_one.update(
                                    中餐食堂就餐预订数=中餐食堂就餐预订数,
                                    中餐食堂就餐签到=没吃,
                                    中餐订餐时间=当前时间,
                                    中餐取消时间=''
                                )
                        if 晚餐食堂就餐预订数 > 0:
                            if 订餐结果表_one.晚餐食堂就餐预订数 > 0:
                                自定义登录状态 = "{\"描述\":\"不能重复订餐\",\"会话\":\"\"}"
                                return HttpResponse(自定义登录状态)
                            else:
                                订餐结果表_one.update(
                                    晚餐食堂就餐预订数=晚餐食堂就餐预订数,
                                    晚餐食堂就餐签到=没吃,
                                    晚餐订餐时间=当前时间,
                                    晚餐取消时间=''
                                )

                        订餐结果表_first = 订餐结果表.objects(
                            手机号=手机号,
                            主菜单name=主菜单name,
                            子菜单page_name=子菜单page_name,
                            子菜单page_desc=子菜单page_desc,
                            用餐日期=用餐日期
                        ).first()
                        描述 = '上传成功'
                        订餐结果描述 = '早餐食堂就餐预订数' + str(订餐结果表_first.早餐食堂就餐预订数) \
                                 + ',中餐食堂就餐预订数' + str(订餐结果表_first.中餐食堂就餐预订数) \
                                 + ',晚餐食堂就餐预订数' + str(订餐结果表_first.晚餐食堂就餐预订数)
                        自定义登录状态 = {'描述': 描述, '会话': r_json['session_key']
                            , '订餐结果描述': 订餐结果描述}
                        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                        自定义登录状态 = str(自定义登录状态)
                        异步计算订餐结果(子菜单page_name,订餐主界面表_first.二级部门)
                        return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')


def 订餐校验验证码(request):
    手机号 = str(request.GET['phone'])
    验证码 = str(request.GET['sms_code'])
    js_code = request.GET['code']
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    payload = {'appid': ding_can_appid, 'secret': ding_can_secret, 'js_code': js_code,
               'grant_type': ding_can_grant_type}
    r = requests.get(url=url, params=payload)
    r_json = json.loads(r.text)
    openid = r_json['openid']
    r = 订餐验证码表.objects(手机号=手机号)
    for rr in r:
        if rr.验证码 == 验证码:
            订餐用户表(手机号=手机号, openid=openid).save()
            return HttpResponse('绑定成功')
    return HttpResponse('绑定失败')


def 订餐发送验证码(request):
    try:
        手机号 = str(request.GET['phone'])
        if 手机号 == '':
            return HttpResponse("手机号为空")
        else:
            import random
            j = 6
            验证码 = ''.join(str(i) for i in random.sample(range(0, 9), j))  # sample(seq, n) 从序列seq中选择n个随机且独立的元素；
            __business_id = uuid.uuid1()
            params = "{\"code\":\"" + 验证码 + "\"}"
            r = send_sms(__business_id, 手机号, sign_name, template_code, params)
            r2 = json.loads(r)
            if r2['Code'] == 'OK':
                r = 订餐验证码表(验证码=验证码, 手机号=手机号).save()
            return HttpResponse(r2['Code'])
    except:
        return HttpResponse('500')


@deprecated_async
def 异步计算订餐结果(子菜单page_name,二级部门):
    print('异步计算开始', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    第一天 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    第二天 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400))
    日期_list = [第一天,第二天]
    for 日期_list_one in 日期_list:
        日期 = 日期_list_one
        子菜单page_name = 子菜单page_name
        子菜单page_desc_list = ['早餐统计','中餐统计','晚餐统计']
        for 子菜单page_desc_list_one in 子菜单page_desc_list:
            子菜单page_desc = 子菜单page_desc_list_one
            订餐部门表_first = 订餐部门表.objects(二级部门=二级部门).first()
            if 订餐部门表_first == None:
                name_list = []
            else:
                name_list = 订餐部门表_first.三级部门列表
            if 子菜单page_desc == 中餐统计:
                订餐结果表_all = 订餐结果表.objects(子菜单page_name=子菜单page_name, 中餐食堂就餐预订数__gte=1, 用餐日期=日期)
                总人数 = 订餐结果表_all.sum('中餐食堂就餐预订数')
                没吃人数 = 订餐结果表.objects(子菜单page_name=子菜单page_name, 中餐食堂就餐预订数__gte=1, 用餐日期=日期, 中餐食堂就餐签到=没吃).sum('中餐食堂就餐预订数')
                吃过人数 = 订餐结果表.objects(子菜单page_name=子菜单page_name, 中餐食堂就餐预订数__gte=1, 用餐日期=日期, 中餐食堂就餐签到=吃过).sum('中餐食堂就餐预订数')
            elif 子菜单page_desc == 晚餐统计:
                订餐结果表_all = 订餐结果表.objects(子菜单page_name=子菜单page_name, 晚餐食堂就餐预订数__gte=1, 用餐日期=日期)
                总人数 = 订餐结果表_all.sum('晚餐食堂就餐预订数')
                没吃人数 = 订餐结果表.objects(子菜单page_name=子菜单page_name, 晚餐食堂就餐预订数__gte=1, 用餐日期=日期, 晚餐食堂就餐签到=没吃).sum('晚餐食堂就餐预订数')
                吃过人数 = 订餐结果表.objects(子菜单page_name=子菜单page_name, 晚餐食堂就餐预订数__gte=1, 用餐日期=日期, 晚餐食堂就餐签到=吃过).sum('晚餐食堂就餐预订数')
            elif 子菜单page_desc == 早餐统计:
                订餐结果表_all = 订餐结果表.objects(子菜单page_name=子菜单page_name, 早餐食堂就餐预订数__gte=1, 用餐日期=日期)
                总人数 = 订餐结果表_all.sum('早餐食堂就餐预订数')
                没吃人数 = 订餐结果表.objects(子菜单page_name=子菜单page_name, 早餐食堂就餐预订数__gte=1, 用餐日期=日期, 早餐食堂就餐签到=没吃).sum('早餐食堂就餐预订数')
                吃过人数 = 订餐结果表.objects(子菜单page_name=子菜单page_name, 早餐食堂就餐预订数__gte=1, 用餐日期=日期, 早餐食堂就餐签到=吃过).sum('早餐食堂就餐预订数')
            else:
                pass
            r_list = []
            id = 1
            for name_one in name_list:
                r_dict = {}
                r_dict['id'] = id
                id = id + 1
                r_dict['name'] = name_one
                pages = []
                for 订餐结果表_one in 订餐结果表_all:
                    订餐主界面表_first = 订餐主界面表.objects(手机号=订餐结果表_one.手机号, 三级部门=name_one).first()
                    if 订餐主界面表_first == None:
                        continue
                    else:
                        rr_dict = {}
                        if 子菜单page_desc == 中餐统计:
                            if 订餐结果表_one.中餐食堂就餐签到 == 没吃:
                                rr_dict['page_name'] = 订餐主界面表_first.姓名
                                rr_dict['page_desc'] = 订餐结果表_one.中餐食堂就餐签到
                                pages.append(rr_dict)
                        elif 子菜单page_desc == 早餐统计:
                            if 订餐结果表_one.早餐食堂就餐签到 == 没吃:
                                rr_dict['page_name'] = 订餐主界面表_first.姓名
                                rr_dict['page_desc'] = 订餐结果表_one.早餐食堂就餐签到
                                pages.append(rr_dict)
                        else:
                            if 订餐结果表_one.晚餐食堂就餐签到 == 没吃:
                                rr_dict['page_name'] = 订餐主界面表_first.姓名
                                rr_dict['page_desc'] = 订餐结果表_one.晚餐食堂就餐签到
                                pages.append(rr_dict)
                r_dict['num'] = len(pages)
                if  r_dict['num'] == 0:
                    pass
                else:
                    r_dict['pages'] = pages
                    r_list.append(r_dict)
            描述 = '下载成功'
            if 子菜单page_desc == 中餐统计:
                app_tittle = '中餐统计'
            elif 子菜单page_desc == 早餐统计:
                app_tittle = '早餐统计'
            else:
                app_tittle = '晚餐统计'
            app_des = '总人数 ' + str(总人数)
            app_code_des = '吃过 ' + str(吃过人数)
            app_code = '没吃过 ' + str(没吃人数)
            start_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            end_date = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400))
            自定义登录状态 = {
                '描述': 描述, 
                '会话': '23456', 
                'list': r_list, 
                'app_tittle': app_tittle, 
                'app_des': app_des, 
                'app_code_des': app_code_des,
                'app_code': app_code, 
                'date': 日期, 
                'start_date': start_date, 
                'end_date': end_date
            }
            订餐统计结果_first = 订餐统计结果.objects(日期=日期,子菜单page_name=子菜单page_name,子菜单page_desc=子菜单page_desc).first()
            if 订餐统计结果_first == None:
                订餐统计结果(日期=日期,子菜单page_name=子菜单page_name,子菜单page_desc=子菜单page_desc,订餐结果=自定义登录状态).save()
            else:
                订餐统计结果_first.update(订餐结果=自定义登录状态)
    print('异步计算完成',time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


def 订餐统计中餐(request):
    日期 = str(request.GET['date'])
    子菜单page_name = str(request.GET['page_name'])
    子菜单page_desc = str(request.GET['page_desc'])
    if 日期 == '':
        日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    订餐统计结果_first = 订餐统计结果.objects(日期=日期,子菜单page_name=子菜单page_name,子菜单page_desc=子菜单page_desc).first()
    if 订餐统计结果_first == None:
        start_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        end_date = time.strftime('%Y-%m-%d', time.localtime(time.time() + 259200))
        自定义登录状态 = {'描述': '下载成功', '会话': '123456', 'list': [], 'app_tittle': '输入有误'
            , 'app_des': '请联系管理员', 'app_code_des': '', 'app_code': ''
            , 'date': 日期, 'start_date': start_date, 'end_date': end_date
                   }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)
    else:
        自定义登录状态 = 订餐统计结果_first.订餐结果
    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
    自定义登录状态 = str(自定义登录状态)
    return HttpResponse(自定义登录状态)

# def 订餐统计晚餐(request):
#     return None

def 订餐下载核销码(request):
    主菜单name = str(request.GET['name'])
    子菜单page_name = str(request.GET['page_name'])
    子菜单page_desc = str(request.GET['page_desc'])
    主菜单name = '食堂订餐'
    订餐中餐核销码表_first = 订餐核销码表.objects(主菜单name=主菜单name, 子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc).first()
    if 订餐中餐核销码表_first == None:
        if 子菜单page_desc == '中餐核销码':
            订餐核销码表(主菜单name=主菜单name, 子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc, 核销码='123456').save()
            自定义登录状态 = {'核销码': '123456', '手机号': '无', '二级部门': '无', '三级部门': '无', '四级部门': '无', '姓名': '无'}
        elif 子菜单page_desc == '晚餐核销码':
            订餐核销码表(主菜单name=主菜单name, 子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc, 核销码='123456').save()
            自定义登录状态 = {'核销码': '654321', '手机号': '无', '二级部门': '无', '三级部门': '无', '四级部门': '无', '姓名': '无'}
        else:
            自定义登录状态 = {'描述': '入参不合法'}
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
    else:
        自定义登录状态 = 订餐中餐核销码表_first.to_json().encode('utf-8').decode('unicode_escape')
    自定义登录状态 = str(自定义登录状态)
    return HttpResponse(自定义登录状态)

def 订餐扫核销码2(request):
    核销码 = str(request.GET['er_wei_ma'])
    主菜单name = str(request.GET['name'])
    子菜单page_name = str(request.GET['page_name'])
    子菜单page_desc = str(request.GET['page_desc'])
    if 核销码 == '123456':
        当前日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        当前小时 = time.strftime('%H', time.localtime(time.time()))
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': ding_can_appid, 'secret': ding_can_secret, 'js_code': js_code,
                   'grant_type': ding_can_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        session_key = r_json['session_key']
        openid = r_json['openid']
        订餐用户表_first = 订餐用户表.objects(openid=openid).first()
        if 订餐用户表_first == None:
            自定义登录状态 = {'描述': '未注册手机号', '姓名': '', '当前日期': '', '类型': ''}
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        手机号 = 订餐用户表_first.手机号
        订餐主界面表_first = 订餐主界面表.objects(手机号=手机号).first()
        # 订餐结果表_first = 订餐结果表.objects(主菜单name=主菜单name, 子菜单page_name=子菜单page_name, 手机号=手机号, 用餐日期=当前日期).first()
        订餐结果表_first = 订餐结果表.objects(手机号=手机号, 用餐日期=当前日期).first()
        if 订餐结果表_first == None:
            自定义登录状态 = {'描述': '没有订餐', '姓名': '', '当前日期': '', '类型': ''}
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            if 子菜单page_name == '' or 子菜单page_name == None:
                子菜单page_name = 订餐结果表_first.子菜单page_name
            if 当前小时>'05'and 当前小时<'09':
                if 订餐结果表_first.早餐食堂就餐签到 == 没吃:
                    订餐结果表_first.update(早餐食堂就餐签到=吃过)
                    自定义登录状态 = {'描述': '成功', '姓名': 订餐主界面表_first.姓名, '当前日期': 当前日期, '类型': '早餐核销'}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    异步计算订餐结果(子菜单page_name,订餐主界面表_first.二级部门)
                    return HttpResponse(自定义登录状态)
                elif 订餐结果表_first.早餐食堂就餐签到 == 吃过:
                    自定义登录状态 = {'描述': '成功', '姓名': 订餐主界面表_first.姓名, '当前日期': 当前日期, '类型': '早餐核销'}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                else:
                    自定义登录状态 = {'描述': '已经吃过或者已取消', '姓名': '', '当前日期': '', '类型': ''}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
            elif 当前小时>'10'and 当前小时<'15':
                if 订餐结果表_first.中餐食堂就餐签到 == 没吃:
                    订餐结果表_first.update(中餐食堂就餐签到=吃过)
                    自定义登录状态 = {'描述': '成功', '姓名': 订餐主界面表_first.姓名, '当前日期': 当前日期, '类型': '中餐核销'}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    异步计算订餐结果(子菜单page_name,订餐主界面表_first.二级部门)
                    return HttpResponse(自定义登录状态)
                elif 订餐结果表_first.中餐食堂就餐签到 == 吃过:
                    自定义登录状态 = {'描述': '成功', '姓名': 订餐主界面表_first.姓名, '当前日期': 当前日期, '类型': '中餐核销'}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                else:
                    自定义登录状态 = {'描述': '已经吃过或者已取消', '姓名': '', '当前日期': '', '类型': ''}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
            elif  当前小时>'16'and 当前小时<'20':
                if 订餐结果表_first.晚餐食堂就餐签到 == 没吃:
                    订餐结果表_first.update(晚餐食堂就餐签到=吃过)
                    自定义登录状态 = {'描述': '成功', '姓名': 订餐主界面表_first.姓名, '当前日期': 当前日期, '类型': '晚餐核销'}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    异步计算订餐结果(子菜单page_name,订餐主界面表_first.二级部门)
                    return HttpResponse(自定义登录状态)
                elif 订餐结果表_first.晚餐食堂就餐签到 == 吃过:
                    自定义登录状态 = {'描述': '成功', '姓名': 订餐主界面表_first.姓名, '当前日期': 当前日期, '类型': '晚餐核销'}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                else:
                    自定义登录状态 = {'描述': '已经吃过或者已取消', '姓名': '', '当前日期': '', '类型': ''}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
            else:
                自定义登录状态 = {'描述': '不在就餐时间', '姓名': '', '当前日期': '', '类型': ''}
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)

    else:
        自定义登录状态 = {'描述': '这不是核销码', '姓名': '', '当前日期': '', '类型': ''}
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)


def 订餐扫核销码(request):
    核销码 = str(request.GET['er_wei_ma'])
    主菜单name = str(request.GET['name'])
    子菜单page_name = str(request.GET['page_name'])
    子菜单page_desc = str(request.GET['page_desc'])
    订餐核销码表_first = 订餐核销码表.objects(主菜单name=主菜单name, 子菜单page_name=子菜单page_name, 核销码=核销码).first()
    if 订餐核销码表_first == None:
        自定义登录状态 = {'描述': '二维码已过期'}
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)
    else:
        当前日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': ding_can_appid, 'secret': ding_can_secret, 'js_code': js_code,
                   'grant_type': ding_can_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        session_key = r_json['session_key']
        openid = r_json['openid']
        订餐用户表_first = 订餐用户表.objects(openid=openid).first()
        手机号 = 订餐用户表_first.手机号
        订餐主界面表_first = 订餐主界面表.objects(手机号=手机号).first()
        订餐结果表_first = 订餐结果表.objects(主菜单name=主菜单name, 子菜单page_name=子菜单page_name, 手机号=手机号, 用餐日期=当前日期).first()
        if 订餐结果表_first == None:
            自定义登录状态 = {'描述': '没有订餐'}
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            if 订餐核销码表_first.子菜单page_desc == '中餐核销码':
                if 订餐结果表_first.中餐食堂就餐签到 == 没吃:
                    订餐结果表_first.update(中餐食堂就餐签到=吃过)
                    订餐核销码表_first.update(核销码=session_key
                                        , 手机号=手机号, 二级部门=订餐主界面表_first.二级部门
                                        , 三级部门=订餐主界面表_first.三级部门, 四级部门=订餐主界面表_first.四级部门
                                        , 姓名=订餐主界面表_first.姓名
                                        )
                    自定义登录状态 = {'描述': '成功', '姓名': 订餐主界面表_first.姓名, '当前日期': 当前日期, '类型': '中餐核销'}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                else:
                    自定义登录状态 = {'描述': '已经吃过了'}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
            elif 订餐核销码表_first.子菜单page_desc == '晚餐核销码':
                if 订餐结果表_first.晚餐食堂就餐签到 == 没吃:
                    订餐结果表_first.update(晚餐食堂就餐签到=吃过)
                    订餐核销码表_first.update(核销码=session_key
                                        , 手机号=手机号, 二级部门=订餐主界面表_first.二级部门
                                        , 三级部门=订餐主界面表_first.三级部门, 四级部门=订餐主界面表_first.四级部门
                                        , 姓名=订餐主界面表_first.姓名)
                    自定义登录状态 = {'描述': '成功', '姓名': 订餐主界面表_first.姓名, '当前日期': 当前日期, '类型': '晚餐核销'}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                else:
                    自定义登录状态 = {'描述': '已经吃过了'}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
            else:
                自定义登录状态 = {'描述': '核销码错误'}
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)

def 订餐下载核销码mp3(request):
    子菜单page_name = str(request.GET['page_name'])
    子菜单page_desc = str(request.GET['page_desc'])
    # 子菜单page_name = '市公司食堂'
    # 子菜单page_desc = '晚餐核销码'
    订餐中餐核销码表_first = 订餐核销码表.objects(子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc).first()
    if 订餐中餐核销码表_first == None:
        姓名 = '您没有订餐'
    else:
        姓名 = '欢迎' + 订餐中餐核销码表_first.姓名
    from aip import AipSpeech
    """ 你的 APPID AK SK """
    APP_ID = '15273029'
    API_KEY = 'skY2wM5whRPfHgC7vc9DrsmW'
    SECRET_KEY = 'UblS7MlmG30UWZjKCLL8p5HEZ9M0SG1A '
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.synthesis(姓名, 'zh', 1, {
        'vol': 5, 'per': 4
    })
    response = HttpResponse(result)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="auido.mp3"'
    return response


def 订餐订单(request):
    try:
        page_name = request.GET['page_name']
        日期 = request.GET['date']
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': ding_can_appid, 'secret': ding_can_secret, 'js_code': js_code,
                   'grant_type': ding_can_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        当前日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        if 日期 == '':
            日期 = 当前日期
        开始日期 = time.strftime('%Y-%m-%d', time.localtime(time.time() - 864000))
        结束日期 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 864000))
        订餐用户表_one = 订餐用户表.objects(openid=r_json['openid']).first()
        if 订餐用户表_one == None:
            描述 = '用户不存在'
            自定义登录状态 = {'描述': 描述,
                       '日期': 日期,
                       '开始日期': 开始日期,
                       '结束日期': 结束日期,
                       '会话': r_json['session_key']}
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            手机号 = 订餐用户表_one.手机号
            订餐结果表_first = 订餐结果表.objects(手机号=手机号, 用餐日期=日期).first()
            if 订餐结果表_first == None:
                描述 = '没有订餐记录'
                自定义登录状态 = {'描述': 描述,
                           '日期': 日期,
                           '开始日期': 开始日期,
                           '结束日期': 结束日期,
                           '会话': r_json['session_key']}
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
            else:
                订餐主界面表_first = 订餐主界面表.objects(手机号=手机号).first()
                订餐食堂模版表_first = 订餐食堂模版表.objects(子菜单page_name=page_name).first()
                if 订餐食堂模版表_first == None:
                    描述 = '没有食堂数据'
                    自定义登录状态 = {'描述': 描述, '会话': r_json['session_key']}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                if 订餐主界面表_first == None:
                    描述 = '您没有权限'
                    自定义登录状态 = {'描述': 描述, '会话': r_json['session_key']}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                描述 = '下载成功'
                自定义登录状态 = {'描述': 描述, '会话': r_json['session_key'],
                           '主菜单name': 订餐结果表_first.主菜单name,
                           '子菜单page_name': 订餐结果表_first.子菜单page_name,
                           '子菜单page_desc': 订餐结果表_first.子菜单page_desc,
                           '姓名': 订餐主界面表_first.姓名,
                           '食堂地址': 订餐食堂模版表_first.食堂地址,
                           '日期': 日期,
                           '开始日期': 开始日期,
                           '结束日期': 结束日期,

                           '早餐食堂就餐预订数': 订餐结果表_first.早餐食堂就餐预订数,
                           '早餐价格': 订餐食堂模版表_first.早餐价格,
                           '早餐食堂就餐签到': 订餐结果表_first.早餐食堂就餐签到,
                           '早餐订餐时间': 订餐结果表_first.早餐订餐时间,
                           '早餐取消时间': 订餐结果表_first.早餐取消时间,

                           '中餐食堂就餐预订数': 订餐结果表_first.中餐食堂就餐预订数,
                           '中餐价格': 订餐食堂模版表_first.中餐价格,
                           '中餐食堂就餐签到': 订餐结果表_first.中餐食堂就餐签到,
                           '中餐订餐时间': 订餐结果表_first.中餐订餐时间,
                           '中餐取消时间': 订餐结果表_first.中餐取消时间,
                           '晚餐食堂就餐预订数': 订餐结果表_first.晚餐食堂就餐预订数,
                           '晚餐食堂就餐签到': 订餐结果表_first.晚餐食堂就餐签到,
                           '晚餐价格': 订餐食堂模版表_first.晚餐价格,
                           '晚餐订餐时间': 订餐结果表_first.晚餐订餐时间,
                           '晚餐取消时间': 订餐结果表_first.晚餐取消时间
                           }
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                print(自定义登录状态)
                return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')


def 订餐取消(request):
    try:
        取消早餐 = request.GET['qu_xiao_zao_can_flag']
        取消中餐 = request.GET['qu_xiao_zhong_can_flag']
        取消晚餐 = request.GET['qu_xiao_wan_can_flag']
        page_name = request.GET['page_name']
        日期 = request.GET['date']
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': ding_can_appid, 'secret': ding_can_secret, 'js_code': js_code,
                   'grant_type': ding_can_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        # r_json = {'openid':'oPngn4yfqDljEh7wvTMD0NHddOOQ','session_key':'session_key'}
        当前时间戳 = time.time()
        当前日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        当前时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if 日期 == '':
            日期 = 当前日期
        开始日期 = time.strftime('%Y-%m-%d', time.localtime(time.time() - 864000))
        结束日期 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 864000))
        订餐用户表_one = 订餐用户表.objects(openid=r_json['openid']).first()
        if 订餐用户表_one == None:
            自定义登录状态 = "{\"描述\":\"用户不存在\",\"会话\":\"\"}"
            return HttpResponse(自定义登录状态)
        else:
            手机号 = 订餐用户表_one.手机号
            订餐结果表_first = 订餐结果表.objects(手机号=手机号, 用餐日期=日期).first()
            if 订餐结果表_first == None:
                描述 = '没有订餐记录'
                自定义登录状态 = {'描述': 描述, '会话': r_json['session_key']}
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
            else:
                订餐主界面表_first = 订餐主界面表.objects(手机号=手机号).first()
                订餐食堂模版表_first = 订餐食堂模版表.objects(子菜单page_name=page_name).first()
                if 订餐食堂模版表_first == None:
                    描述 = '没有食堂数据'
                    自定义登录状态 = {'描述': 描述, '会话': r_json['session_key']}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                if 订餐主界面表_first == None:
                    描述 = '您没有权限'
                    自定义登录状态 = {'描述': 描述, '会话': r_json['session_key']}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                描述 = '至少选择取消一项'

                早餐就餐时间 = 日期 + ' ' + 订餐食堂模版表_first.早餐就餐时间
                中餐就餐时间 = 日期 + ' ' + 订餐食堂模版表_first.中餐就餐时间
                晚餐就餐时间 = 日期 + ' ' + 订餐食堂模版表_first.晚餐就餐时间
                预定早餐提前秒 = 订餐食堂模版表_first.预定早餐提前秒
                预定中餐提前秒 = 订餐食堂模版表_first.预定中餐提前秒
                预定晚餐提前秒 = 订餐食堂模版表_first.预定晚餐提前秒
                取消早餐提前秒 = 订餐食堂模版表_first.取消早餐提前秒
                取消中餐提前秒 = 订餐食堂模版表_first.取消中餐提前秒
                取消晚餐提前秒 = 订餐食堂模版表_first.取消晚餐提前秒
                取消早餐提前截止时间 = time.mktime(time.strptime(早餐就餐时间, "%Y-%m-%d %H:%M:%S")) - 取消早餐提前秒
                取消中餐提前截止时间 = time.mktime(time.strptime(中餐就餐时间, "%Y-%m-%d %H:%M:%S")) - 取消中餐提前秒
                取消晚餐提前截止时间 = time.mktime(time.strptime(晚餐就餐时间, "%Y-%m-%d %H:%M:%S")) - 取消晚餐提前秒
                if 取消早餐 == 'true':
                    if 订餐结果表_first.早餐食堂就餐签到 != 取消:
                        if 订餐结果表_first.早餐食堂就餐预订数 >= 1:
                            if 当前时间戳 < 取消早餐提前截止时间:
                                if 订餐结果表_first.早餐食堂就餐签到 == 没吃:
                                    订餐结果表_first.update(早餐食堂就餐预订数=0, 早餐食堂就餐签到=取消, 早餐取消时间=当前时间)
                                    异步计算订餐结果(page_name,订餐主界面表_first.二级部门)
                                    描述 = '早餐取消成功'
                                else:
                                    描述 = '早餐已吃过，不能取消'
                            else:
                                描述 = '已超过截止时间，不能取消'
                        else:
                            描述 = '早餐未预定，不能取消'
                    else:
                        描述 = '早餐已取消，不能重复操作'
                if 取消中餐 == 'true':
                    if 订餐结果表_first.中餐食堂就餐签到 != 取消:
                        if 订餐结果表_first.中餐食堂就餐预订数 >= 1:
                            if 当前时间戳 < 取消中餐提前截止时间:
                                if 订餐结果表_first.中餐食堂就餐签到 == 没吃:
                                    订餐结果表_first.update(中餐食堂就餐预订数=0, 中餐食堂就餐签到=取消, 中餐取消时间=当前时间)
                                    异步计算订餐结果(page_name,订餐主界面表_first.二级部门)
                                    描述 = '中餐取消成功'
                                else:
                                    描述 = '中餐已吃过，不能取消'
                            else:
                                描述 = '已超过截止时间，不能取消'
                        else:
                            描述 = '中餐未预定，不能取消'
                    else:
                        描述 = '中餐已取消，不能重复操作'
                if 取消晚餐 == 'true':
                    if 订餐结果表_first.晚餐食堂就餐签到 != 取消:
                        if 订餐结果表_first.晚餐食堂就餐预订数 >= 1:
                            if 当前时间戳 < 取消晚餐提前截止时间:
                                if 订餐结果表_first.晚餐食堂就餐签到 == 没吃:
                                    订餐结果表_first.update(晚餐食堂就餐预订数=0, 晚餐食堂就餐签到=取消, 晚餐取消时间=当前时间)
                                    异步计算订餐结果(page_name,订餐主界面表_first.二级部门)
                                    描述 = '晚餐取消成功'
                                else:
                                    描述 = '晚餐已吃过，不能取消'
                            else:
                                描述 = '已超过截止时间，不能取消'
                        else:
                            描述 = '晚餐未预定，不能取消'
                    else:
                        描述 = '晚餐已取消，不能重复操作'
                订餐结果表_second = 订餐结果表.objects(手机号=手机号, 用餐日期=日期).first()
                自定义登录状态 = {'描述': 描述, '会话': r_json['session_key'],
                           '主菜单name': 订餐结果表_second.主菜单name,
                           '子菜单page_name': 订餐结果表_second.子菜单page_name,
                           '子菜单page_desc': 订餐结果表_second.子菜单page_desc,
                           '姓名': 订餐主界面表_first.姓名,
                           '食堂地址': 订餐食堂模版表_first.食堂地址,
                           '日期': 日期,
                           '开始日期': 开始日期,
                           '结束日期': 结束日期,

                           '早餐食堂就餐预订数': 订餐结果表_second.早餐食堂就餐预订数,
                           '早餐价格': 订餐食堂模版表_first.早餐价格,
                           '早餐食堂就餐签到': 订餐结果表_second.早餐食堂就餐签到,
                           '早餐订餐时间': 订餐结果表_second.早餐订餐时间,
                           '早餐取消时间': 订餐结果表_second.早餐取消时间,

                           '中餐食堂就餐预订数': 订餐结果表_second.中餐食堂就餐预订数,
                           '中餐价格': 订餐食堂模版表_first.中餐价格,
                           '中餐食堂就餐签到': 订餐结果表_second.中餐食堂就餐签到,
                           '中餐订餐时间': 订餐结果表_second.中餐订餐时间,
                           '中餐取消时间': 订餐结果表_second.中餐取消时间,

                           '晚餐食堂就餐预订数': 订餐结果表_second.晚餐食堂就餐预订数,
                           '晚餐食堂就餐签到': 订餐结果表_second.晚餐食堂就餐签到,
                           '晚餐价格': 订餐食堂模版表_first.晚餐价格,
                           '晚餐订餐时间': 订餐结果表_second.晚餐订餐时间,
                           '晚餐取消时间': 订餐结果表_second.晚餐取消时间
                           }
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')

@deprecated_async
def 异步计算菜单(page_name):
    pass

def 订餐菜单初始化(request):
    try:
        js_code = request.GET['code']
        name = request.GET['name']
        page_name = request.GET['page_name']
        page_desc = request.GET['page_desc']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': ding_can_appid, 'secret': ding_can_secret, 'js_code': js_code,
                   'grant_type': ding_can_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 订餐用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            自定义登录状态 = {
                '描述': '未注册手机号',
                'name': name,
                'page_name': page_name,
                'page_desc': page_desc,
                'lou_yu_list': [],
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        主界面表first = 订餐主界面表.objects(手机号=用户.手机号).first()
        if 主界面表first == None:
            自定义登录状态 = {
                '描述': '没有权限',
                'name': name,
                'page_name': page_name,
                'page_desc': page_desc,
                'lou_yu_list': [],
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)

        异步计算菜单(page_name)
        订餐菜单表first = 订餐菜单表.objects(
            食堂名称=page_name
        ).first()
        if     订餐菜单表first == None:
            分工list = [
                {
                    'dan_yuan_id':0,
                    'dan_yuan_name':'2019-03-31_市公司食堂_中餐',
                    'dan_yuan':[
                        {
                            'lou_ceng_id':0,
                            'ceng':[
                                {
                                    'men_pai_id':'2019-03-31_市公司食堂_中餐_青菜',
                                    'men_pai_hao':'青菜',
                                    'zhuang_tai':'placeholder_grey'
                                },
                                {
                                    'men_pai_id': '2019-03-31_市公司食堂_中餐_白菜',
                                    'men_pai_hao': '白菜',
                                    'zhuang_tai': 'placeholder_red'
                                },
                                {
                                    'men_pai_id': '2019-03-31_市公司食堂_中餐_黄花菜',
                                    'men_pai_hao': '黄花菜',
                                    'zhuang_tai': 'placeholder_grey'
                                },
                            ]
                        },
                        {
                            'lou_ceng_id': 1,
                            'ceng': [
                                {
                                    'men_pai_id': '2019-03-31_市公司食堂_中餐_黄鱼',
                                    'men_pai_hao': '黄鱼',
                                    'zhuang_tai': 'placeholder_red'
                                },
                                {
                                    'men_pai_id': '2019-03-31_市公司食堂_中餐_泥鳅',
                                    'men_pai_hao': '泥鳅',
                                    'zhuang_tai': 'placeholder_red'
                                },
                                {
                                    'men_pai_id': '2019-03-31_市公司食堂_中餐_咸鱼',
                                    'men_pai_hao': '咸鱼',
                                    'zhuang_tai': 'placeholder_red'
                                },
                            ]
                        },
                    ]
                },
                {
                    'dan_yuan_id': 1,
                    'dan_yuan_name': '2019-03-31_市公司食堂_晚餐',
                    'dan_yuan': [
                        {
                            'lou_ceng_id': 0,
                            'ceng': [
                                {
                                    'men_pai_id': '2019-03-31_市公司食堂_晚餐_青菜',
                                    'men_pai_hao': '青菜',
                                    'zhuang_tai': 'placeholder_green'
                                },
                                {
                                    'men_pai_id': '2019-03-31_市公司食堂_晚餐_白菜',
                                    'men_pai_hao': '白菜',
                                    'zhuang_tai': 'placeholder_green'
                                },
                                {
                                    'men_pai_id': '2019-03-31_市公司食堂_晚餐_黄花菜',
                                    'men_pai_hao': '黄花菜',
                                    'zhuang_tai': 'placeholder_green'
                                },
                            ]
                        },
                        {
                            'lou_ceng_id': 1,
                            'ceng': [
                                {
                                    'men_pai_id': '2019-03-31_市公司食堂_晚餐_黄鱼',
                                    'men_pai_hao': '黄鱼',
                                    'zhuang_tai': 'placeholder_green'
                                },
                                {
                                    'men_pai_id': '2019-03-31_市公司食堂_晚餐_泥鳅',
                                    'men_pai_hao': '泥鳅',
                                    'zhuang_tai': 'placeholder_green'
                                },
                                {
                                    'men_pai_id': '2019-03-31_市公司食堂_晚餐_咸鱼',
                                    'men_pai_hao': '咸鱼',
                                    'zhuang_tai': 'placeholder_green'
                                },
                            ]
                        },
                    ]
                },
            ]
        else:
            分工list = 订餐菜单表first.菜单列表
        分工list_len = len(分工list)
        分工list_len_取整除 = 分工list_len // 订餐菜单分页
        分工list_len_取整除 = 分工list_len_取整除 +1
        countries = list( range(0,分工list_len_取整除) )
        countries_val = 0
        分工list_slice = 分工list[countries_val * 订餐菜单分页: (countries_val + 1) * 订餐菜单分页]
        自定义登录状态 = {
            '描述': '成功',
            'name': name,
            'page_name':page_name,
            'page_desc':page_desc,
            'countries':countries,
            'lou_yu_list': 分工list_slice,
        }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')

def 订餐菜单点击分页(request):
    try:
        js_code = request.GET['code']
        name = request.GET['name']
        page_name = request.GET['page_name']
        page_desc = request.GET['page_desc']
        countries_val = int( request.GET['countries_val'] )

        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': ding_can_appid, 'secret': ding_can_secret, 'js_code': js_code,
                   'grant_type': ding_can_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 订餐用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            自定义登录状态 = {
                '描述': '未注册手机号',
                'name': name,
                'page_name': page_name,
                'page_desc': page_desc,
                'lou_yu_list': [],
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        主界面表first = 订餐主界面表.objects(手机号=用户.手机号).first()
        if 主界面表first == None:
            自定义登录状态 = {
                '描述': '没有权限',
                'name': name,
                'page_name': page_name,
                'page_desc': page_desc,
                'lou_yu_list': [],
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        录入分工表first = 订餐菜单表.objects(
            食堂名称=page_name
        ).first()
        if 录入分工表first == None:
            分工list = [
                {
                    'dan_yuan_id': 0,
                    'dan_yuan_name': '2019-03-31_中餐',
                    'dan_yuan': [
                        {
                            'lou_ceng_id': 0,
                            'ceng': [
                                {
                                    'men_pai_id': '2019-03-31_中餐_青菜',
                                    'men_pai_hao': '青菜',
                                    'zhuang_tai': 'placeholder_red'
                                },
                                {
                                    'men_pai_id': '2019-03-31_中餐_白菜',
                                    'men_pai_hao': '白菜',
                                    'zhuang_tai': 'placeholder_red'
                                },
                                {
                                    'men_pai_id': '2019-03-31_中餐_黄花菜',
                                    'men_pai_hao': '黄花菜',
                                    'zhuang_tai': 'placeholder_red'
                                },

                            ]
                        },
                        {
                            'lou_ceng_id': 1,
                            'ceng': [
                                {
                                    'men_pai_id': '2019-03-31_中餐_黄鱼',
                                    'men_pai_hao': '黄鱼',
                                    'zhuang_tai': 'placeholder_red'
                                },
                                {
                                    'men_pai_id': '2019-03-31_中餐_泥鳅',
                                    'men_pai_hao': '泥鳅',
                                    'zhuang_tai': 'placeholder_red'
                                },
                                {
                                    'men_pai_id': '2019-03-31_中餐_咸鱼',
                                    'men_pai_hao': '咸鱼',
                                    'zhuang_tai': 'placeholder_red'
                                },

                            ]
                        },
                    ]

                },
                {
                    'dan_yuan_id': 1,
                    'dan_yuan_name': '2019-03-31_晚餐',
                    'dan_yuan': [
                        {
                            'lou_ceng_id': 0,
                            'ceng': [
                                {
                                    'men_pai_id': '2019-03-31_晚餐_青菜',
                                    'men_pai_hao': '青菜',
                                    'zhuang_tai': 'placeholder_green'
                                },
                                {
                                    'men_pai_id': '2019-03-31_晚餐_白菜',
                                    'men_pai_hao': '白菜',
                                    'zhuang_tai': 'placeholder_green'
                                },
                                {
                                    'men_pai_id': '2019-03-31_晚餐_黄花菜',
                                    'men_pai_hao': '黄花菜',
                                    'zhuang_tai': 'placeholder_green'
                                },

                            ]
                        },
                        {
                            'lou_ceng_id': 1,
                            'ceng': [
                                {
                                    'men_pai_id': '2019-03-31_晚餐_黄鱼',
                                    'men_pai_hao': '黄鱼',
                                    'zhuang_tai': 'placeholder_green'
                                },
                                {
                                    'men_pai_id': '2019-03-31_晚餐_泥鳅',
                                    'men_pai_hao': '泥鳅',
                                    'zhuang_tai': 'placeholder_green'
                                },
                                {
                                    'men_pai_id': '2019-03-31_晚餐_咸鱼',
                                    'men_pai_hao': '咸鱼',
                                    'zhuang_tai': 'placeholder_green'
                                },

                            ]
                        },
                    ]

                },
            ]
        else:
            分工list = 录入分工表first.录入分工
        分工list_slice = 分工list[ countries_val*订餐菜单分页 : (countries_val+1)*订餐菜单分页 ]
        自定义登录状态 = {
            '描述': '成功',
            'name': name,
            'page_name':page_name,
            'page_desc':page_desc,
            'lou_yu_list': 分工list_slice,
        }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')

def 订餐采集初始化(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': ding_can_appid, 'secret': ding_can_secret, 'js_code': js_code,
                   'grant_type': ding_can_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 订餐用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            自定义登录状态 = {
                '描述': '未注册手机号',
                'countries': [''],
                'countries2': [''],
                'countries3': [''],
                'chang_suo_lou_yu_zong_dong_shu': '',
                'xian_chang_jing_du': '',
                'xian_chang_wei_du': '',
                'lou_yu_ceng_shu': '',
                'di_xia_shi_ceng_shu': '',
                'dian_ti_shu_liang': '',
                'dx_xia_zai': '',
                'dx_shang_chuang': '',
                'yd_xia_zai': '',
                'yd_shang_chuang': '',
                'shi_fou_you_di_xia_ting_cha_chang': False,
                'shi_fou_you_yi_wang_shi_feng': False,
                'shi_fou_you_yi_kan_cha': False
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        抽奖主界面表first = 订餐主界面表.objects(手机号=用户.手机号).first()
        if 抽奖主界面表first == None:
            四级部门 = ''
        else:
            四级部门 = 抽奖主界面表first.四级部门
        bindMenPaiHao_id = request.GET['bindMenPaiHao_id']
        bindMenPaiHao_id_list = bindMenPaiHao_id.split(菜单分隔符)
        print(bindMenPaiHao_id_list)
        订餐日期 = bindMenPaiHao_id_list[0]
        食堂名称 = bindMenPaiHao_id_list[1]
        订餐类型 = bindMenPaiHao_id_list[2]
        菜谱名称 = bindMenPaiHao_id_list[3]
        订餐菜单评价表first = 订餐菜单评价表.objects(
            订餐日期=订餐日期,
            食堂名称=食堂名称,
            订餐类型=订餐类型,
            菜谱名称=菜谱名称,
        ).first()
        if 订餐菜单评价表first == None:
            场所楼宇总栋数 = ''
            现场经度 = ''
            现场纬度 = ''
            楼宇层数 = ''
            地下室层数 = ''
            电梯数量 = ''
            电信下载速率 = ''
            电信上传速率 = ''
            移动下载速率 = ''
            移动上传速率 = ''
            shi_fou_you_di_xia_ting_cha_chang = False
            shi_fou_you_yi_wang_shi_feng = False
            shi_fou_you_yi_kan_cha = False
        else:
            场所楼宇总栋数 = ''
            现场经度 = ''
            现场纬度 = ''
            楼宇层数 = ''
            地下室层数 = ''
            电梯数量 = ''
            电信下载速率 = ''
            电信上传速率 = ''
            移动下载速率 = ''
            移动上传速率 = ''
            shi_fou_you_di_xia_ting_cha_chang = False
            shi_fou_you_yi_wang_shi_feng = False
            shi_fou_you_yi_kan_cha = False
        自定义登录状态 = {
            '描述': '成功',
            'countries': [订餐日期],
            'countries2': [食堂名称],
            'countries3': [菜谱名称],
            'chang_suo_lou_yu_zong_dong_shu': 场所楼宇总栋数,
            'xian_chang_jing_du': 现场经度,
            'xian_chang_wei_du': 现场纬度,
            'lou_yu_ceng_shu': 楼宇层数,
            'di_xia_shi_ceng_shu': 地下室层数,
            'dian_ti_shu_liang': 电梯数量,
            'dx_xia_zai': 电信下载速率,
            'dx_shang_chuang': 电信上传速率,
            'yd_xia_zai': 移动下载速率,
            'yd_shang_chuang': 移动上传速率,
            'shi_fou_you_di_xia_ting_cha_chang': shi_fou_you_di_xia_ting_cha_chang,
            'shi_fou_you_yi_wang_shi_feng': shi_fou_you_yi_wang_shi_feng,
            'shi_fou_you_yi_kan_cha': shi_fou_you_yi_kan_cha,
        }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')

def 订餐评价初始化(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': ding_can_appid, 'secret': ding_can_secret, 'js_code': js_code,
                   'grant_type': ding_can_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 订餐用户表.objects(openid=r_json['openid']).first()
        手机号 = 用户.手机号
        订餐评论表objs = 订餐评论表.objects
        ping_jia_list = []
        for 订餐评论表obj in 订餐评论表objs:
            ping_jia_dict = {
                'ping_jia_id':订餐评论表obj.创建时间,
                'biao_ti': 订餐评论表obj.手机号,
                'nei_rong':订餐评论表obj.评论内容,
                'image_url':'https://wx.wuminmin.top/ding_can_image/?obj_id='+str(订餐评论表obj.id)
                # 'image_url':'http://127.0.0.1:8000/ding_can_image/?obj_id='+str(订餐评论表obj.id)
            }
            ping_jia_list.append(ping_jia_dict)
        自定义登录状态 = {
            '描述':'成功',
            'ping_jia_list':ping_jia_list
        }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')

def 订餐上传评价(request):
    try:
        if request.method == 'GET':
            js_code = request.GET['code']
            url = 'https://api.weixin.qq.com/sns/jscode2session'
            payload = {'appid': ding_can_appid, 'secret': ding_can_secret, 'js_code': js_code,
                       'grant_type': ding_can_grant_type}
            r = requests.get(url=url, params=payload)
            r_json = json.loads(r.text)
            用户 = 订餐用户表.objects(openid=r_json['openid']).first()
            if 用户 == None:
                return HttpResponse('未注册手机号')
            订餐主界面表first = 订餐主界面表.objects(手机号=用户.手机号).first()
            if 订餐主界面表first == None:
                return HttpResponse('用户未授权')
            ping_jia_txt = request.GET['ping_jia_txt']
            print(ping_jia_txt)
            # tu_pian = request.FILES.get('file')
            # print(tu_pian)
            path = myConfig.django_root_path + '/' + 'mysite' + '/' + '404.png'
            outfile = open(path, 'rb')
            手机号 = 用户.手机号
            创建时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            订餐评论表(
                手机号=手机号,
                创建时间=创建时间,
                评论内容=ping_jia_txt,
                评论图片=outfile
            ).save()
            return HttpResponse('成功')
        if request.method == 'POST':
            js_code =  request.POST['code']
            url = 'https://api.weixin.qq.com/sns/jscode2session'
            payload = {'appid': ding_can_appid, 'secret': ding_can_secret, 'js_code': js_code,
                       'grant_type': ding_can_grant_type}
            r = requests.get(url=url, params=payload)
            r_json = json.loads(r.text)
            用户 = 订餐用户表.objects(openid=r_json['openid']).first()
            if 用户 == None:
                return HttpResponse('未注册手机号')
            订餐主界面表first = 订餐主界面表.objects(手机号=用户.手机号).first()
            if 订餐主界面表first == None:
                return HttpResponse('用户未授权')
            ping_jia_txt =  request.POST['ping_jia_txt']
            tu_pian = request.FILES.get('file')
            手机号 = 用户.手机号
            订餐评论表first = 订餐评论表.objects(
                手机号=手机号,
                评论内容=ping_jia_txt,
            ).first()
            创建时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if 订餐评论表first == None:
                订餐评论表(
                    手机号=手机号,
                    创建时间=创建时间,
                    评论内容=ping_jia_txt,
                    评论图片=tu_pian
                ).save()
                return HttpResponse('上传图片成功')
            else:
                订餐评论表first.update(
                    评论图片=tu_pian
                )
            return HttpResponse('上传图片成功')
    except:
        print(traceback.format_exc())
        return HttpResponse('上传图片失败')

def 订餐评价初始化图片(request):
    try:
        obj_id = request.GET['obj_id']
        if obj_id == '404':
            path = myConfig.django_root_path + '/' + 'mysite' + '/' + '404.png'
            outfile = open(path, 'rb')
            response = FileResponse(outfile)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="%s"' % "image.jpg"
            return response
        采集模版表first = 订餐评论表.objects(id=obj_id).first()
        if 采集模版表first == None:
            path = myConfig.django_root_path + '/' + 'mysite' + '/' + '404.png'
            outfile = open(path, 'rb')
            response = FileResponse(outfile)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="%s"' % "image.jpg"
            return response
        else:
            image = 采集模版表first.评论图片.read()
            response = HttpResponse(image)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="ano.jpg"'
            return response
    except:
        print(traceback.format_exc())
        path = myConfig.django_root_path + '/' + 'mysite' + '/' + '404.png'
        outfile = open(path, 'rb')
        response = FileResponse(outfile)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s"' % "image.jpg"
        return response


if __name__ == '__main__':
    异步计算订餐结果(' ','')


