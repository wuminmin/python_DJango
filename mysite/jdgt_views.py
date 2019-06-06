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
from myConfig import appid, secret, grant_type, django_root_path, jdgt_appid, jdgt_secret, jdgt_grant_type, sign_name, \
    template_code
from mysite.ding_can_mongo import 订餐登录状态表
from mysite.jdgt_mongo import 结对共拓食堂模版表, 结对共拓结果表, 结对共拓主界面表, 结对共拓用户表, 结对共拓登录状态表, 结对共拓验证码表, 没吃, 吃过, 中餐统计, 晚餐统计, 结对共拓核销码表, \
    取消, 结对共拓部门表, 结对共拓统计结果, 结对共拓菜单分页, 结对共拓菜单表, 菜单分隔符, 结对共拓菜单模版表, 结对共拓菜单评价表, 结对共拓客户经理表, 结对共拓客户经理上传单位信息, 结对共拓部门主任客户经理对应表, \
    结对共拓部门主任走访客户结果表,客户经理未核实, 客户经理已核实, 客户经理不通过, 政企校园完成打分, 党群部审核通过, 党群部审核不通过

from mysite.schedule_tool import 启动订餐提醒定时器


# 异步函数
def deprecated_async(f):
    def wrapper(*args, **kwargs):
        from threading import Thread
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


启动订餐提醒定时器()


def 订餐登录检查(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        查询结果 = 结对共拓用户表.objects(openid=r_json['openid']).first()
        if 查询结果 == None:
            自定义登录状态 = "{\"描述\":\"用户不存在\",\"会话\":\"\"}"
            return HttpResponse(自定义登录状态)
        else:
            r = 订餐登录状态表(session_key=r_json['session_key'], openid=r_json['openid']).save()
            自定义登录状态 = "{\"描述\":\"新界面\",\"会话\":\"" + str(r.id) + "\"}"
            return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')


def 订餐下载主界面数据(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 结对共拓用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            自定义登录状态 = {'描述': '未注册手机号', '姓名': '', '当前日期': '', '类型': ''}
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            手机号 = 用户.手机号
            print(手机号)
            主界面 = 结对共拓主界面表.objects(手机号=手机号).first()
            if 主界面 == None:
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
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        print(r_json)
        用户 = 结对共拓用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            自定义登录状态 = "{\"描述\":\"用户不存在\",\"会话\":\"" + r_json['session_key'] + "\"}"
            return HttpResponse(自定义登录状态)
        else:
            手机号 = 用户.手机号
            # 结对共拓主界面表.objects(手机号=手机号,主菜单name=主菜单name,子菜单page_name=子菜单page_name,子菜单page_desc=子菜单page_desc)
            订餐模版表_one = 结对共拓食堂模版表.objects(子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc).first()
            if 订餐模版表_one == None:
                自定义登录状态 = "{\"描述\":\"没有食堂\",\"会话\":\"" + r_json['session_key'] + "\"}"
                return HttpResponse(自定义登录状态)
            else:
                食堂地址 = 订餐模版表_one.食堂地址
                主菜单name = 订餐模版表_one.主菜单name
                用餐日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                预订开始日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                预订结束日期 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 864000))
                会话 = r_json['session_key']
                描述 = '下载成功'
                自定义登录状态 = {'描述': 描述, '会话': 会话, '预订开始日期': 预订开始日期, '预订结束日期': 预订结束日期
                    , '主菜单name': 主菜单name, '子菜单page_name': 子菜单page_name, '子菜单page_desc': 子菜单page_desc, '食堂地址': 食堂地址
                    , '用餐日期': 用餐日期}
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
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        # r_json = {'openid':'oPngn4yfqDljEh7wvTMD0NHddOOQ','session_key':'session_key'}
        当前时间戳 = time.time()
        当前时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        当前日期加一天 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400))
        当前日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        结对共拓用户表_one = 结对共拓用户表.objects(openid=r_json['openid']).first()
        手机号 = 结对共拓用户表_one.手机号
        结对共拓主界面表_first = 结对共拓主界面表.objects(手机号=手机号).first()
        食堂就餐订餐选项 = [0, 1]
        食堂就餐订餐有效选项 = [1]
        if 结对共拓用户表_one == None:
            自定义登录状态 = "{\"描述\":\"用户不存在\",\"会话\":\"\"}"
            return HttpResponse(自定义登录状态)
        else:
            中餐食堂 = request.GET['zhong_can_shi_tang']
            晚餐食堂 = request.GET['wan_can_shi_tang']
            中餐外带 = request.GET['zhong_can_wai_dai']
            晚餐外带 = request.GET['wan_can_wai_dai']
            主菜单name = request.GET['name']
            子菜单page_name = request.GET['page_name']
            子菜单page_desc = request.GET['page_desc']
            用餐日期 = request.GET['date']
            if 用餐日期 < 当前日期:
                自定义登录状态 = "{\"描述\":\"预订日期不正确\",\"会话\":\"\"}"
                return HttpResponse(自定义登录状态)
            try:
                中餐食堂 = int(中餐食堂)
                晚餐食堂 = int(晚餐食堂)
                中餐外带 = int(中餐外带)
                晚餐外带 = int(晚餐外带)
            except:
                自定义登录状态 = "{\"描述\":\"预订数量必须是数字\",\"会话\":\"\"}"
                return HttpResponse(自定义登录状态)
            手机号 = 结对共拓用户表_one.手机号
            结对共拓食堂模版表_one = 结对共拓食堂模版表.objects(主菜单name=主菜单name
                                              , 子菜单page_name=子菜单page_name
                                              , 子菜单page_desc=子菜单page_desc
                                              ).first()
            if 结对共拓食堂模版表_one == None:
                描述 = '没有食堂数据'
                自定义登录状态 = {'描述': 描述, '会话': r_json['session_key']
                           }
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
            else:
                早餐就餐时间 = 用餐日期 + ' ' + 结对共拓食堂模版表_one.早餐就餐时间
                中餐就餐时间 = 用餐日期 + ' ' + 结对共拓食堂模版表_one.中餐就餐时间
                晚餐就餐时间 = 用餐日期 + ' ' + 结对共拓食堂模版表_one.晚餐就餐时间
                预定早餐提前秒 = 结对共拓食堂模版表_one.预定早餐提前秒
                预定中餐提前秒 = 结对共拓食堂模版表_one.预定中餐提前秒
                预定晚餐提前秒 = 结对共拓食堂模版表_one.预定晚餐提前秒
                取消早餐提前秒 = 结对共拓食堂模版表_one.取消早餐提前秒
                取消中餐提前秒 = 结对共拓食堂模版表_one.取消中餐提前秒
                取消晚餐提前秒 = 结对共拓食堂模版表_one.取消晚餐提前秒
                预定中餐提前截止时间 = time.mktime(time.strptime(中餐就餐时间, "%Y-%m-%d %H:%M:%S")) - 预定中餐提前秒
                预定晚餐提前截止时间 = time.mktime(time.strptime(晚餐就餐时间, "%Y-%m-%d %H:%M:%S")) - 预定晚餐提前秒

                结对共拓结果表_one = 结对共拓结果表.objects(手机号=手机号, 主菜单name=主菜单name, 子菜单page_name=子菜单page_name
                                              , 子菜单page_desc=子菜单page_desc, 用餐日期=用餐日期).first()
                # if 结对共拓结果表_one == None:
                中餐食堂就餐预订数 = 0
                中餐食堂外带预订数 = 0
                晚餐食堂就餐预订数 = 0
                晚餐食堂外带预订数 = 0
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
                if 中餐食堂就餐预订数 == 0 and 中餐食堂外带预订数 == 0 and 晚餐食堂就餐预订数 == 0 and 晚餐食堂外带预订数 == 0:
                    自定义登录状态 = "{\"描述\":\"至少选择一项订餐\",\"会话\":\"\"}"
                    return HttpResponse(自定义登录状态)
                else:
                    if 结对共拓结果表_one == None:
                        中餐食堂就餐签到 = ''
                        中餐订餐时间 = ''
                        晚餐食堂就餐签到 = ''
                        晚餐订餐时间 = ''
                        if 中餐食堂就餐预订数 == 1:
                            中餐食堂就餐签到 = 没吃
                            中餐订餐时间 = 当前时间
                        if 晚餐食堂就餐预订数 == 1:
                            晚餐食堂就餐签到 = 没吃
                            晚餐订餐时间 = 当前时间
                        结对共拓结果表(
                            手机号=手机号,
                            主菜单name=主菜单name,
                            子菜单page_name=子菜单page_name,
                            子菜单page_desc=子菜单page_desc,
                            用餐日期=用餐日期,
                            #
                            中餐食堂就餐预订数=中餐食堂就餐预订数,
                            中餐食堂就餐签到=中餐食堂就餐签到,
                            中餐订餐时间=中餐订餐时间,
                            #
                            晚餐食堂就餐预订数=晚餐食堂就餐预订数,
                            晚餐食堂就餐签到=晚餐食堂就餐签到,
                            晚餐订餐时间=晚餐订餐时间
                        ).save()
                        结对共拓结果表_first = 结对共拓结果表.objects(手机号=手机号, 主菜单name=主菜单name, 子菜单page_name=子菜单page_name
                                                        , 子菜单page_desc=子菜单page_desc, 用餐日期=用餐日期).first()
                        描述 = '上传成功'
                        订餐结果描述 = '中餐食堂就餐预订数' + str(结对共拓结果表_first.中餐食堂就餐预订数) \
                                 + ',晚餐食堂就餐预订数' + str(结对共拓结果表_first.晚餐食堂就餐预订数) \
                                 + ',中餐食堂外带预订数' + str(结对共拓结果表_first.中餐食堂外带预订数) \
                                 + ',晚餐食堂外带预订数' + str(结对共拓结果表_first.晚餐食堂外带预订数)
                        自定义登录状态 = {'描述': 描述, '会话': r_json['session_key']
                            , '订餐结果描述': 订餐结果描述}
                        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                        自定义登录状态 = str(自定义登录状态)
                        异步计算订餐结果(子菜单page_name, 结对共拓主界面表_first.二级部门)
                        return HttpResponse(自定义登录状态)
                    else:
                        if 中餐食堂就餐预订数 == 1:
                            if 结对共拓结果表_one.中餐食堂就餐预订数 == 1:
                                自定义登录状态 = "{\"描述\":\"不能重复订餐\",\"会话\":\"\"}"
                                return HttpResponse(自定义登录状态)
                            else:
                                结对共拓结果表_one.update(
                                    中餐食堂就餐预订数=中餐食堂就餐预订数,
                                    中餐食堂就餐签到=没吃,
                                    中餐订餐时间=当前时间,
                                    中餐取消时间=''
                                )
                        if 晚餐食堂就餐预订数 == 1:
                            if 结对共拓结果表_one.晚餐食堂就餐预订数 == 1:
                                自定义登录状态 = "{\"描述\":\"不能重复订餐\",\"会话\":\"\"}"
                                return HttpResponse(自定义登录状态)
                            else:
                                结对共拓结果表_one.update(
                                    晚餐食堂就餐预订数=晚餐食堂就餐预订数,
                                    晚餐食堂就餐签到=没吃,
                                    晚餐订餐时间=当前时间,
                                    晚餐取消时间=''
                                )

                        结对共拓结果表_first = 结对共拓结果表.objects(手机号=手机号, 主菜单name=主菜单name, 子菜单page_name=子菜单page_name
                                                        , 子菜单page_desc=子菜单page_desc, 用餐日期=用餐日期).first()
                        描述 = '上传成功'
                        订餐结果描述 = '中餐食堂就餐预订数' + str(结对共拓结果表_first.中餐食堂就餐预订数) \
                                 + ',晚餐食堂就餐预订数' + str(结对共拓结果表_first.晚餐食堂就餐预订数) \
                                 + ',中餐食堂外带预订数' + str(结对共拓结果表_first.中餐食堂外带预订数) \
                                 + ',晚餐食堂外带预订数' + str(结对共拓结果表_first.晚餐食堂外带预订数)
                        自定义登录状态 = {'描述': 描述, '会话': r_json['session_key']
                            , '订餐结果描述': 订餐结果描述}
                        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                        自定义登录状态 = str(自定义登录状态)
                        异步计算订餐结果(子菜单page_name, 结对共拓主界面表_first.二级部门)
                        return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')


def 订餐校验验证码(request):
    手机号 = str(request.GET['phone'])
    验证码 = str(request.GET['sms_code'])
    js_code = request.GET['code']
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
               'grant_type': jdgt_grant_type}
    r = requests.get(url=url, params=payload)
    r_json = json.loads(r.text)
    openid = r_json['openid']
    r = 结对共拓验证码表.objects(手机号=手机号)
    for rr in r:
        if rr.验证码 == 验证码:
            结对共拓用户表(手机号=手机号, openid=openid).save()
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
                r = 结对共拓验证码表(验证码=验证码, 手机号=手机号).save()
            return HttpResponse(r2['Code'])
    except:
        return HttpResponse('500')


@deprecated_async
def 异步计算订餐结果(子菜单page_name, 二级部门):
    第一天 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    第二天 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400))
    日期_list = [第一天, 第二天]
    for 日期_list_one in 日期_list:
        日期 = 日期_list_one
        子菜单page_name = 子菜单page_name
        子菜单page_desc_list = ['中餐统计', '晚餐统计']
        for 子菜单page_desc_list_one in 子菜单page_desc_list:
            子菜单page_desc = 子菜单page_desc_list_one
            结对共拓部门表_first = 结对共拓部门表.objects(二级部门=二级部门).first()
            if 结对共拓部门表_first == None:
                name_list = []
            else:
                name_list = 结对共拓部门表_first.三级部门列表
            if 子菜单page_desc == 中餐统计:
                结对共拓结果表_all = 结对共拓结果表.objects(子菜单page_name=子菜单page_name, 中餐食堂就餐预订数=1, 用餐日期=日期)
                总人数 = len(list(结对共拓结果表_all))
                没吃人数 = len(list(结对共拓结果表.objects(子菜单page_name=子菜单page_name, 中餐食堂就餐预订数=1, 用餐日期=日期, 中餐食堂就餐签到=没吃)))
                吃过人数 = len(list(结对共拓结果表.objects(子菜单page_name=子菜单page_name, 中餐食堂就餐预订数=1, 用餐日期=日期, 中餐食堂就餐签到=吃过)))
            elif 子菜单page_desc == 晚餐统计:
                结对共拓结果表_all = 结对共拓结果表.objects(子菜单page_name=子菜单page_name, 晚餐食堂就餐预订数=1, 用餐日期=日期)
                总人数 = len(list(结对共拓结果表_all))
                没吃人数 = len(list(结对共拓结果表.objects(子菜单page_name=子菜单page_name, 晚餐食堂就餐预订数=1, 用餐日期=日期, 晚餐食堂就餐签到=没吃)))
                吃过人数 = len(list(结对共拓结果表.objects(子菜单page_name=子菜单page_name, 晚餐食堂就餐预订数=1, 用餐日期=日期, 晚餐食堂就餐签到=吃过)))
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
                for 结对共拓结果表_one in 结对共拓结果表_all:
                    结对共拓主界面表_first = 结对共拓主界面表.objects(手机号=结对共拓结果表_one.手机号, 三级部门=name_one).first()
                    if 结对共拓主界面表_first == None:
                        continue
                    else:
                        rr_dict = {}
                        rr_dict['page_name'] = 结对共拓主界面表_first.姓名
                        if 子菜单page_desc == 中餐统计:
                            rr_dict['page_desc'] = 结对共拓结果表_one.中餐食堂就餐签到
                        else:
                            rr_dict['page_desc'] = 结对共拓结果表_one.晚餐食堂就餐签到
                        pages.append(rr_dict)
                r_dict['num'] = len(pages)
                r_dict['pages'] = pages
                r_list.append(r_dict)
            描述 = '下载成功'
            if 子菜单page_desc == 中餐统计:
                app_tittle = '中餐统计'
            else:
                app_tittle = '晚餐统计'
            app_des = '总人数 ' + str(总人数)
            app_code_des = '吃过 ' + str(吃过人数)
            app_code = '没吃过 ' + str(没吃人数)
            start_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            end_date = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400))
            自定义登录状态 = {'描述': 描述, '会话': '23456', 'list': r_list, 'app_tittle': app_tittle, 'app_des': app_des
                , 'app_code_des': app_code_des, 'app_code': app_code, 'date': 日期, 'start_date': start_date,
                       'end_date': end_date
                       }
            结对共拓统计结果_first = 结对共拓统计结果.objects(日期=日期, 子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc).first()
            if 结对共拓统计结果_first == None:
                结对共拓统计结果(日期=日期, 子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc, 订餐结果=自定义登录状态).save()
            else:
                结对共拓统计结果_first.update(订餐结果=自定义登录状态)
    print('异步计算完成', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


def 订餐统计中餐(request):
    日期 = str(request.GET['date'])
    子菜单page_name = str(request.GET['page_name'])
    子菜单page_desc = str(request.GET['page_desc'])
    if 日期 == '':
        日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    结对共拓统计结果_first = 结对共拓统计结果.objects(日期=日期, 子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc).first()
    if 结对共拓统计结果_first == None:
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
        自定义登录状态 = 结对共拓统计结果_first.订餐结果
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
    订餐中餐核销码表_first = 结对共拓核销码表.objects(主菜单name=主菜单name, 子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc).first()
    if 订餐中餐核销码表_first == None:
        if 子菜单page_desc == '中餐核销码':
            结对共拓核销码表(主菜单name=主菜单name, 子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc, 核销码='123456').save()
            自定义登录状态 = {'核销码': '123456', '手机号': '无', '二级部门': '无', '三级部门': '无', '四级部门': '无', '姓名': '无'}
        elif 子菜单page_desc == '晚餐核销码':
            结对共拓核销码表(主菜单name=主菜单name, 子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc, 核销码='123456').save()
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
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        session_key = r_json['session_key']
        openid = r_json['openid']
        结对共拓用户表_first = 结对共拓用户表.objects(openid=openid).first()
        if 结对共拓用户表_first == None:
            自定义登录状态 = {'描述': '未注册手机号', '姓名': '', '当前日期': '', '类型': ''}
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        手机号 = 结对共拓用户表_first.手机号
        结对共拓主界面表_first = 结对共拓主界面表.objects(手机号=手机号).first()
        # 结对共拓结果表_first = 结对共拓结果表.objects(主菜单name=主菜单name, 子菜单page_name=子菜单page_name, 手机号=手机号, 用餐日期=当前日期).first()
        结对共拓结果表_first = 结对共拓结果表.objects(手机号=手机号, 用餐日期=当前日期).first()
        if 结对共拓结果表_first == None:
            自定义登录状态 = {'描述': '没有订餐', '姓名': '', '当前日期': '', '类型': ''}
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            if 子菜单page_name == '' or 子菜单page_name == None:
                子菜单page_name = 结对共拓结果表_first.子菜单page_name
            if 当前小时 > '10' and 当前小时 < '15':
                if 结对共拓结果表_first.中餐食堂就餐签到 == 没吃:
                    结对共拓结果表_first.update(中餐食堂就餐签到=吃过)
                    自定义登录状态 = {'描述': '成功', '姓名': 结对共拓主界面表_first.姓名, '当前日期': 当前日期, '类型': '中餐核销'}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    异步计算订餐结果(子菜单page_name, 结对共拓主界面表_first.二级部门)
                    return HttpResponse(自定义登录状态)
                elif 结对共拓结果表_first.中餐食堂就餐签到 == 吃过:
                    自定义登录状态 = {'描述': '成功', '姓名': 结对共拓主界面表_first.姓名, '当前日期': 当前日期, '类型': '中餐核销'}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                else:
                    自定义登录状态 = {'描述': '已经吃过或者已取消', '姓名': '', '当前日期': '', '类型': ''}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
            elif 当前小时 > '16' and 当前小时 < '20':
                if 结对共拓结果表_first.晚餐食堂就餐签到 == 没吃:
                    结对共拓结果表_first.update(晚餐食堂就餐签到=吃过)
                    自定义登录状态 = {'描述': '成功', '姓名': 结对共拓主界面表_first.姓名, '当前日期': 当前日期, '类型': '晚餐核销'}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    异步计算订餐结果(子菜单page_name, 结对共拓主界面表_first.二级部门)
                    return HttpResponse(自定义登录状态)
                elif 结对共拓结果表_first.晚餐食堂就餐签到 == 吃过:
                    自定义登录状态 = {'描述': '成功', '姓名': 结对共拓主界面表_first.姓名, '当前日期': 当前日期, '类型': '晚餐核销'}
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
    结对共拓核销码表_first = 结对共拓核销码表.objects(主菜单name=主菜单name, 子菜单page_name=子菜单page_name, 核销码=核销码).first()
    if 结对共拓核销码表_first == None:
        自定义登录状态 = {'描述': '二维码已过期'}
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)
    else:
        当前日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        session_key = r_json['session_key']
        openid = r_json['openid']
        结对共拓用户表_first = 结对共拓用户表.objects(openid=openid).first()
        手机号 = 结对共拓用户表_first.手机号
        结对共拓主界面表_first = 结对共拓主界面表.objects(手机号=手机号).first()
        结对共拓结果表_first = 结对共拓结果表.objects(主菜单name=主菜单name, 子菜单page_name=子菜单page_name, 手机号=手机号, 用餐日期=当前日期).first()
        if 结对共拓结果表_first == None:
            自定义登录状态 = {'描述': '没有订餐'}
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            if 结对共拓核销码表_first.子菜单page_desc == '中餐核销码':
                if 结对共拓结果表_first.中餐食堂就餐签到 == 没吃:
                    结对共拓结果表_first.update(中餐食堂就餐签到=吃过)
                    结对共拓核销码表_first.update(核销码=session_key
                                          , 手机号=手机号, 二级部门=结对共拓主界面表_first.二级部门
                                          , 三级部门=结对共拓主界面表_first.三级部门, 四级部门=结对共拓主界面表_first.四级部门
                                          , 姓名=结对共拓主界面表_first.姓名
                                          )
                    自定义登录状态 = {'描述': '成功', '姓名': 结对共拓主界面表_first.姓名, '当前日期': 当前日期, '类型': '中餐核销'}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                else:
                    自定义登录状态 = {'描述': '已经吃过了'}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
            elif 结对共拓核销码表_first.子菜单page_desc == '晚餐核销码':
                if 结对共拓结果表_first.晚餐食堂就餐签到 == 没吃:
                    结对共拓结果表_first.update(晚餐食堂就餐签到=吃过)
                    结对共拓核销码表_first.update(核销码=session_key
                                          , 手机号=手机号, 二级部门=结对共拓主界面表_first.二级部门
                                          , 三级部门=结对共拓主界面表_first.三级部门, 四级部门=结对共拓主界面表_first.四级部门
                                          , 姓名=结对共拓主界面表_first.姓名)
                    自定义登录状态 = {'描述': '成功', '姓名': 结对共拓主界面表_first.姓名, '当前日期': 当前日期, '类型': '晚餐核销'}
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
    订餐中餐核销码表_first = 结对共拓核销码表.objects(子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc).first()
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
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        当前日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        if 日期 == '':
            日期 = 当前日期
        开始日期 = time.strftime('%Y-%m-%d', time.localtime(time.time() - 864000))
        结束日期 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 864000))
        结对共拓用户表_one = 结对共拓用户表.objects(openid=r_json['openid']).first()
        if 结对共拓用户表_one == None:
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
            手机号 = 结对共拓用户表_one.手机号
            结对共拓结果表_first = 结对共拓结果表.objects(手机号=手机号, 用餐日期=日期).first()
            if 结对共拓结果表_first == None:
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
                结对共拓主界面表_first = 结对共拓主界面表.objects(手机号=手机号).first()
                结对共拓食堂模版表_first = 结对共拓食堂模版表.objects(子菜单page_name=page_name).first()
                if 结对共拓食堂模版表_first == None:
                    描述 = '没有食堂数据'
                    自定义登录状态 = {'描述': 描述, '会话': r_json['session_key']}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                if 结对共拓主界面表_first == None:
                    描述 = '您没有权限'
                    自定义登录状态 = {'描述': 描述, '会话': r_json['session_key']}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                描述 = '下载成功'
                自定义登录状态 = {'描述': 描述, '会话': r_json['session_key'],
                           '主菜单name': 结对共拓结果表_first.主菜单name,
                           '子菜单page_name': 结对共拓结果表_first.子菜单page_name,
                           '子菜单page_desc': 结对共拓结果表_first.子菜单page_desc,
                           '姓名': 结对共拓主界面表_first.姓名,
                           '食堂地址': 结对共拓食堂模版表_first.食堂地址,
                           '日期': 日期,
                           '开始日期': 开始日期,
                           '结束日期': 结束日期,
                           '中餐食堂就餐预订数': 结对共拓结果表_first.中餐食堂就餐预订数,
                           '中餐价格': 结对共拓食堂模版表_first.中餐价格,
                           '中餐食堂就餐签到': 结对共拓结果表_first.中餐食堂就餐签到,
                           '中餐订餐时间': 结对共拓结果表_first.中餐订餐时间,
                           '中餐取消时间': 结对共拓结果表_first.中餐取消时间,
                           '晚餐食堂就餐预订数': 结对共拓结果表_first.晚餐食堂就餐预订数,
                           '晚餐食堂就餐签到': 结对共拓结果表_first.晚餐食堂就餐签到,
                           '晚餐价格': 结对共拓食堂模版表_first.晚餐价格,
                           '晚餐订餐时间': 结对共拓结果表_first.晚餐订餐时间,
                           '晚餐取消时间': 结对共拓结果表_first.晚餐取消时间
                           }
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')


def 订餐取消(request):
    try:
        取消中餐 = request.GET['qu_xiao_zhong_can_flag']
        取消晚餐 = request.GET['qu_xiao_wan_can_flag']
        page_name = request.GET['page_name']
        日期 = request.GET['date']
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
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
        结对共拓用户表_one = 结对共拓用户表.objects(openid=r_json['openid']).first()
        if 结对共拓用户表_one == None:
            自定义登录状态 = "{\"描述\":\"用户不存在\",\"会话\":\"\"}"
            return HttpResponse(自定义登录状态)
        else:
            手机号 = 结对共拓用户表_one.手机号
            结对共拓结果表_first = 结对共拓结果表.objects(手机号=手机号, 用餐日期=日期).first()
            if 结对共拓结果表_first == None:
                描述 = '没有订餐记录'
                自定义登录状态 = {'描述': 描述, '会话': r_json['session_key']}
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
            else:
                结对共拓主界面表_first = 结对共拓主界面表.objects(手机号=手机号).first()
                结对共拓食堂模版表_first = 结对共拓食堂模版表.objects(子菜单page_name=page_name).first()
                if 结对共拓食堂模版表_first == None:
                    描述 = '没有食堂数据'
                    自定义登录状态 = {'描述': 描述, '会话': r_json['session_key']}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                if 结对共拓主界面表_first == None:
                    描述 = '您没有权限'
                    自定义登录状态 = {'描述': 描述, '会话': r_json['session_key']}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                描述 = '至少选择取消一项'

                早餐就餐时间 = 日期 + ' ' + 结对共拓食堂模版表_first.早餐就餐时间
                中餐就餐时间 = 日期 + ' ' + 结对共拓食堂模版表_first.中餐就餐时间
                晚餐就餐时间 = 日期 + ' ' + 结对共拓食堂模版表_first.晚餐就餐时间
                预定早餐提前秒 = 结对共拓食堂模版表_first.预定早餐提前秒
                预定中餐提前秒 = 结对共拓食堂模版表_first.预定中餐提前秒
                预定晚餐提前秒 = 结对共拓食堂模版表_first.预定晚餐提前秒
                取消早餐提前秒 = 结对共拓食堂模版表_first.取消早餐提前秒
                取消中餐提前秒 = 结对共拓食堂模版表_first.取消中餐提前秒
                取消晚餐提前秒 = 结对共拓食堂模版表_first.取消晚餐提前秒
                取消中餐提前截止时间 = time.mktime(time.strptime(中餐就餐时间, "%Y-%m-%d %H:%M:%S")) - 取消中餐提前秒
                取消晚餐提前截止时间 = time.mktime(time.strptime(晚餐就餐时间, "%Y-%m-%d %H:%M:%S")) - 取消晚餐提前秒
                if 取消中餐 == 'true':
                    if 结对共拓结果表_first.中餐食堂就餐签到 != 取消:
                        if 结对共拓结果表_first.中餐食堂就餐预订数 == 1:
                            if 当前时间戳 < 取消中餐提前截止时间:
                                if 结对共拓结果表_first.中餐食堂就餐签到 == 没吃:
                                    结对共拓结果表_first.update(中餐食堂就餐预订数=0, 中餐食堂就餐签到=取消, 中餐取消时间=当前时间)
                                    异步计算订餐结果(page_name, 结对共拓主界面表_first.二级部门)
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
                    if 结对共拓结果表_first.晚餐食堂就餐签到 != 取消:
                        if 结对共拓结果表_first.晚餐食堂就餐预订数 == 1:
                            if 当前时间戳 < 取消晚餐提前截止时间:
                                if 结对共拓结果表_first.晚餐食堂就餐签到 == 没吃:
                                    结对共拓结果表_first.update(晚餐食堂就餐预订数=0, 晚餐食堂就餐签到=取消, 晚餐取消时间=当前时间)
                                    异步计算订餐结果(page_name, 结对共拓主界面表_first.二级部门)
                                    描述 = '晚餐取消成功'
                                else:
                                    描述 = '晚餐已吃过，不能取消'
                            else:
                                描述 = '已超过截止时间，不能取消'
                        else:
                            描述 = '晚餐未预定，不能取消'
                    else:
                        描述 = '晚餐已取消，不能重复操作'
                结对共拓结果表_second = 结对共拓结果表.objects(手机号=手机号, 用餐日期=日期).first()
                自定义登录状态 = {'描述': 描述, '会话': r_json['session_key'],
                           '主菜单name': 结对共拓结果表_second.主菜单name,
                           '子菜单page_name': 结对共拓结果表_second.子菜单page_name,
                           '子菜单page_desc': 结对共拓结果表_second.子菜单page_desc,
                           '姓名': 结对共拓主界面表_first.姓名,
                           '食堂地址': 结对共拓食堂模版表_first.食堂地址,
                           '日期': 日期,
                           '开始日期': 开始日期,
                           '结束日期': 结束日期,
                           '中餐食堂就餐预订数': 结对共拓结果表_second.中餐食堂就餐预订数,
                           '中餐价格': 结对共拓食堂模版表_first.中餐价格,
                           '中餐食堂就餐签到': 结对共拓结果表_second.中餐食堂就餐签到,
                           '中餐订餐时间': 结对共拓结果表_second.中餐订餐时间,
                           '中餐取消时间': 结对共拓结果表_second.中餐取消时间,
                           '晚餐食堂就餐预订数': 结对共拓结果表_second.晚餐食堂就餐预订数,
                           '晚餐食堂就餐签到': 结对共拓结果表_second.晚餐食堂就餐签到,
                           '晚餐价格': 结对共拓食堂模版表_first.晚餐价格,
                           '晚餐订餐时间': 结对共拓结果表_second.晚餐订餐时间,
                           '晚餐取消时间': 结对共拓结果表_second.晚餐取消时间
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
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 结对共拓用户表.objects(openid=r_json['openid']).first()
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
        主界面表first = 结对共拓主界面表.objects(手机号=用户.手机号).first()
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
        结对共拓菜单表first = 结对共拓菜单表.objects(
            食堂名称=page_name
        ).first()
        if 结对共拓菜单表first == None:
            分工list = [
                {
                    'dan_yuan_id': 0,
                    'dan_yuan_name': '2019-03-31_市公司食堂_中餐',
                    'dan_yuan': [
                        {
                            'lou_ceng_id': 0,
                            'ceng': [
                                {
                                    'men_pai_id': '2019-03-31_市公司食堂_中餐_青菜',
                                    'men_pai_hao': '青菜',
                                    'zhuang_tai': 'placeholder_grey'
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
            分工list = 结对共拓菜单表first.菜单列表
        分工list_len = len(分工list)
        分工list_len_取整除 = 分工list_len // 结对共拓菜单分页
        分工list_len_取整除 = 分工list_len_取整除 + 1
        countries = list(range(0, 分工list_len_取整除))
        countries_val = 0
        分工list_slice = 分工list[countries_val * 结对共拓菜单分页: (countries_val + 1) * 结对共拓菜单分页]
        自定义登录状态 = {
            '描述': '成功',
            'name': name,
            'page_name': page_name,
            'page_desc': page_desc,
            'countries': countries,
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
        countries_val = int(request.GET['countries_val'])

        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 结对共拓用户表.objects(openid=r_json['openid']).first()
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
        主界面表first = 结对共拓主界面表.objects(手机号=用户.手机号).first()
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
        录入分工表first = 结对共拓菜单表.objects(
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
        分工list_slice = 分工list[countries_val * 结对共拓菜单分页: (countries_val + 1) * 结对共拓菜单分页]
        自定义登录状态 = {
            '描述': '成功',
            'name': name,
            'page_name': page_name,
            'page_desc': page_desc,
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
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 结对共拓用户表.objects(openid=r_json['openid']).first()
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
        抽奖主界面表first = 结对共拓主界面表.objects(手机号=用户.手机号).first()
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
        结对共拓菜单评价表first = 结对共拓菜单评价表.objects(
            订餐日期=订餐日期,
            食堂名称=食堂名称,
            订餐类型=订餐类型,
            菜谱名称=菜谱名称,
        ).first()
        if 结对共拓菜单评价表first == None:
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
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 结对共拓用户表.objects(openid=r_json['openid']).first()
        自定义登录状态 = {
            'ping_jia_list': [
                {
                    'ping_jia_id': '0',
                    'biao_ti': '张三',
                    'nei_rong': '今天中餐还可以，肉好',
                },
                {
                    'ping_jia_id': '1',
                    'biao_ti': '李四',
                    'nei_rong': '今天晚餐不好，饭不熟',
                },
                {
                    'ping_jia_id': '2',
                    'biao_ti': '王五',
                    'nei_rong': '黄鱼烧焦了',
                },
            ]
        }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)
    except:
        return HttpResponse('500')


def 订餐上传评价(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 结对共拓用户表.objects(openid=r_json['openid']).first()
        自定义登录状态 = {
            'ping_jia_list': [
                {
                    'ping_jia_id': '0',
                    'biao_ti': '张三',
                    'nei_rong': '今天中餐还可以，肉好',
                },
                {
                    'ping_jia_id': '1',
                    'biao_ti': '李四',
                    'nei_rong': '今天晚餐不好，饭不熟',
                },
                {
                    'ping_jia_id': '2',
                    'biao_ti': '王五',
                    'nei_rong': '黄鱼烧焦了',
                },
            ]
        }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)
    except:
        return HttpResponse('500')


if __name__ == '__main__':
    异步计算订餐结果(' ', '')

def 客户经理上报单位信息(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)

        用户 = 结对共拓用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            自定义登录状态 = {
                '描述': '该用户未注册'
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            print(用户.手机号)
            print(request.GET['dan_wei_ming_cheng'])
            print(request.GET['ke_hu_bian_ma'])
            print(request.GET['ke_hu_jing_li'])
            print(request.GET['shou_ji_hao_ma'])
            dan_wei_ming_cheng = request.GET['dan_wei_ming_cheng']
            ke_hu_bian_ma = request.GET['ke_hu_bian_ma']
            ke_hu_jing_li = request.GET['ke_hu_jing_li']
            shou_ji_hao_ma = request.GET['shou_ji_hao_ma']
            结对共拓客户经理上传单位信息first = 结对共拓客户经理上传单位信息.objects(
                客户编码=ke_hu_bian_ma
            ).first()
            if 结对共拓客户经理上传单位信息first == None:
                结对共拓客户经理上传单位信息(
                    单位名称=dan_wei_ming_cheng,
                    客户编码=ke_hu_bian_ma,
                    客户经理=ke_hu_jing_li,
                    手机号码=shou_ji_hao_ma,
                ).save()
            else:
                结对共拓客户经理上传单位信息first.update(
                    单位名称=dan_wei_ming_cheng,
                    客户编码=ke_hu_bian_ma,
                    客户经理=ke_hu_jing_li,
                    手机号码=shou_ji_hao_ma,
                )

            结果表 = {
                '描述': '上传成功',
            }
            结果表 = json.dumps(结果表).encode('utf-8').decode('unicode_escape')
            结果表 = str(结果表)
            return HttpResponse(结果表)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')


def 部门主任选择客户经理初始化(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)

        用户 = 结对共拓用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            自定义登录状态 = {
                '描述': '该用户未注册'
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            结对共拓部门主任客户经理对应表objs = 结对共拓部门主任客户经理对应表.objects(
                部门主任手机号码=用户.手机号
            )
            print(结对共拓部门主任客户经理对应表objs)
            if list(结对共拓部门主任客户经理对应表objs) == []:
                自定义登录状态 = {
                    '描述': '没有关联客户经理'
                }
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
            countries = []
            for 结对共拓部门主任客户经理对应表obj in 结对共拓部门主任客户经理对应表objs:
                姓名 = 结对共拓主界面表.objects(
                    手机号=结对共拓部门主任客户经理对应表obj.客户经理手机号码
                ).first().姓名
                countries.append(姓名)
            结果表 = {
                '描述': '成功',
                'countries': countries
            }
            结果表 = json.dumps(结果表).encode('utf-8').decode('unicode_escape')
            结果表 = str(结果表)
            return HttpResponse(结果表)
    except:
        print(traceback.format_exc())
        结果表 = {
            '描述': '系统错误',
        }
        结果表 = json.dumps(结果表).encode('utf-8').decode('unicode_escape')
        结果表 = str(结果表)
        return HttpResponse(结果表)


def 部门主任选择单位初始化(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)

        用户 = 结对共拓用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            自定义登录状态 = {
                '描述': '该用户未注册'
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            countries_val = request.GET['countries_val']
            结对共拓客户经理上传单位信息objs = 结对共拓客户经理上传单位信息.objects(
                客户经理=countries_val
            )
            if list(结对共拓客户经理上传单位信息objs) == []:
                自定义登录状态 = {
                    '描述': '没有关联客户单位'
                }
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
            countries2 = []
            for 结对共拓客户经理上传单位信息obj in 结对共拓客户经理上传单位信息objs:
                countries2.append(结对共拓客户经理上传单位信息obj.单位名称)
            结果表 = {
                '描述': '成功',
                'countries2': countries2
            }
            结果表 = json.dumps(结果表).encode('utf-8').decode('unicode_escape')
            结果表 = str(结果表)
            return HttpResponse(结果表)
    except:
        print(traceback.format_exc())
        结果表 = {
            '描述': '系统错误',
        }
        结果表 = json.dumps(结果表).encode('utf-8').decode('unicode_escape')
        结果表 = str(结果表)
        return HttpResponse(结果表)


def 部门主任上传数据(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 结对共拓用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            自定义登录状态 = {
                '描述': '该用户未注册'
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            countries_val = request.GET['countries_val']
            countries2_val = request.GET['countries2_val']
            chang_suo_lou_yu_zong_dong_shu = request.GET['chang_suo_lou_yu_zong_dong_shu']
            lou_yu_ceng_shu = request.GET['lou_yu_ceng_shu']
            di_xia_shi_ceng_shu = request.GET['di_xia_shi_ceng_shu']
            dian_ti_shu_liang = request.GET['dian_ti_shu_liang']
            dx_xia_zai = request.GET['dx_xia_zai']
            shi_fou_you_di_xia_ting_cha_chang = request.GET['shi_fou_you_di_xia_ting_cha_chang']
            shi_fou_you_yi_wang_shi_feng = request.GET['shi_fou_you_yi_wang_shi_feng']
            当前日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            结对共拓主界面表first = 结对共拓主界面表.objects(
                手机号=用户.手机号,
            ).first()
            结对共拓部门主任走访客户结果表first = 结对共拓部门主任走访客户结果表.objects(
                走访日期=当前日期,
                部门主任姓名=结对共拓主界面表first.姓名,
                单位名称=countries2_val
            ).first()
            if shi_fou_you_di_xia_ting_cha_chang == 'true':
                shi_fou_you_di_xia_ting_cha_chang = True
            else:
                shi_fou_you_di_xia_ting_cha_chang = False
            if shi_fou_you_yi_wang_shi_feng == 'true':
                shi_fou_you_yi_wang_shi_feng = True
            else:
                shi_fou_you_yi_wang_shi_feng = False
            if 结对共拓部门主任走访客户结果表first == None:
                结对共拓部门主任走访客户结果表(
                    走访日期=当前日期,
                    部门主任姓名=结对共拓主界面表first.姓名,
                    客户经理姓名=countries_val,
                    单位名称=countries2_val,
                    走访主题=chang_suo_lou_yu_zong_dong_shu,
                    走访对象={'走访对象': lou_yu_ceng_shu},
                    商机信息={'商机信息': di_xia_shi_ceng_shu},
                    竞争信息={'竞争信息': dian_ti_shu_liang},
                    服务问题={'服务问题': dx_xia_zai},
                    是否有服务问题=shi_fou_you_di_xia_ting_cha_chang,
                    是否提交云方案=shi_fou_you_yi_wang_shi_feng,
                    状态=客户经理未核实,
                ).save()
                描述 = '成功'
            else:
                if 结对共拓部门主任走访客户结果表first.状态 in [客户经理未核实,客户经理不通过,党群部审核不通过]:
                    结对共拓部门主任走访客户结果表first.update(
                        走访日期=当前日期,
                        部门主任姓名=结对共拓主界面表first.姓名,
                        客户经理姓名=countries_val,
                        单位名称=countries2_val,
                        走访主题=chang_suo_lou_yu_zong_dong_shu,
                        走访对象={'走访对象': lou_yu_ceng_shu},
                        商机信息={'商机信息': di_xia_shi_ceng_shu},
                        竞争信息={'竞争信息': dian_ti_shu_liang},
                        服务问题={'服务问题': dx_xia_zai},
                        是否有服务问题=shi_fou_you_di_xia_ting_cha_chang,
                        是否提交云方案=shi_fou_you_yi_wang_shi_feng,
                        状态 = 客户经理未核实,
                    )
                    描述 = '成功'
                else:
                    描述 = 结对共拓部门主任走访客户结果表first.状态
            自定义登录状态 = {
                '描述': 描述 ,
                '会话': '',
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        结果表 = {
            '描述': '系统错误',
        }
        结果表 = json.dumps(结果表).encode('utf-8').decode('unicode_escape')
        结果表 = str(结果表)
        return HttpResponse(结果表)


def 部门主任上传图片(request):
    try:
        js_code = request.POST['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 结对共拓用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            描述 = '该用户未注册'
        else:
            countries_val = request.POST['countries_val']
            countries2_val = request.POST['countries2_val']
            import os
            from django.core.files.storage import default_storage
            from django.core.files.base import ContentFile
            from django.conf import settings
            data = request.FILES['file']  # or self.files['image'] in your form
            path = default_storage.save('tmp/somename.mp3', ContentFile(data.read()))
            img_file2 = os.path.join(settings.MEDIA_ROOT, path)
            img_file = open(img_file2, 'rb')
            当前日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            结对共拓主界面表first = 结对共拓主界面表.objects(
                手机号=用户.手机号,
            ).first()
            结对共拓部门主任走访客户结果表first = 结对共拓部门主任走访客户结果表.objects(
                走访日期=当前日期,
                部门主任姓名=结对共拓主界面表first.姓名,
                单位名称=countries2_val
            ).first()
            if 结对共拓部门主任走访客户结果表first == None:
                结对共拓部门主任走访客户结果表(
                    走访日期=当前日期,
                    部门主任姓名=结对共拓主界面表first.姓名,
                    单位名称=countries2_val,
                    大门照片=img_file
                ).save()
                描述 = '成功'
            else:
                if 结对共拓部门主任走访客户结果表first.状态 in [客户经理未核实, 客户经理不通过, 党群部审核不通过]:
                    结对共拓部门主任走访客户结果表first.大门照片.replace(img_file)
                    结对共拓部门主任走访客户结果表first.save()
                    描述 = '成功'
                else:
                    描述 = 结对共拓部门主任走访客户结果表first.状态
            自定义登录状态 = {
                '描述': 描述,
                '会话': '',
            }
            # 自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            # 自定义登录状态 = str(自定义登录状态)
        return HttpResponse(描述)
    except:
        描述 = '系统错误'
        print(traceback.format_exc())
        # 结果表 = {
        #     '描述': 描述,
        # }
        # 结果表 = json.dumps(结果表).encode('utf-8').decode('unicode_escape')
        # 结果表 = str(结果表)
        return HttpResponse(描述)


def 客户经理核实走访初始化(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 结对共拓用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            自定义登录状态 = {
                '描述': '该用户未注册'
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            list = []
            结对共拓部门主任走访客户结果表objs = 结对共拓部门主任走访客户结果表.objects(
                状态 = 客户经理未核实
            )
            i = 0
            for 结对共拓部门主任走访客户结果表obj in 结对共拓部门主任走访客户结果表objs:
                list.append(
                    {
                        'riqi': 结对共拓部门主任走访客户结果表obj.走访日期,
                        'zhu_ren': 结对共拓部门主任走访客户结果表obj.部门主任姓名,
                        'dan_wei': 结对共拓部门主任走访客户结果表obj.单位名称,
                        'value':i
                    }
                )
                i = i+1
            自定义登录状态 = {
                '描述': '成功',
                '会话': '',
                'list': list
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        结果表 = {
            '描述': '系统错误',
        }
        结果表 = json.dumps(结果表).encode('utf-8').decode('unicode_escape')
        结果表 = str(结果表)
        return HttpResponse(结果表)


def 客户经理政企校园查询详情(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 结对共拓用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            自定义登录状态 = {
                '描述': '该用户未注册'
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            riqi = request.GET['riqi']
            zhu_ren = request.GET['zhu_ren']
            dan_wei = request.GET['dan_wei']
            结对共拓部门主任走访客户结果表first = 结对共拓部门主任走访客户结果表.objects(
                走访日期=riqi,
                部门主任姓名=zhu_ren,
                单位名称=dan_wei,
            ).first()
            if 结对共拓部门主任走访客户结果表first == None:
                自定义登录状态 = {
                    '描述': '无走访记录',
                }
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
            自定义登录状态 = {
                '描述': '成功',
                '会话': '',
                'chang_suo_lou_yu_zong_dong_shu': 结对共拓部门主任走访客户结果表first.走访主题,
                'lou_yu_ceng_shu': 结对共拓部门主任走访客户结果表first.走访对象['走访对象'],
                'di_xia_shi_ceng_shu': 结对共拓部门主任走访客户结果表first.商机信息['商机信息'],
                'dian_ti_shu_liang': 结对共拓部门主任走访客户结果表first.竞争信息['竞争信息'],
                'dx_xia_zai': 结对共拓部门主任走访客户结果表first.服务问题['服务问题'],
                'shi_fou_you_di_xia_ting_cha_chang': 结对共拓部门主任走访客户结果表first.是否有服务问题,
                'shi_fou_you_yi_wang_shi_feng': 结对共拓部门主任走访客户结果表first.是否提交云方案,
                'src': myConfig.global_image_url+'?riqi=' + riqi + '&zhu_ren=' + zhu_ren + '&dan_wei=' + dan_wei,
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        结果表 = {
            '描述': '系统错误',
        }
        结果表 = json.dumps(结果表).encode('utf-8').decode('unicode_escape')
        结果表 = str(结果表)
        return HttpResponse(结果表)


def 客户经理核实走访下载图片(request):
    try:
        riqi = request.GET['riqi']
        zhu_ren = request.GET['zhu_ren']
        dan_wei = request.GET['dan_wei']
        结对共拓部门主任走访客户结果表first = 结对共拓部门主任走访客户结果表.objects(
            走访日期 = riqi,
            部门主任姓名=zhu_ren,
            单位名称=dan_wei
        ).first()
        if 结对共拓部门主任走访客户结果表first == None:
            path = myConfig.django_root_path + '/' + 'mysite' + '/' + '404.png'
            outfile = open(path, 'rb')
            response = FileResponse(outfile)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="%s"' % "image.jpg"
            return response
        else:
            image = 结对共拓部门主任走访客户结果表first.大门照片.read()
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

def 客户经理同意走访任务(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 结对共拓用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            自定义登录状态 = {
                '描述': '该用户未注册'
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            riqi = request.GET['riqi']
            zhu_ren = request.GET['zhu_ren']
            dan_wei = request.GET['dan_wei']
            结对共拓部门主任走访客户结果表first = 结对共拓部门主任走访客户结果表.objects(
                走访日期=riqi,
                部门主任姓名=zhu_ren,
                单位名称=dan_wei,
            ).first()
            if 结对共拓部门主任走访客户结果表first == None:
                自定义登录状态 = {
                    '描述': '无效记录',
                }
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
            else:
                if 结对共拓部门主任走访客户结果表first.状态 == 客户经理未核实:
                    结对共拓部门主任走访客户结果表first.update(
                        状态=客户经理已核实
                    )
                    自定义登录状态 = {
                        '描述': '成功',
                        '会话': '',
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                elif 结对共拓部门主任走访客户结果表first.状态 == 客户经理已核实:
                    自定义登录状态 = {
                        '描述': '客户经理已核实',
                        '会话': ''
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                elif 结对共拓部门主任走访客户结果表first.状态 == 客户经理不通过:
                    自定义登录状态 = {
                        '描述': '客户经理不通过',
                        '会话': ''
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                else:
                    自定义登录状态 = {
                        '描述': '状态未定义',
                        '会话': ''
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        结果表 = {
            '描述': '系统错误',
        }
        结果表 = json.dumps(结果表).encode('utf-8').decode('unicode_escape')
        结果表 = str(结果表)
        return HttpResponse(结果表)

def 客户经理不同意走访任务(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 结对共拓用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            自定义登录状态 = {
                '描述': '该用户未注册'
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            riqi = request.GET['riqi']
            zhu_ren = request.GET['zhu_ren']
            dan_wei = request.GET['dan_wei']
            结对共拓部门主任走访客户结果表first = 结对共拓部门主任走访客户结果表.objects(
                走访日期=riqi,
                部门主任姓名=zhu_ren,
                单位名称=dan_wei,
            ).first()
            if 结对共拓部门主任走访客户结果表first == None:
                自定义登录状态 = {
                    '描述': '无效记录',
                }
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
            else:
                if 结对共拓部门主任走访客户结果表first.状态 == 客户经理未核实:
                    结对共拓部门主任走访客户结果表first.update(
                        状态=客户经理不通过
                    )
                    自定义登录状态 = {
                        '描述': '成功',
                        '会话': '',
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                else:
                    自定义登录状态 = {
                        '描述': '无效选项',
                        '会话': ''
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        结果表 = {
            '描述': '系统错误',
        }
        结果表 = json.dumps(结果表).encode('utf-8').decode('unicode_escape')
        结果表 = str(结果表)
        return HttpResponse(结果表)

def 政企校园录入积分初始化(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 结对共拓用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            自定义登录状态 = {
                '描述': '该用户未注册'
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            list = []
            结对共拓部门主任走访客户结果表objs = 结对共拓部门主任走访客户结果表.objects(
                状态 = 客户经理已核实
            )
            i = 0
            for 结对共拓部门主任走访客户结果表obj in 结对共拓部门主任走访客户结果表objs:
                list.append(
                    {
                        'riqi': 结对共拓部门主任走访客户结果表obj.走访日期,
                        'zhu_ren': 结对共拓部门主任走访客户结果表obj.部门主任姓名,
                        'dan_wei': 结对共拓部门主任走访客户结果表obj.单位名称,
                        'value': i
                    }
                )
                i = i +1
            自定义登录状态 = {
                '描述': '成功',
                '会话': '',
                'list': list
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        结果表 = {
            '描述': '系统错误',
        }
        结果表 = json.dumps(结果表).encode('utf-8').decode('unicode_escape')
        结果表 = str(结果表)
        return HttpResponse(结果表)


def 政企校园录打分(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 结对共拓用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            自定义登录状态 = {
                '描述': '该用户未注册'
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            riqi = request.GET['riqi']
            zhu_ren = request.GET['zhu_ren']
            dan_wei = request.GET['dan_wei']
            结对共拓部门主任走访客户结果表first = 结对共拓部门主任走访客户结果表.objects(
                走访日期=riqi,
                部门主任姓名=zhu_ren,
                单位名称=dan_wei,
            ).first()
            if 结对共拓部门主任走访客户结果表first == None:
                自定义登录状态 = {
                    '描述': '无效记录',
                }
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
            else:
                if 结对共拓部门主任走访客户结果表first.状态 == 客户经理未核实:
                    自定义登录状态 = {
                        '描述': '客户经理未核实',
                        '会话': '',
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                elif 结对共拓部门主任走访客户结果表first.状态 == 客户经理已核实:
                    ji_feng = request.GET['ji_feng']
                    当前时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    结对共拓部门主任走访客户结果表first.update(
                        状态 = 政企校园完成打分,
                        得分 = {'积分':ji_feng,'当前时间':当前时间},
                    )
                    自定义登录状态 = {
                        '描述': '成功',
                        '会话': ''
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                elif 结对共拓部门主任走访客户结果表first.状态 == 客户经理不通过:
                    自定义登录状态 = {
                        '描述': '客户经理不通过',
                        '会话': ''
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                else:
                    自定义登录状态 = {
                        '描述': '状态未定义',
                        '会话': ''
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        结果表 = {
            '描述': '系统错误',
        }
        结果表 = json.dumps(结果表).encode('utf-8').decode('unicode_escape')
        结果表 = str(结果表)
        return HttpResponse(结果表)


def 党群部审核初始化(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 结对共拓用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            自定义登录状态 = {
                '描述': '该用户未注册'
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            list = []
            结对共拓部门主任走访客户结果表objs = 结对共拓部门主任走访客户结果表.objects(
                状态=政企校园完成打分
            )
            i = 0
            for 结对共拓部门主任走访客户结果表obj in 结对共拓部门主任走访客户结果表objs:
                list.append(
                    {
                        'riqi': 结对共拓部门主任走访客户结果表obj.走访日期,
                        'zhu_ren': 结对共拓部门主任走访客户结果表obj.部门主任姓名,
                        'dan_wei': 结对共拓部门主任走访客户结果表obj.单位名称,
                        'value': i
                    }
                )
                i = i + 1
            自定义登录状态 = {
                '描述': '成功',
                '会话': '',
                'list': list
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        结果表 = {
            '描述': '系统错误',
        }
        结果表 = json.dumps(结果表).encode('utf-8').decode('unicode_escape')
        结果表 = str(结果表)
        return HttpResponse(结果表)


def 党群部查询详情(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 结对共拓用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            自定义登录状态 = {
                '描述': '该用户未注册'
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            riqi = request.GET['riqi']
            zhu_ren = request.GET['zhu_ren']
            dan_wei = request.GET['dan_wei']
            结对共拓部门主任走访客户结果表first = 结对共拓部门主任走访客户结果表.objects(
                走访日期=riqi,
                部门主任姓名=zhu_ren,
                单位名称=dan_wei,
                # 状态=客户经理未核实
            ).first()
            if 结对共拓部门主任走访客户结果表first == None:
                自定义登录状态 = {
                    '描述': '无走访记录',
                }
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
            自定义登录状态 = {
                '描述': '成功',
                '会话': '',
                'ji_feng':结对共拓部门主任走访客户结果表first.得分['积分'],
                'chang_suo_lou_yu_zong_dong_shu': 结对共拓部门主任走访客户结果表first.走访主题,
                'lou_yu_ceng_shu': 结对共拓部门主任走访客户结果表first.走访对象['走访对象'],
                'di_xia_shi_ceng_shu': 结对共拓部门主任走访客户结果表first.商机信息['商机信息'],
                'dian_ti_shu_liang': 结对共拓部门主任走访客户结果表first.竞争信息['竞争信息'],
                'dx_xia_zai': 结对共拓部门主任走访客户结果表first.服务问题['服务问题'],
                'shi_fou_you_di_xia_ting_cha_chang': 结对共拓部门主任走访客户结果表first.是否有服务问题,
                'shi_fou_you_yi_wang_shi_feng': 结对共拓部门主任走访客户结果表first.是否提交云方案,
                'src': myConfig.global_image_url+'?riqi=' + riqi + '&zhu_ren=' + zhu_ren + '&dan_wei=' + dan_wei,
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        结果表 = {
            '描述': '系统错误',
        }
        结果表 = json.dumps(结果表).encode('utf-8').decode('unicode_escape')
        结果表 = str(结果表)
        return HttpResponse(结果表)

def 党群部同意走访任务(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 结对共拓用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            自定义登录状态 = {
                '描述': '该用户未注册'
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            riqi = request.GET['riqi']
            zhu_ren = request.GET['zhu_ren']
            dan_wei = request.GET['dan_wei']
            结对共拓部门主任走访客户结果表first = 结对共拓部门主任走访客户结果表.objects(
                走访日期=riqi,
                部门主任姓名=zhu_ren,
                单位名称=dan_wei,
            ).first()
            if 结对共拓部门主任走访客户结果表first == None:
                自定义登录状态 = {
                    '描述': '无效记录',
                }
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
            else:
                if 结对共拓部门主任走访客户结果表first.状态 == 客户经理未核实:
                    自定义登录状态 = {
                        '描述': '客户经理未核实',
                        '会话': '',
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                elif 结对共拓部门主任走访客户结果表first.状态 == 客户经理已核实:
                    自定义登录状态 = {
                        '描述': '客户经理已核实',
                        '会话': ''
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                elif 结对共拓部门主任走访客户结果表first.状态 == 客户经理不通过:
                    自定义登录状态 = {
                        '描述': '客户经理不通过',
                        '会话': ''
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                elif 结对共拓部门主任走访客户结果表first.状态 == 政企校园完成打分:
                    结对共拓部门主任走访客户结果表first.update(
                        状态 = 党群部审核通过
                    )
                    自定义登录状态 = {
                        '描述': '成功',
                        '会话': ''
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                else:
                    自定义登录状态 = {
                        '描述': '状态未定义',
                        '会话': ''
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        结果表 = {
            '描述': '系统错误',
        }
        结果表 = json.dumps(结果表).encode('utf-8').decode('unicode_escape')
        结果表 = str(结果表)
        return HttpResponse(结果表)

def 党群部不同意走访任务(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 结对共拓用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            自定义登录状态 = {
                '描述': '该用户未注册'
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            riqi = request.GET['riqi']
            zhu_ren = request.GET['zhu_ren']
            dan_wei = request.GET['dan_wei']
            结对共拓部门主任走访客户结果表first = 结对共拓部门主任走访客户结果表.objects(
                走访日期=riqi,
                部门主任姓名=zhu_ren,
                单位名称=dan_wei,
            ).first()
            if 结对共拓部门主任走访客户结果表first == None:
                自定义登录状态 = {
                    '描述': '无效记录',
                }
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
            else:
                if 结对共拓部门主任走访客户结果表first.状态 == 客户经理未核实:
                    自定义登录状态 = {
                        '描述': '客户经理未核实',
                        '会话': '',
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                elif 结对共拓部门主任走访客户结果表first.状态 == 客户经理已核实:
                    自定义登录状态 = {
                        '描述': '客户经理已核实',
                        '会话': ''
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                elif 结对共拓部门主任走访客户结果表first.状态 == 客户经理不通过:
                    自定义登录状态 = {
                        '描述': '客户经理不通过',
                        '会话': ''
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                elif 结对共拓部门主任走访客户结果表first.状态 == 政企校园完成打分:
                    结对共拓部门主任走访客户结果表first.update(
                        状态=党群部审核不通过
                    )
                    自定义登录状态 = {
                        '描述': '成功',
                        '会话': ''
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                else:
                    自定义登录状态 = {
                        '描述': '状态未定义',
                        '会话': ''
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        结果表 = {
            '描述': '系统错误',
        }
        结果表 = json.dumps(结果表).encode('utf-8').decode('unicode_escape')
        结果表 = str(结果表)
        return HttpResponse(结果表)


def 查询任务初始化(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 结对共拓用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            自定义登录状态 = {
                '描述': '该用户未注册'
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            list = []
            结对共拓部门主任走访客户结果表objs = 结对共拓部门主任走访客户结果表.objects
            i = 0
            for 结对共拓部门主任走访客户结果表obj in 结对共拓部门主任走访客户结果表objs:
                list.append(
                    {
                        'riqi': 结对共拓部门主任走访客户结果表obj.走访日期,
                        'zhu_ren': 结对共拓部门主任走访客户结果表obj.部门主任姓名,
                        'dan_wei': 结对共拓部门主任走访客户结果表obj.单位名称,
                        'value': i
                    }
                )
                i = i + 1
            自定义登录状态 = {
                '描述': '成功',
                '会话': '',
                'list': list
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        结果表 = {
            '描述': '系统错误',
        }
        结果表 = json.dumps(结果表).encode('utf-8').decode('unicode_escape')
        结果表 = str(结果表)
        return HttpResponse(结果表)


def 查询任务详情(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': jdgt_appid, 'secret': jdgt_secret, 'js_code': js_code,
                   'grant_type': jdgt_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 结对共拓用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            自定义登录状态 = {
                '描述': '该用户未注册'
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            riqi = request.GET['riqi']
            zhu_ren = request.GET['zhu_ren']
            dan_wei = request.GET['dan_wei']
            结对共拓部门主任走访客户结果表first = 结对共拓部门主任走访客户结果表.objects(
                走访日期=riqi,
                部门主任姓名=zhu_ren,
                单位名称=dan_wei,
            ).first()
            if 结对共拓部门主任走访客户结果表first == None:
                自定义登录状态 = {
                    '描述': '无走访记录',
                }
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
            自定义登录状态 = {
                '描述': '成功',
                '会话': '',
                '状态':结对共拓部门主任走访客户结果表first.状态,
                'ji_feng':结对共拓部门主任走访客户结果表first.得分['积分'],
                'chang_suo_lou_yu_zong_dong_shu': 结对共拓部门主任走访客户结果表first.走访主题,
                'lou_yu_ceng_shu': 结对共拓部门主任走访客户结果表first.走访对象['走访对象'],
                'di_xia_shi_ceng_shu': 结对共拓部门主任走访客户结果表first.商机信息['商机信息'],
                'dian_ti_shu_liang': 结对共拓部门主任走访客户结果表first.竞争信息['竞争信息'],
                'dx_xia_zai': 结对共拓部门主任走访客户结果表first.服务问题['服务问题'],
                'shi_fou_you_di_xia_ting_cha_chang': 结对共拓部门主任走访客户结果表first.是否有服务问题,
                'shi_fou_you_yi_wang_shi_feng': 结对共拓部门主任走访客户结果表first.是否提交云方案,
                'src': myConfig.global_image_url + '?riqi=' + riqi + '&zhu_ren=' + zhu_ren + '&dan_wei=' + dan_wei,
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        结果表 = {
            '描述': '系统错误',
        }
        结果表 = json.dumps(结果表).encode('utf-8').decode('unicode_escape')
        结果表 = str(结果表)
        return HttpResponse(结果表)