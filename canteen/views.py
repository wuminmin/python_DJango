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
from mysite.demo_sms_send import send_sms
from myConfig import appid, secret, grant_type, django_root_path, canteen_appid, canteen_secret, canteen_grant_type, \
    sign_name, template_code
from .models import 订餐食堂模版表, 订餐结果表, 订餐主界面表, 订餐用户表, 订餐登录状态表, 订餐验证码表, 没吃, 吃过, 中餐统计, 晚餐统计, 订餐核销码表, 取消, 订餐部门表, \
    订餐统计结果, 订餐菜单分页, 订餐菜单表, 菜单分隔符, 订餐菜单模版表, 订餐菜单评价表, 订餐评论表, 早餐统计, 青阳食堂, 青阳电信分公司, 池州烟草公司, 池州电信分公司, 早餐外带统计, 中餐外带统计, 晚餐外带统计, \
    烟草公司每月外带上限次数
import sys
from . import models
from . import tool
from . import db

from canteen.auto import 启动定时器
启动定时器()


def myHttpResponse(res):  # 合并跨域配置
    import json
    from django.http import HttpResponse, FileResponse
    response = HttpResponse(json.dumps(res))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

# 异步函数
def deprecated_async(f):
    def wrapper(*args, **kwargs):
        from threading import Thread
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

def 订餐登录检查(request):
    try:
        wx_login_get_openid_dict = tool.wx_login_get_openid(request)
        查询结果 = 订餐用户表.objects(openid=wx_login_get_openid_dict['openid']).first()
        if 查询结果 == None:
            自定义登录状态 = "{\"描述\":\"用户不存在\",\"会话\":\"\"}"
            return HttpResponse(自定义登录状态)
        else:
            r = 订餐登录状态表(session_key='', openid=wx_login_get_openid_dict['openid']).save()
            自定义登录状态 = "{\"描述\":\"新界面\",\"会话\":\"" + str(r.id) + "\"}"
            return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')


def 订餐下载主界面数据(request):
    try:
        wx_login_get_openid_dict = tool.wx_login_get_openid(request)
        用户 = 订餐用户表.objects(openid=wx_login_get_openid_dict['openid']).first()
        if 用户 == None:
            自定义登录状态 = {'描述': '未注册手机号', '姓名': '', '当前日期': '', '类型': ''}
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            手机号 = 用户.手机号
            主界面 = models.订餐主界面表.objects(手机号=手机号).first()
            if 主界面 == None:
                用户.delete()
                描述 = '没有数据'
                会话 = '123456'
                主页标题 = ''
                主页描述 = ''
                验证码标题 = ''
                验证码描述 = ''
                主界内容 = []
                自定义登录状态 = {'描述': 描述, '会话': 会话,'主页标题':主页标题,'主页描述':主页描述,'验证码标题':验证码标题,
                           '验证码描述':验证码描述,'主界内容':主界内容}
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
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
        wx_login_get_openid_dict = tool.wx_login_get_openid(request)
        用户 = 订餐用户表.objects(openid=wx_login_get_openid_dict['openid']).first()
        if 用户 == None:
            自定义登录状态 = "{\"描述\":\"用户不存在\",\"会话\":\"" + '' + "\"}"
            return HttpResponse(自定义登录状态)
        else:
            手机号 = 用户.手机号
            订餐主界面表first = 订餐主界面表.objects(手机号=手机号).first()
            if 订餐主界面表first == None:
                自定义登录状态 = "{\"描述\":\"用户未授权\",\"会话\":\"" + '' + "\"}"
                return HttpResponse(自定义登录状态)

            订餐模版表_one = 订餐食堂模版表.objects(子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc).first()
            if 订餐模版表_one == None:
                自定义登录状态 = "{\"描述\":\"没有食堂\",\"会话\":\"" + '' + "\"}"
                return HttpResponse(自定义登录状态)
            else:
                食堂地址 = 订餐模版表_one.食堂地址
                主菜单name = 订餐模版表_one.主菜单name
                用餐日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                预订开始日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                预订结束日期 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 864000))
                会话 = ''
                描述 = '下载成功'
                if 订餐主界面表first.二级部门 == '青阳分公司':
                    countries = ['无', '预定1份', '预定2份', '预定3份']
                else:
                    countries = ['无', '预定1份']
                if 订餐主界面表first.二级部门 == '青阳分公司':
                    accounts = ['无', '预定1份', '预定2份', '预定3份']
                else:
                    accounts = ['无', '预定1份']
                if 订餐主界面表first.二级部门 == '青阳分公司':
                    accounts2 = ['无', '预定1份', '预定2份', '预定3份']
                else:
                    accounts2 = ['无', '预定1份']

                自定义登录状态 = {'描述': 描述, '会话': 会话, '预订开始日期': 预订开始日期, '预订结束日期': 预订结束日期, '主菜单name': 主菜单name,
                           '子菜单page_name': 子菜单page_name, '子菜单page_desc': 子菜单page_desc, '食堂地址': 食堂地址, '用餐日期': 用餐日期,
                           'countries': countries, 'accounts': accounts, 'accounts2': accounts2, }
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')


def 下载订餐模版2(request):
    try:
        用餐日期 = request.GET['date']
        主菜单name = request.GET['name']
        子菜单page_name = request.GET['page_name']
        子菜单page_desc = request.GET['page_desc']
        wx_login_get_openid_dict = tool.wx_login_get_openid(request)
        用户 = 订餐用户表.objects(openid=wx_login_get_openid_dict['openid']).first()
        if 用户 == None:
            自定义登录状态 = "{\"描述\":\"用户不存在\",\"会话\":\"" + '' + "\"}"
            return HttpResponse(自定义登录状态)
        else:
            手机号 = 用户.手机号
            订餐主界面表first = 订餐主界面表.objects(手机号=手机号).first()
            if 订餐主界面表first == None:
                自定义登录状态 = "{\"描述\":\"用户未授权\",\"会话\":\"" + '' + "\"}"
                return HttpResponse(自定义登录状态)
            # 订餐模版表_one = 订餐食堂模版表.objects(子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc).first()
            # if 订餐模版表_one == None:
            #     自定义登录状态 = "{\"描述\":\"没有食堂\",\"会话\":\"" + '' + "\"}"
            #     return HttpResponse(自定义登录状态)
            else:
                # 主菜单name = 订餐模版表_one.主菜单name
                if 用餐日期 == '':
                    用餐日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                会话 = ''
                描述 = '下载成功'
                queryset0 = 订餐结果表.objects(手机号=手机号, 用餐日期=用餐日期,子菜单page_name=子菜单page_name,
                    子菜单page_desc=子菜单page_desc, ).first()
                ding_can_list = [ ]
                from . import models
                for one in models.产品全局字典[wx_login_get_openid_dict['app_id']]['产品列表']:
                    if queryset0 == None:
                        ding_can_list.append(
                            {
                                'tittle':one['名称'],'input_list': one['预定数量条件'],
                                    'input_index': 0
                            }
                        )
                    else:
                        if one['名称'] in queryset0.产品:
                            ding_can_list.append(
                                {
                                    'tittle':one['名称'],'input_list': one['预定数量条件'],
                                    'input_index': queryset0.产品[one['名称']]['预定数量']
                                }
                            )
                        else:
                            ding_can_list.append(
                                {
                                    'tittle':one['名称'],'input_list': one['预定数量条件'],
                                        'input_index': 0
                                }
                            )
                from . import models
                qset4 = models.订餐钱包表.objects(openid=wx_login_get_openid_dict['openid']).first()
                if qset4 == None:
                    qset5 = models.订餐钱包充值表.objects(手机号=手机号,充值成功标识=False).first()
                    if qset5 == None:
                        充值金额=0
                        models.订餐钱包表(openid=wx_login_get_openid_dict['openid'],已充值=充值金额).save()
                    else:
                        充值金额 = qset5.充值金额
                        models.订餐钱包表(openid=wx_login_get_openid_dict['openid'],已充值=充值金额).save()
                        qset5.update(充值成功标识=True)
                    余额 = 充值金额
                    钱包 = '已充值:'+ str(充值金额/100) +'元,余额：'+str(余额/100)+'元，已消费'+ str(0)+'元,预消费' +str(0) +'元。'
                else:
                    qset5 = models.订餐钱包充值表.objects(手机号=手机号,充值成功标识=False).first()
                    if qset5 == None:
                        充值金额=0
                        已充值 = qset4.已充值+充值金额
                    else:
                        充值金额 = qset5.充值金额
                        已充值 = qset4.已充值+充值金额
                        qset4.update(已充值=已充值)
                        qset5.update(充值成功标识=True)
                    余额 = 已充值 - qset4.已消费 - qset4.预消费
                    钱包 = '已充值:'+ str(已充值/100)  +'元,余额：'+str(余额/100) +'元,已消费'+ str(qset4.已消费/100)+'元,预消费' +str(qset4.预消费/100) +'元。'
                自定义登录状态 = {
                    'ding_can_list': ding_can_list, 
                    '描述': 描述, '会话': 会话, 
                    '预订开始日期': '', 
                    '预订结束日期': '',
                    # '主菜单name': 主菜单name, 
                    '子菜单page_name': 子菜单page_name, 
                    '子菜单page_desc': 子菜单page_desc, 
                    '食堂地址': 钱包,
                    '用餐日期': 用餐日期, 
                }
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')

@deprecated_async
def 异步计算消费金额(wx_login_get_openid_dict):
    from . import models
    已消费 = 0
    预消费 = 0
    qset订餐用户表 =  models.订餐用户表.objects( openid=wx_login_get_openid_dict['openid'] ).first()
    if qset订餐用户表 == None:
        pass
    else:
        手机号 = qset订餐用户表.手机号
        查询预消费和已消费 = db.查询预消费和已消费(手机号,models.产品全局字典[wx_login_get_openid_dict['app_id']]['产品名称列表'])
        已消费 = 已消费 + 查询预消费和已消费['已消费']
        预消费 = 预消费 + 查询预消费和已消费['预消费']
        qset1 = models.订餐钱包表.objects(openid=wx_login_get_openid_dict['openid']).first()
        if qset1 == None:
            pass
        else:
            qset1.update(
                已消费 = 已消费,
                预消费 = 预消费
            )

def 上传订餐结果2(request):
    from . import models
    try:
        js_code = request.GET['code']
        wx_login_get_openid_dict = tool.wx_login_get_openid(request)
        当前时间戳 = time.time()
        当前时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        当前日期加一天 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400))
        当前日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        当前月份 = time.strftime('%Y-%m', time.localtime(time.time()))
        订餐用户表_one = 订餐用户表.objects(openid=wx_login_get_openid_dict['openid']).first()
        if 订餐用户表_one == None:
            自定义登录状态 = "{\"描述\":\"用户不存在\",\"会话\":\"\"}"
            return HttpResponse(自定义登录状态)
        else:
            手机号 = 订餐用户表_one.手机号
            订餐主界面表_first = 订餐主界面表.objects(手机号=手机号).first()
            折扣标签 = 订餐主界面表_first.四级部门
            主菜单name = request.GET['name']
            子菜单page_name = request.GET['page_name']
            子菜单page_desc = request.GET['page_desc']
            用餐日期 = request.GET['date']
            if 用餐日期 < 当前日期:
                自定义登录状态 = "{\"描述\":\"预订日期不正确\",\"会话\":\"\"}"
                return HttpResponse(自定义登录状态)
            queryset0 = models.订餐结果表.objects(手机号=手机号, 主菜单name=主菜单name, 子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc,
                用餐日期=用餐日期).first()
            
            if queryset0 == None: #同步订餐临时表和结果表
                models.订餐结果表(手机号=手机号, 主菜单name=主菜单name, 子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc,
                    用餐日期=用餐日期, ).save()
                queryset1 = models.订餐结果临时表.objects(手机号=手机号, 主菜单name=主菜单name, 子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc,
                用餐日期=用餐日期).first()
                if queryset1 == None:
                    models.订餐结果临时表(手机号=手机号, 主菜单name=主菜单name, 子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc,
                    用餐日期=用餐日期, ).save()
                else:
                    queryset1.delete()
                    models.订餐结果临时表(手机号=手机号, 主菜单name=主菜单name, 子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc,
                    用餐日期=用餐日期, ).save()
            else:
                queryset1 = models.订餐结果临时表.objects(手机号=手机号, 主菜单name=主菜单name, 子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc,
                用餐日期=用餐日期).first()
                if queryset1 == None:
                    models.订餐结果临时表(手机号=手机号, 主菜单name=主菜单name, 子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc,
                        用餐日期=用餐日期,
                    ).save()
            ding_can_list = request.GET.get('ding_can_list')
            ding_can_list = json.loads(ding_can_list)
            totalAmount_int = 0
            goods = []
            for ding_can_list_one in ding_can_list:
                tittle = ding_can_list_one['tittle']
                index = int (ding_can_list_one['input_index'] )
                qset2 = models.订餐结果表.objects(
                        手机号=手机号,  
                        子菜单page_name=子菜单page_name,
                        用餐日期=用餐日期
                    ).first()
                queryset1 = models.订餐结果临时表.objects(
                    手机号=手机号,子菜单page_name=子菜单page_name,
                    用餐日期=用餐日期
                ).first()
                for one in models.产品全局字典[wx_login_get_openid_dict['app_id']]['产品列表']:
                    if tittle == one['名称']:
                        if qset2 == None :
                            签到 = '没吃'
                            totalAmount_int = totalAmount_int + tool.动态计算金额(index,one,折扣标签)
                        elif tittle in qset2.产品:
                            签到 = qset2.产品[tittle]['签到']
                            
                            已有预定数量 = qset2.产品[tittle]['预定数量']
                            if index == 已有预定数量:
                                totalAmount_int = totalAmount_int + tool.动态计算金额((index-已有预定数量),one,折扣标签)
                            elif index < 已有预定数量:
                                if 签到 == '吃过':
                                    自定义登录状态 = {'描述': tittle+'吃过,不能修改', '会话': ''}
                                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                                    自定义登录状态 = str(自定义登录状态)
                                    return HttpResponse(自定义登录状态)
                                totalAmount_int = totalAmount_int + tool.动态计算金额((index-已有预定数量),one,折扣标签)
                                就餐时间 = one['就餐时间']
                                就餐时间 = 用餐日期 + ' ' + 就餐时间
                                取消提前秒 = one['取消提前秒']
                                预定提前截止时间 = time.mktime(time.strptime(就餐时间, "%Y-%m-%d %H:%M:%S")) - 取消提前秒
                                if 当前时间戳 < 预定提前截止时间:
                                    pass
                                else:
                                    订餐取消计数表1 = models.订餐取消计数表.objects(__raw__ = {'d.手机号':手机号,'d.月份':当前月份}).first()
                                    if 订餐取消计数表1 == None:
                                        d = {'手机号':手机号,'取消次数':1,'月份':当前月份}
                                        models.订餐取消计数表(d=d).save()
                                    else:
                                        取消次数 = 订餐取消计数表1.d['取消次数']
                                        取消次数上限 = models.产品全局字典[wx_login_get_openid_dict['app_id']]['取消次数上限']
                                        if 取消次数 <= 取消次数上限:
                                            tmp_d = 订餐取消计数表1.d
                                            d['取消次数'] = d['取消次数']+1
                                            订餐取消计数表1.update(d=tmp_d)
                                        else:
                                            自定义登录状态 = {'描述': tittle+'已过期，且超过'+str(取消次数上限)+'次取消上限。', '会话': ''}
                                            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                                            自定义登录状态 = str(自定义登录状态)
                                            return HttpResponse(自定义登录状态)
                            else:
                                if 签到 == '吃过':
                                    自定义登录状态 = {'描述': tittle+'吃过,不能修改', '会话': ''}
                                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                                    自定义登录状态 = str(自定义登录状态)
                                    return HttpResponse(自定义登录状态)
                                totalAmount_int = totalAmount_int + tool.动态计算金额((index-已有预定数量),one,折扣标签)
                                就餐时间 = one['就餐时间']
                                就餐时间 = 用餐日期 + ' ' + 就餐时间
                                取消提前秒 = one['取消提前秒']
                                预定提前截止时间 = time.mktime(time.strptime(就餐时间, "%Y-%m-%d %H:%M:%S")) - 取消提前秒
                                if 当前时间戳 < 预定提前截止时间:
                                    签到 = '没吃'
                                else:
                                    自定义登录状态 = {'描述': tittle+'已过期，不能预定', '会话': ''}
                                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                                    自定义登录状态 = str(自定义登录状态)
                                    return HttpResponse(自定义登录状态)
                        else:
                            签到 = '没吃'
                            if index == 0:
                                pass
                            else:
                                totalAmount_int = totalAmount_int + tool.动态计算金额((index),one,折扣标签)
                                就餐时间 = one['就餐时间']
                                就餐时间 = 用餐日期 + ' ' + 就餐时间
                                取消提前秒 = one['取消提前秒']
                                预定提前截止时间 = time.mktime(time.strptime(就餐时间, "%Y-%m-%d %H:%M:%S")) - 取消提前秒
                                if 当前时间戳 < 预定提前截止时间:
                                    pass
                                else:
                                    自定义登录状态 = {'描述': tittle+'已过期，不能预定', '会话': ''}
                                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                                    自定义登录状态 = str(自定义登录状态)
                                    return HttpResponse(自定义登录状态)
                        产品 = queryset1.产品
                        产品[tittle] = {
                            '预定时间':当前时间,
                            '预定数量':index,
                            '签到':签到,
                            '价格':tool.动态计算价格(one,折扣标签)
                        }
                        queryset1.update(产品=产品)
            queryset10 = models.订餐结果临时表.objects(
                手机号=手机号,
                子菜单page_name=子菜单page_name,
                用餐日期=用餐日期, 
            ).first()
            qset11 = models.订餐钱包表.objects(openid=wx_login_get_openid_dict['openid']).first()
            if qset11 == None:
                models.订餐钱包表(openid=wx_login_get_openid_dict['openid'],已充值=0).save()
                qset11 = models.订餐钱包表.objects(openid=wx_login_get_openid_dict['openid']).first()
                已充值 = qset11.已充值
            else:
                已充值 = qset11.已充值
            if 已充值 - totalAmount_int - qset11.已消费 - qset11.预消费  >= 0:
                qset22 = models.订餐结果表.objects(
                    手机号=queryset10.手机号,
                    主菜单name=queryset10.主菜单name,
                    子菜单page_name=queryset10.子菜单page_name,
                    子菜单page_desc=queryset10.子菜单page_desc, 
                    用餐日期=queryset10.用餐日期
                ).first()
                if qset22 == None:
                    models.订餐结果表(
                        手机号=queryset10.手机号,
                        主菜单name=queryset10.主菜单name,
                        子菜单page_name=queryset10.子菜单page_name,
                        子菜单page_desc=queryset10.子菜单page_desc, 
                        用餐日期=queryset10.用餐日期,
                        产品 = queryset10.产品
                    ).save()
                    异步计算消费金额(wx_login_get_openid_dict)
                else:
                    qset22.update(
                        产品 = queryset10.产品
                    )
                    异步计算消费金额(wx_login_get_openid_dict)
                描述 = '上传成功'
                订餐结果描述 = '上传成功'
                自定义登录状态 = {'描述': 描述, '会话': '123456', '订餐结果描述': 订餐结果描述}
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                异步计算订餐结果(子菜单page_name, 订餐主界面表_first.二级部门)
                异步统计产品(子菜单page_name, 订餐主界面表_first.二级部门,wx_login_get_openid_dict)
                return HttpResponse(自定义登录状态)
            else:
                ding_can_chinaums_pay_order_res = ding_can_chinaums_pay_order(str(totalAmount_int),goods,wx_login_get_openid_dict)
                print(ding_can_chinaums_pay_order_res)
                描述 = '银联下单'
                订餐结果描述 = '银联下单'
                其他参数 = {
                    'totalAmount':totalAmount_int,
                    'oid':str( queryset10.id ) ,
                    '子菜单page_name':子菜单page_name,
                    '二级部门':订餐主界面表_first.二级部门
                }
                自定义登录状态 = {
                    '描述': 描述, '会话': '',
                    '订餐结果描述': 订餐结果描述,
                    'miniPayRequest':ding_can_chinaums_pay_order_res['miniPayRequest'],
                    'state': 其他参数 
                }
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')

def 订餐校验验证码(request):
    from . import models
    手机号 = str(request.GET['phone'])
    验证码 = str(request.GET['sms_code'])
    wx_login_get_openid_dict = tool.wx_login_get_openid(request)
    r = models.订餐验证码表.objects(手机号=手机号)
    for rr in r:
        if rr.验证码 == 验证码:
            订餐用户表(手机号=手机号, openid=wx_login_get_openid_dict['openid']).save()
            return HttpResponse('绑定成功')
    return HttpResponse('绑定失败')


def 订餐发送验证码(request):
    try:
        手机号 = str(request.GET['phone'])
        if 手机号 == '':
            return HttpResponse("手机号为空")
        elif 手机号 == '123456789':
            return HttpResponse("验证码")
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
def 异步计算订餐结果(子菜单page_name, 二级部门):
    第一天 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    第二天 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400))
    第三天 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400 + 86400))
    日期_list = [第一天, 第二天, 第三天]
    for 日期_list_one in 日期_list:
        日期 = 日期_list_one
        子菜单page_desc_list = [早餐统计, 中餐统计, 晚餐统计, 早餐外带统计, 中餐外带统计, 晚餐外带统计]
        for 子菜单page_desc_list_one in 子菜单page_desc_list:
            子菜单page_desc = 子菜单page_desc_list_one
            订餐部门表_first = 订餐部门表.objects(二级部门=二级部门).first()
            if 订餐部门表_first == None:
                name_list = []
            else:
                name_list = 订餐部门表_first.三级部门列表
            总人数 = 0
            没吃人数 = 0
            吃过人数 = 0
            总份数 = 0
            没吃份数 = 0
            吃过份数 = 0
            订餐结果表_all = 订餐结果表.objects(子菜单page_name=子菜单page_name, 用餐日期=日期)
            # if 子菜单page_desc == 中餐统计:
            #     订餐结果表_all = 订餐结果表.objects(子菜单page_name=子菜单page_name, 中餐食堂就餐预订数__gte=1, 用餐日期=日期)
            #     总人数 = len(list(订餐结果表.objects(子菜单page_name=子菜单page_name, 中餐食堂就餐预订数__gte=1, 用餐日期=日期)))
            #     没吃人数 = len(list(订餐结果表.objects(子菜单page_name=子菜单page_name, 中餐食堂就餐预订数__gte=1, 用餐日期=日期, 中餐食堂就餐签到=没吃)))
            #     吃过人数 = len(list(订餐结果表.objects(子菜单page_name=子菜单page_name, 中餐食堂就餐预订数__gte=1, 用餐日期=日期, 中餐食堂就餐签到=吃过)))
            #     总份数 = 订餐结果表.objects(子菜单page_name=子菜单page_name, 中餐食堂就餐预订数__gte=1, 用餐日期=日期).sum('中餐食堂就餐预订数')
            #     没吃份数 = 订餐结果表.objects(子菜单page_name=子菜单page_name, 中餐食堂就餐预订数__gte=1, 用餐日期=日期, 中餐食堂就餐签到=没吃).sum('中餐食堂就餐预订数')
            #     吃过份数 = 订餐结果表.objects(子菜单page_name=子菜单page_name, 中餐食堂就餐预订数__gte=1, 用餐日期=日期, 中餐食堂就餐签到=吃过).sum('中餐食堂就餐预订数')
            # elif 子菜单page_desc == 晚餐统计:
            #     订餐结果表_all = 订餐结果表.objects(子菜单page_name=子菜单page_name, 晚餐食堂就餐预订数__gte=1, 用餐日期=日期)
            #     总人数 = len(list(订餐结果表.objects(子菜单page_name=子菜单page_name, 晚餐食堂就餐预订数__gte=1, 用餐日期=日期)))
            #     没吃人数 = len(list(订餐结果表.objects(子菜单page_name=子菜单page_name, 晚餐食堂就餐预订数__gte=1, 用餐日期=日期, 晚餐食堂就餐签到=没吃)))
            #     吃过人数 = len(list(订餐结果表.objects(子菜单page_name=子菜单page_name, 晚餐食堂就餐预订数__gte=1, 用餐日期=日期, 晚餐食堂就餐签到=吃过)))
            #     总份数 = 订餐结果表.objects(子菜单page_name=子菜单page_name, 晚餐食堂就餐预订数__gte=1, 用餐日期=日期).sum('晚餐食堂就餐预订数')
            #     没吃份数 = 订餐结果表.objects(子菜单page_name=子菜单page_name, 晚餐食堂就餐预订数__gte=1, 用餐日期=日期, 晚餐食堂就餐签到=没吃).sum('晚餐食堂就餐预订数')
            #     吃过份数 = 订餐结果表.objects(子菜单page_name=子菜单page_name, 晚餐食堂就餐预订数__gte=1, 用餐日期=日期, 晚餐食堂就餐签到=吃过).sum('晚餐食堂就餐预订数')
            # elif 子菜单page_desc == 早餐统计:
            #     订餐结果表_all = 订餐结果表.objects(子菜单page_name=子菜单page_name, 早餐食堂就餐预订数__gte=1, 用餐日期=日期)
            #     总人数 = len(list(订餐结果表.objects(子菜单page_name=子菜单page_name, 早餐食堂就餐预订数__gte=1, 用餐日期=日期)))
            #     没吃人数 = len(list(订餐结果表.objects(子菜单page_name=子菜单page_name, 早餐食堂就餐预订数__gte=1, 用餐日期=日期, 早餐食堂就餐签到=没吃)))
            #     吃过人数 = len(list(订餐结果表.objects(子菜单page_name=子菜单page_name, 早餐食堂就餐预订数__gte=1, 用餐日期=日期, 早餐食堂就餐签到=吃过)))
            #     总份数 = 订餐结果表.objects(子菜单page_name=子菜单page_name, 早餐食堂就餐预订数__gte=1, 用餐日期=日期).sum('早餐食堂就餐预订数')
            #     没吃份数 = 订餐结果表.objects(子菜单page_name=子菜单page_name, 早餐食堂就餐预订数__gte=1, 用餐日期=日期, 早餐食堂就餐签到=没吃).sum('早餐食堂就餐预订数')
            #     吃过份数 = 订餐结果表.objects(子菜单page_name=子菜单page_name, 早餐食堂就餐预订数__gte=1, 用餐日期=日期, 早餐食堂就餐签到=吃过).sum('早餐食堂就餐预订数')
            # elif 子菜单page_desc == 早餐外带统计:
            #     订餐结果表_all = 订餐结果表.objects(子菜单page_name=子菜单page_name, 早餐食堂外带预订数__gte=1, 用餐日期=日期)
            #     总人数 = len(list(订餐结果表.objects(子菜单page_name=子菜单page_name, 早餐食堂外带预订数__gte=1, 用餐日期=日期)))
            #     没吃人数 = len(list(订餐结果表.objects(子菜单page_name=子菜单page_name, 早餐食堂外带预订数__gte=1, 用餐日期=日期, 中餐食堂就餐签到=没吃)))
            #     吃过人数 = len(list(订餐结果表.objects(子菜单page_name=子菜单page_name, 早餐食堂外带预订数__gte=1, 用餐日期=日期, 中餐食堂就餐签到=吃过)))
            #     总份数 = 订餐结果表.objects(子菜单page_name=子菜单page_name, 早餐食堂外带预订数__gte=1, 用餐日期=日期).sum('早餐食堂外带预订数')
            #     没吃份数 = 订餐结果表.objects(子菜单page_name=子菜单page_name, 早餐食堂外带预订数__gte=1, 用餐日期=日期, 中餐食堂就餐签到=没吃).sum('早餐食堂外带预订数')
            #     吃过份数 = 订餐结果表.objects(子菜单page_name=子菜单page_name, 早餐食堂外带预订数__gte=1, 用餐日期=日期, 中餐食堂就餐签到=吃过).sum('早餐食堂外带预订数')
            # elif 子菜单page_desc == 中餐外带统计:
            #     订餐结果表_all = 订餐结果表.objects(子菜单page_name=子菜单page_name, 中餐食堂外带预订数__gte=1, 用餐日期=日期)
            #     总人数 = len(list(订餐结果表.objects(子菜单page_name=子菜单page_name, 中餐食堂外带预订数__gte=1, 用餐日期=日期)))
            #     没吃人数 = len(list(订餐结果表.objects(子菜单page_name=子菜单page_name, 中餐食堂外带预订数__gte=1, 用餐日期=日期, 中餐食堂就餐签到=没吃)))
            #     吃过人数 = len(list(订餐结果表.objects(子菜单page_name=子菜单page_name, 中餐食堂外带预订数__gte=1, 用餐日期=日期, 中餐食堂就餐签到=吃过)))
            #     总份数 = 订餐结果表.objects(子菜单page_name=子菜单page_name, 中餐食堂外带预订数__gte=1, 用餐日期=日期).sum('中餐食堂外带预订数')
            #     没吃份数 = 订餐结果表.objects(子菜单page_name=子菜单page_name, 中餐食堂外带预订数__gte=1, 用餐日期=日期, 中餐食堂就餐签到=没吃).sum('中餐食堂外带预订数')
            #     吃过份数 = 订餐结果表.objects(子菜单page_name=子菜单page_name, 中餐食堂外带预订数__gte=1, 用餐日期=日期, 中餐食堂就餐签到=吃过).sum('中餐食堂外带预订数')
            # elif 子菜单page_desc == 晚餐外带统计:
            #     订餐结果表_all = 订餐结果表.objects(子菜单page_name=子菜单page_name, 晚餐食堂外带预订数__gte=1, 用餐日期=日期)
            #     总人数 = len(list(订餐结果表.objects(子菜单page_name=子菜单page_name, 晚餐食堂外带预订数__gte=1, 用餐日期=日期)))
            #     没吃人数 = len(list(订餐结果表.objects(子菜单page_name=子菜单page_name, 晚餐食堂外带预订数__gte=1, 用餐日期=日期, 中餐食堂就餐签到=没吃)))
            #     吃过人数 = len(list(订餐结果表.objects(子菜单page_name=子菜单page_name, 晚餐食堂外带预订数__gte=1, 用餐日期=日期, 中餐食堂就餐签到=吃过)))
            #     总份数 = 订餐结果表.objects(子菜单page_name=子菜单page_name, 晚餐食堂外带预订数__gte=1, 用餐日期=日期).sum('晚餐食堂外带预订数')
            #     没吃份数 = 订餐结果表.objects(子菜单page_name=子菜单page_name, 晚餐食堂外带预订数__gte=1, 用餐日期=日期, 中餐食堂就餐签到=没吃).sum('晚餐食堂外带预订数')
            #     吃过份数 = 订餐结果表.objects(子菜单page_name=子菜单page_name, 晚餐食堂外带预订数__gte=1, 用餐日期=日期, 中餐食堂就餐签到=吃过).sum('晚餐食堂外带预订数')
            # else:
            #     订餐结果表_all = []
            #     pass
            r_list = []
            id = 1
            for name_one in name_list:
                r_dict = {}
                r_dict['id'] = id
                id = id + 1
                r_dict['name'] = name_one
                pages = []
                # for 订餐结果表_one in 订餐结果表_all:
                #     订餐主界面表_first = 订餐主界面表.objects(手机号=订餐结果表_one.手机号, 三级部门=name_one).first()
                #     if 订餐主界面表_first == None:
                #         continue
                #     else:
                #         rr_dict = {}
                        # if 子菜单page_desc == 早餐外带统计:
                        #     if 订餐结果表_one.早餐食堂就餐签到 == 没吃:
                        #         rr_dict['page_name'] = 订餐主界面表_first.姓名
                        #         rr_dict['shu_liang'] = 订餐结果表_one.早餐食堂外带预订数
                        #         rr_dict['page_desc'] = 订餐结果表_one.早餐食堂就餐签到
                        #         pages.append(rr_dict)
                        # elif 子菜单page_desc == 中餐外带统计:
                        #     if 订餐结果表_one.中餐食堂就餐签到 == 没吃:
                        #         rr_dict['page_name'] = 订餐主界面表_first.姓名
                        #         rr_dict['shu_liang'] = 订餐结果表_one.中餐食堂外带预订数
                        #         rr_dict['page_desc'] = 订餐结果表_one.中餐食堂就餐签到
                        #         pages.append(rr_dict)
                        # elif 子菜单page_desc == 晚餐外带统计:
                        #     if 订餐结果表_one.晚餐食堂就餐签到 == 没吃:
                        #         rr_dict['page_name'] = 订餐主界面表_first.姓名
                        #         rr_dict['shu_liang'] = 订餐结果表_one.晚餐食堂外带预订数
                        #         rr_dict['page_desc'] = 订餐结果表_one.晚餐食堂就餐签到
                        #         pages.append(rr_dict)
                        # elif 子菜单page_desc == 早餐统计:
                        #     if 订餐结果表_one.子菜单page_name == 青阳食堂:
                        #         rr_dict['page_name'] = 订餐主界面表_first.姓名
                        #         rr_dict['shu_liang'] = 订餐结果表_one.早餐食堂外带预订数
                        #         rr_dict['page_desc'] = 订餐结果表_one.早餐食堂就餐签到
                        #         pages.append(rr_dict)
                        #     else:
                        #         if 订餐结果表_one.早餐食堂就餐签到 == 没吃:
                        #             rr_dict['page_name'] = 订餐主界面表_first.姓名
                        #             rr_dict['shu_liang'] = 订餐结果表_one.早餐食堂就餐预订数
                        #             rr_dict['page_desc'] = 订餐结果表_one.早餐食堂就餐签到
                        #             pages.append(rr_dict)
                        # elif 子菜单page_desc == 中餐统计:
                        #     if 订餐结果表_one.子菜单page_name == 青阳食堂:
                        #         rr_dict['page_name'] = 订餐主界面表_first.姓名
                        #         rr_dict['shu_liang'] = 订餐结果表_one.中餐食堂就餐预订数
                        #         rr_dict['page_desc'] = 订餐结果表_one.中餐食堂就餐签到
                        #         pages.append(rr_dict)
                        #     else:
                        #         if 订餐结果表_one.中餐食堂就餐签到 == 没吃:
                        #             rr_dict['page_name'] = 订餐主界面表_first.姓名
                        #             rr_dict['shu_liang'] = 订餐结果表_one.中餐食堂就餐预订数
                        #             rr_dict['page_desc'] = 订餐结果表_one.中餐食堂就餐签到
                        #             pages.append(rr_dict)
                        # elif 子菜单page_desc == 晚餐统计:
                        #     if 订餐结果表_one.子菜单page_name == 青阳食堂:
                        #         rr_dict['page_name'] = 订餐主界面表_first.姓名
                        #         rr_dict['shu_liang'] = 订餐结果表_one.晚餐食堂就餐预订数
                        #         rr_dict['page_desc'] = 订餐结果表_one.晚餐食堂就餐签到
                        #         pages.append(rr_dict)
                        #     else:
                        #         if 订餐结果表_one.晚餐食堂就餐签到 == 没吃:
                        #             rr_dict['page_name'] = 订餐主界面表_first.姓名
                        #             rr_dict['shu_liang'] = 订餐结果表_one.晚餐食堂就餐预订数
                        #             rr_dict['page_desc'] = 订餐结果表_one.晚餐食堂就餐签到
                        #             pages.append(rr_dict)
                        # else:
                        #     pass
                r_dict['num'] = len(pages)
                if r_dict['num'] == 0:
                    pass
                else:
                    r_dict['pages'] = pages
                    r_list.append(r_dict)
            描述 = '下载成功'
            app_tittle = 子菜单page_desc
            app_des = '总人数 ' + str(总人数) + ';总份数' + str(总份数)
            app_code_des = '吃过人数 ' + str(吃过人数) + ';吃过份数' + str(吃过份数)
            app_code = '没吃人数' + str(没吃人数) + ';没吃份数' + str(没吃份数)
            自定义登录状态 = {'描述': 描述, '会话': '23456', 'list': r_list, 'app_tittle': app_tittle, 'app_des': app_des,
                'app_code_des': app_code_des, 'app_code': app_code, 'date': 日期, 'start_date': 第一天, 'end_date': 第三天}
            订餐统计结果_first = 订餐统计结果.objects(日期=日期, 子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc).first()
            if 订餐统计结果_first == None:
                订餐统计结果(日期=日期, 子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc, 订餐结果=自定义登录状态).save()
            else:
                订餐统计结果_first.update(订餐结果=自定义登录状态)

@deprecated_async
def 异步统计产品(食堂名称,二级部门,wx_login_get_openid_dict):
    第一天 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    第二天 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400))
    第三天 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400 + 86400))
    日期_list = [第一天, 第二天, 第三天]
    # 订餐部门表_first = 订餐部门表.objects(二级部门=二级部门).first()
    from . import models
    qset1 = models.订餐主界面表.objects(二级部门=二级部门)
    name_list = []
    for one in qset1:
        三级部门 = one.三级部门
        if 三级部门 in name_list:
            pass
        else:
            name_list.append(三级部门)
    for 日期_list_one in 日期_list:
        日期 = 日期_list_one
        from . import models
        for 产品 in models.产品全局字典[wx_login_get_openid_dict['app_id']]['产品列表']:
            产品名称 = 产品['名称']
            pipeline = [
                {
                    "$match": {
                        "产品."+产品名称+".预定数量": {
                            "$gte":1
                        },
                        "用餐日期":日期
                    }
                }
            ]
            总人数 = len(list(models.订餐结果表.objects.aggregate(*pipeline)))
            pipeline2 = [
                    {
                    "$match": {
                        "产品."+产品名称+".预定数量": {
                            "$gte":1
                        },
                        "产品."+产品名称+".签到":"没吃",
                        "用餐日期":日期_list_one
                    }
                }
            ]
            没吃人数 = len(list(models.订餐结果表.objects.aggregate(*pipeline2)))
            pipeline3 = [
                    {
                    "$match": {
                        "产品."+产品名称+".预定数量": {
                            "$gte":1
                        },
                        "产品."+产品名称+".签到":"吃过",
                        "用餐日期":日期_list_one
                    }
                }
            ]
            吃过人数 = len(list(models.订餐结果表.objects.aggregate(*pipeline3)))
            pipeline4 = [
                {
                    "$match": {
                        "产品."+产品名称+".预定数量": {
                            "$gte":1
                        },
                        "用餐日期":日期_list_one
                    }
                }
                ,
                {
                    "$group": {
                        "_id": "null",
                        产品名称: {
                            "$sum": "$产品."+产品名称+".预定数量"
                        }
                    }
                }
            ]
            总份数 = 0
            for r in list(models.订餐结果表.objects.aggregate(*pipeline4)):
                总份数 = r[产品名称]
            pipeline5 = [
                {
                    "$match": {
                        "产品."+产品名称+".预定数量": {
                            "$gte":1
                        },
                        "产品."+产品名称+".签到":"没吃",
                        "用餐日期":日期_list_one
                    }
                }
                ,
                {
                    "$group": {
                        "_id": "null",
                        产品名称: {
                            "$sum": "$产品."+产品名称+".预定数量"
                        }
                    }
                }
            ]
            没吃份数 = 0
            for r in list(models.订餐结果表.objects.aggregate(*pipeline5)):
                没吃份数 = r[产品名称]
            pipeline6 = [
                {
                    "$match": {
                        "产品."+产品名称+".预定数量": {
                            "$gte":1
                        },
                        "产品."+产品名称+".签到":"吃过",
                        "用餐日期":日期_list_one
                    }
                }
                ,
                {
                    "$group": {
                        "_id": "null",
                        产品名称: {
                            "$sum": "$产品."+产品名称+".预定数量"
                        }
                    }
                }
            ]
            吃过份数 = 0
            for r in list(models.订餐结果表.objects.aggregate(*pipeline6)):
                吃过份数 = r[产品名称]
            r_list = []
            id = 1
            for name_one in name_list:
                r_dict = {}
                r_dict['id'] = id
                id = id + 1
                r_dict['name'] = name_one
                pages = []
                for p in list(models.订餐结果表.objects.aggregate(*pipeline)):
                    订餐主界面表_first = models.订餐主界面表.objects(手机号=p['手机号'], 三级部门=name_one).first()
                    if 订餐主界面表_first == None:
                        continue
                    else:
                        rr_dict = {}
                        if p['产品'][产品名称]['签到'] == 没吃:
                            rr_dict['page_name'] = 订餐主界面表_first.姓名
                            rr_dict['shu_liang'] = p['产品'][产品名称]['预定数量']
                            rr_dict['page_desc'] = p['产品'][产品名称]['签到']
                            pages.append(rr_dict)
                r_dict['num'] = len(pages)
                if r_dict['num'] == 0:
                    pass
                else:
                    r_dict['pages'] = pages
                    r_list.append(r_dict)
            描述 = '下载成功'
            app_tittle = 产品名称
            app_des = '总人数 ' + str(总人数) + ';总份数' + str(总份数)
            app_code_des = '吃过人数 ' + str(吃过人数) + ';吃过份数' + str(吃过份数)
            app_code = '没吃人数' + str(没吃人数) + ';没吃份数' + str(没吃份数)
            自定义登录状态 = {'描述': 描述, '会话': '23456', 'list': r_list, 'app_tittle': app_tittle, 'app_des': app_des,
                'app_code_des': app_code_des, 'app_code': app_code, 'date': 日期, 'start_date': 第一天, 'end_date': 第三天}
            订餐统计结果_first = models.订餐统计结果.objects(日期=日期, 子菜单page_name=食堂名称, 子菜单page_desc=产品名称).first()
            if 订餐统计结果_first == None:
                订餐统计结果(日期=日期, 子菜单page_name=食堂名称, 子菜单page_desc=产品名称, 订餐结果=自定义登录状态).save()
            else:
                订餐统计结果_first.update(订餐结果=自定义登录状态)

def 订餐统计(request):
    日期 = str(request.GET['date'])
    子菜单page_name = str(request.GET['page_name'])
    子菜单page_desc = str(request.GET['page_desc'])
    if 日期 == '':
        日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    订餐统计结果_first = 订餐统计结果.objects(日期=日期, 子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc).first()
    if 订餐统计结果_first == None:
        # start_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # end_date = time.strftime('%Y-%m-%d', time.localtime(time.time() + 259200))
        自定义登录状态 = {'描述': '下载成功', '会话': '123456', 'list': [], 'app_tittle': '订餐统计结果不存在', 'app_des': '请联系管理员',
                   'app_code_des': '', 'app_code': '', 'date': 日期, 'start_date': '', 'end_date': ''}
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)
    else:
        自定义登录状态 = 订餐统计结果_first.订餐结果
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)


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
            自定义登录状态 = {'核销码': '654321', '手机号': '无', '二级部门': '无', '三级部门': '无', '四级部门': '无', '姓名': '无'}
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
    else:
        自定义登录状态 = 订餐中餐核销码表_first.to_json().encode('utf-8').decode('unicode_escape')
    自定义登录状态 = str(自定义登录状态)
    return HttpResponse(自定义登录状态)


# def 订餐扫核销码2(request):
#     核销码 = str(request.GET['er_wei_ma'])
#     主菜单name = str(request.GET['name'])
#     子菜单page_name = str(request.GET['page_name'])
#     子菜单page_desc = str(request.GET['page_desc'])
#     if 核销码 == '123456':
#         当前日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
#         当前小时 = time.strftime('%H', time.localtime(time.time()))
#         js_code = request.GET['code']
#         wx_login_get_openid_dict = tool.wx_login_get_openid(request)
#         session_key = ''
#         openid=wx_login_get_openid_dict['openid']
#         订餐用户表_first = 订餐用户表.objects(openid=wx_login_get_openid_dict['openid']).first()
#         if 订餐用户表_first == None:
#             自定义登录状态 = {'描述': '未注册手机号', '姓名': '', '当前日期': '', '类型': ''}
#             自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
#             自定义登录状态 = str(自定义登录状态)
#             return HttpResponse(自定义登录状态)
#         手机号 = 订餐用户表_first.手机号
#         # 订餐主界面表_first = 订餐主界面表.objects(手机号=手机号).first()
#         # 订餐结果表_first = 订餐结果表.objects(主菜单name=主菜单name, 子菜单page_name=子菜单page_name, 手机号=手机号, 用餐日期=当前日期).first()
#         订餐结果表_first = 订餐结果表.objects(手机号=手机号, 用餐日期=当前日期).first()
#         if 订餐结果表_first == None:
#             自定义登录状态 = {'描述': '没有订餐', '姓名': '', '当前日期': '', '类型': ''}
#             自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
#             自定义登录状态 = str(自定义登录状态)
#             return HttpResponse(自定义登录状态)
#         else:
#             if 子菜单page_name == '' or 子菜单page_name == None:
#                 子菜单page_name = 订餐结果表_first.子菜单page_name
#             if 当前小时 > '05' and 当前小时 < '09':
#                 if 订餐结果表_first.早餐食堂就餐签到 == 没吃:
#                     订餐结果表_first.update(早餐食堂就餐签到=吃过)
#                     异步计算消费金额(wx_login_get_openid_dict)
#                     自定义登录状态 = {'描述': '成功', '姓名': 订餐主界面表_first.姓名, '当前日期': 当前日期, '类型': '早餐核销'}
#                     自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
#                     自定义登录状态 = str(自定义登录状态)
#                     # 异步计算订餐结果(子菜单page_name, 订餐主界面表_first.二级部门)
#                     异步统计产品(子菜单page_name, 订餐主界面表_first.二级部门,wx_login_get_openid_dict)
#                     return HttpResponse(自定义登录状态)
#                 elif 订餐结果表_first.早餐食堂就餐签到 == 吃过:
#                     自定义登录状态 = {'描述': '成功', '姓名': 订餐主界面表_first.姓名, '当前日期': 当前日期, '类型': '早餐核销'}
#                     自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
#                     自定义登录状态 = str(自定义登录状态)
#                     return HttpResponse(自定义登录状态)
#                 else:
#                     自定义登录状态 = {'描述': '已经吃过或者已取消', '姓名': '', '当前日期': '', '类型': ''}
#                     自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
#                     自定义登录状态 = str(自定义登录状态)
#                     return HttpResponse(自定义登录状态)
#             elif 当前小时 > '10' and 当前小时 < '15':
#                 if 订餐结果表_first.中餐食堂就餐签到 == 没吃:
#                     订餐结果表_first.update(中餐食堂就餐签到=吃过)
#                     异步计算消费金额(wx_login_get_openid_dict)
#                     自定义登录状态 = {'描述': '成功', '姓名': 订餐主界面表_first.姓名, '当前日期': 当前日期, '类型': '中餐核销'}
#                     自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
#                     自定义登录状态 = str(自定义登录状态)
#                     # 异步计算订餐结果(子菜单page_name, 订餐主界面表_first.二级部门)
#                     异步统计产品(子菜单page_name, 订餐主界面表_first.二级部门,wx_login_get_openid_dict)
#                     return HttpResponse(自定义登录状态)
#                 elif 订餐结果表_first.中餐食堂就餐签到 == 吃过:
#                     自定义登录状态 = {'描述': '成功', '姓名': 订餐主界面表_first.姓名, '当前日期': 当前日期, '类型': '中餐核销'}
#                     自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
#                     自定义登录状态 = str(自定义登录状态)
#                     return HttpResponse(自定义登录状态)
#                 else:
#                     自定义登录状态 = {'描述': '已经吃过或者已取消', '姓名': '', '当前日期': '', '类型': ''}
#                     自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
#                     自定义登录状态 = str(自定义登录状态)
#                     return HttpResponse(自定义登录状态)
#             elif 当前小时 > '16' and 当前小时 < '20':
#                 if 订餐结果表_first.晚餐食堂就餐签到 == 没吃:
#                     订餐结果表_first.update(晚餐食堂就餐签到=吃过)
#                     异步计算消费金额(wx_login_get_openid_dict)
#                     自定义登录状态 = {'描述': '成功', '姓名': 订餐主界面表_first.姓名, '当前日期': 当前日期, '类型': '晚餐核销'}
#                     自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
#                     自定义登录状态 = str(自定义登录状态)
#                     # 异步计算订餐结果(子菜单page_name, 订餐主界面表_first.二级部门)
#                     异步统计产品(子菜单page_name, 订餐主界面表_first.二级部门,wx_login_get_openid_dict)
#                     return HttpResponse(自定义登录状态)
#                 elif 订餐结果表_first.晚餐食堂就餐签到 == 吃过:
#                     自定义登录状态 = {'描述': '成功', '姓名': 订餐主界面表_first.姓名, '当前日期': 当前日期, '类型': '晚餐核销'}
#                     自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
#                     自定义登录状态 = str(自定义登录状态)
#                     return HttpResponse(自定义登录状态)
#                 else:
#                     自定义登录状态 = {'描述': '已经吃过或者已取消', '姓名': '', '当前日期': '', '类型': ''}
#                     自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
#                     自定义登录状态 = str(自定义登录状态)
#                     return HttpResponse(自定义登录状态)
#             else:
#                 自定义登录状态 = {'描述': '不在就餐时间', '姓名': '', '当前日期': '', '类型': ''}
#                 自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
#                 自定义登录状态 = str(自定义登录状态)
#                 return HttpResponse(自定义登录状态)

#     else:
#         自定义登录状态 = {'描述': '这不是核销码', '姓名': '', '当前日期': '', '类型': ''}
#         自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
#         自定义登录状态 = str(自定义登录状态)
#         return HttpResponse(自定义登录状态)

def ding_can_sao_he_xiao_ma2(request):
    from bson.objectid import ObjectId
    from . import models as ding_can_mongo  #新版订餐后台
    try:
        核销码 = str(request.GET['er_wei_ma'])
        # 主菜单name = str(request.GET['name'])
        # 子菜单page_name = str(request.GET['page_name'])
        # 子菜单page_desc = str(request.GET['page_desc'])
        # js_code = request.GET['code']
        核销码 = 核销码.encode('utf8')[3:].decode('utf8')
        print(核销码,'---------------------------ding_can_sao_he_xiao_ma2--------')
        核销码json = json.loads(核销码)
        日期 = 核销码json['date']
        当前日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        if 日期 == '':
            日期 = 当前日期
        产品名称 = 核销码json['name']
        oid = 核销码json['oid']
        wx_login_get_openid_dict = tool.wx_login_get_openid(request)
        订餐用户表_one = 订餐用户表.objects(openid=wx_login_get_openid_dict['openid']).first()
        if 订餐用户表_one == None:
            自定义登录状态 = {'描述': '管理员未注册', '姓名': '', '当前日期': '', '类型': ''}
            return myHttpResponse(自定义登录状态)
        else:
            key = 核销码json['key']
            if key == '预定码':
                qset1 = ding_can_mongo.订餐结果表.objects(
                    id=ObjectId(oid),
                    用餐日期=当前日期
                ).first()
                if qset1 == None:
                    自定义登录状态 = {'描述': '今日无订餐记录', '姓名': '', '当前日期': '', '类型': ''}
                    return myHttpResponse(自定义登录状态)
                else:
                    产品 = qset1.产品
                    if 产品[产品名称]['预定数量'] == 0:
                        自定义登录状态 = {'描述': '订餐数量为0，不能核销', '姓名': '', '当前日期': '', '类型': ''}
                        return myHttpResponse(自定义登录状态)
                    if 产品[产品名称]['签到'] == '吃过':
                        自定义登录状态 = {'描述': '已吃过，不能重复核销', '姓名': '', '当前日期': '', '类型': ''}
                        return myHttpResponse(自定义登录状态)
                    产品[产品名称]['签到'] = '吃过'
                    产品[产品名称]['签到时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    qset1.update(产品=产品)
                    顾客手机号 = qset1.手机号
                    订餐用户表1330 = ding_can_mongo.订餐用户表.objects(手机号=顾客手机号).first()
                    if 订餐用户表1330 == None:
                        res = {'描述': '顾客信息不存在', '姓名': '', '当前日期': '', '类型': ''}
                        return myHttpResponse(res)
                    print(顾客手机号)
                    qset2 = ding_can_mongo.订餐钱包表.objects(openid = 订餐用户表1330.openid).first()
                    if qset2 == None:
                        res = {'描述': '钱包无记录，系统异常', '姓名': '', '当前日期': '', '类型': ''}
                        return myHttpResponse(res)
                    else:
                        已消费 = qset2.已消费
                        预消费 = qset2.预消费
                        已消费 = 已消费 + ( int(产品[产品名称]['价格']) * int(产品[产品名称]['预定数量']) )
                        预消费 = 预消费 - ( int(产品[产品名称]['价格']) * int(产品[产品名称]['预定数量']) )
                        qset2.update(已消费=已消费,预消费=预消费)
                        订餐主界面表1 = ding_can_mongo.订餐主界面表.objects(手机号=qset1.手机号).first()
                        食堂名称 = qset1.子菜单page_name
                        二级部门 = 订餐主界面表1.二级部门
                        异步统计产品(食堂名称=食堂名称,二级部门=二级部门,wx_login_get_openid_dict=wx_login_get_openid_dict)
                        自定义登录状态 = {'描述': '成功', 
                            '订餐结果': '姓名：'+订餐主界面表1.姓名+',预定数量：'+str(产品[产品名称]['预定数量'])+',产品名称：'+产品名称
                        }
                        return myHttpResponse(自定义登录状态)
            elif key == '非预定码':
                qset1 = ding_can_mongo.订餐结果表.objects(
                    id=ObjectId(oid),
                    用餐日期=当前日期
                ).first()
                if qset1 == None:
                    自定义登录状态 = {'描述': '今日无订餐记录', '姓名': '', '当前日期': '', '类型': ''}
                    return myHttpResponse(自定义登录状态)
                else:
                    产品 = qset1.产品
                    if 产品[产品名称]['预定数量'] == 0:
                        自定义登录状态 = {'描述': '订餐数量为0，不能核销', '姓名': '', '当前日期': '', '类型': ''}
                        return myHttpResponse(自定义登录状态)
                    if 产品[产品名称]['签到'] == '吃过':
                        自定义登录状态 = {'描述': '已吃过，不能重复核销', '姓名': '', '当前日期': '', '类型': ''}
                        return myHttpResponse(自定义登录状态)
                    产品[产品名称]['签到'] = '吃过'
                    产品[产品名称]['签到时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    qset1.update(产品=产品)
                    顾客手机号 = qset1.手机号
                    订餐用户表1330 = ding_can_mongo.订餐用户表.objects(手机号=顾客手机号).first()
                    if 订餐用户表1330 == None:
                        res = {'描述': '顾客信息不存在', '姓名': '', '当前日期': '', '类型': ''}
                        return myHttpResponse(res)
                    qset2 = ding_can_mongo.订餐钱包表.objects(openid = 订餐用户表1330.openid).first()
                    if qset2 == None:
                        res = {'描述': '钱包无记录，系统异常', '姓名': '', '当前日期': '', '类型': ''}
                        return myHttpResponse(res)
                    else:
                        已消费 = qset2.已消费
                        预消费 = qset2.预消费
                        已消费 = 已消费 + ( int(产品[产品名称]['价格']) * int(产品[产品名称]['预定数量']) )
                        预消费 = 预消费 - ( int(产品[产品名称]['价格']) * int(产品[产品名称]['预定数量']) )
                        qset2.update(已消费=已消费,预消费=预消费)
                        订餐主界面表1 = ding_can_mongo.订餐主界面表.objects(手机号=qset1.手机号).first()
                        食堂名称 = qset1.子菜单page_name
                        二级部门 = 订餐主界面表1.二级部门
                        异步统计产品(食堂名称=食堂名称,二级部门=二级部门,wx_login_get_openid_dict=wx_login_get_openid_dict)
                        自定义登录状态 = {'描述': '成功', 
                            '订餐结果': '姓名：'+订餐主界面表1.姓名+',预定数量：'+str(产品[产品名称]['预定数量'])+',产品名称：'+产品名称
                        }
                        return myHttpResponse(自定义登录状态)
            else:
                自定义登录状态 = {'描述': '核销码key错误', '姓名': '', '当前日期': '', '类型': ''}
                return myHttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        自定义登录状态 = {'描述': '系统错误', '姓名': '', '当前日期': '', '类型': ''}
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
        wx_login_get_openid_dict = tool.wx_login_get_openid(request)
        订餐用户表_first = 订餐用户表.objects(openid=wx_login_get_openid_dict['openid']).first()
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
                    订餐核销码表_first.update(核销码=session_key, 手机号=手机号, 二级部门=订餐主界面表_first.二级部门, 三级部门=订餐主界面表_first.三级部门,
                                        四级部门=订餐主界面表_first.四级部门, 姓名=订餐主界面表_first.姓名)
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
                    订餐核销码表_first.update(核销码=session_key, 手机号=手机号, 二级部门=订餐主界面表_first.二级部门, 三级部门=订餐主界面表_first.三级部门,
                                        四级部门=订餐主界面表_first.四级部门, 姓名=订餐主界面表_first.姓名)
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
                自定义登录状态 = {'描述': '错误'}
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)


def ding_can_xia_zai_mp3(request):
    mp3_text = str(request.GET['mp3_text'])
    from aip import AipSpeech
    """ 你的 APPID AK SK """
    APP_ID = '15273029'
    API_KEY = 'skY2wM5whRPfHgC7vc9DrsmW'
    SECRET_KEY = 'UblS7MlmG30UWZjKCLL8p5HEZ9M0SG1A '
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.synthesis(mp3_text, 'zh', 1, {'vol': 5, 'per': 0,'spd':2})
    response = HttpResponse(result)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="auido.mp3"'
    return response


def 订餐订单(request):
    try:
        page_name = request.GET['page_name']
        日期 = request.GET['date']
        js_code = request.GET['code']
        wx_login_get_openid_dict = tool.wx_login_get_openid(request)
        当前日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        if 日期 == '':
            日期 = 当前日期
        开始日期 = time.strftime('%Y-%m-%d', time.localtime(time.time() - 864000))
        结束日期 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 864000))
        订餐用户表_one = 订餐用户表.objects(openid=wx_login_get_openid_dict['openid']).first()
        if 订餐用户表_one == None:
            描述 = '用户不存在'
            自定义登录状态 = {'描述': 描述, '日期': 日期, '开始日期': 开始日期, '结束日期': 结束日期, '会话': ''}
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            手机号 = 订餐用户表_one.手机号
            订餐结果表_first = 订餐结果表.objects(手机号=手机号, 用餐日期=日期).first()
            if 订餐结果表_first == None:
                描述 = '没有订餐记录'
                自定义登录状态 = {'描述': 描述, '日期': 日期, '开始日期': 开始日期, '结束日期': 结束日期, '会话': ''}
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
            else:
                订餐主界面表_first = 订餐主界面表.objects(手机号=手机号).first()
                订餐食堂模版表_first = 订餐食堂模版表.objects(子菜单page_name=page_name).first()
                if 订餐食堂模版表_first == None:
                    描述 = '没有食堂数据'
                    自定义登录状态 = {'描述': 描述, '会话': ''}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                if 订餐主界面表_first == None:
                    描述 = '您没有权限'
                    自定义登录状态 = {'描述': 描述, '会话': ''}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                描述 = '下载成功'
                自定义登录状态 = {'描述': 描述, '会话': '', '主菜单name': 订餐结果表_first.主菜单name,
                           '子菜单page_name': 订餐结果表_first.子菜单page_name, '子菜单page_desc': 订餐结果表_first.子菜单page_desc,
                           '姓名': 订餐主界面表_first.姓名, '食堂地址': 订餐食堂模版表_first.食堂地址, '日期': 日期, '开始日期': 开始日期, '结束日期': 结束日期,

                           '早餐食堂就餐预订数': 订餐结果表_first.早餐食堂就餐预订数, '早餐价格': 订餐食堂模版表_first.早餐价格,
                           '早餐食堂就餐签到': 订餐结果表_first.早餐食堂就餐签到, '早餐订餐时间': 订餐结果表_first.早餐订餐时间, '早餐取消时间': 订餐结果表_first.早餐取消时间,

                           '中餐食堂就餐预订数': 订餐结果表_first.中餐食堂就餐预订数, '中餐价格': 订餐食堂模版表_first.中餐价格,
                           '中餐食堂就餐签到': 订餐结果表_first.中餐食堂就餐签到, '中餐订餐时间': 订餐结果表_first.中餐订餐时间, '中餐取消时间': 订餐结果表_first.中餐取消时间,
                           '晚餐食堂就餐预订数': 订餐结果表_first.晚餐食堂就餐预订数, '晚餐食堂就餐签到': 订餐结果表_first.晚餐食堂就餐签到,
                           '晚餐价格': 订餐食堂模版表_first.晚餐价格, '晚餐订餐时间': 订餐结果表_first.晚餐订餐时间, '晚餐取消时间': 订餐结果表_first.晚餐取消时间}
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
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
        wx_login_get_openid_dict = tool.wx_login_get_openid(request)
        当前时间戳 = time.time()
        当前日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        当前时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if 日期 == '':
            日期 = 当前日期
        开始日期 = time.strftime('%Y-%m-%d', time.localtime(time.time() - 864000))
        结束日期 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 864000))
        openid=wx_login_get_openid_dict['openid']
        订餐用户表_one = 订餐用户表.objects(openid=wx_login_get_openid_dict['openid']).first()
        if 订餐用户表_one == None:
            自定义登录状态 = "{\"描述\":\"用户不存在\",\"会话\":\"\"}"
            return HttpResponse(自定义登录状态)
        else:
            手机号 = 订餐用户表_one.手机号
            订餐结果表_first = 订餐结果表.objects(手机号=手机号, 用餐日期=日期).first()
            if 订餐结果表_first == None:
                描述 = '没有订餐记录'
                自定义登录状态 = {'描述': 描述, '会话': ''}
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
            else:
                订餐主界面表_first = 订餐主界面表.objects(手机号=手机号).first()
                订餐食堂模版表_first = 订餐食堂模版表.objects(子菜单page_name=page_name).first()
                if 订餐食堂模版表_first == None:
                    描述 = '没有食堂数据'
                    自定义登录状态 = {'描述': 描述, '会话': ''}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                if 订餐主界面表_first == None:
                    描述 = '您没有权限'
                    自定义登录状态 = {'描述': 描述, '会话': ''}
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
                                    # 异步计算订餐结果(page_name, 订餐主界面表_first.二级部门)
                                    异步统计产品(子菜单page_name, 订餐主界面表_first.二级部门,wx_login_get_openid_dict)
                                    异步计算消费金额(wx_login_get_openid_dict)
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
                                    # 异步计算订餐结果(page_name, 订餐主界面表_first.二级部门)
                                    异步统计产品(子菜单page_name, 订餐主界面表_first.二级部门,wx_login_get_openid_dict)
                                    异步计算消费金额(wx_login_get_openid_dict)
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
                                    # 异步计算订餐结果(page_name, 订餐主界面表_first.二级部门)
                                    异步统计产品(子菜单page_name, 订餐主界面表_first.二级部门,wx_login_get_openid_dict)
                                    异步计算消费金额(wx_login_get_openid_dict)
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
                自定义登录状态 = {'描述': 描述, '会话': '', '主菜单name': 订餐结果表_second.主菜单name,
                           '子菜单page_name': 订餐结果表_second.子菜单page_name, '子菜单page_desc': 订餐结果表_second.子菜单page_desc,
                           '姓名': 订餐主界面表_first.姓名, '食堂地址': 订餐食堂模版表_first.食堂地址, '日期': 日期, '开始日期': 开始日期, '结束日期': 结束日期,

                           '早餐食堂就餐预订数': 订餐结果表_second.早餐食堂就餐预订数, '早餐价格': 订餐食堂模版表_first.早餐价格,
                           '早餐食堂就餐签到': 订餐结果表_second.早餐食堂就餐签到, '早餐订餐时间': 订餐结果表_second.早餐订餐时间,
                           '早餐取消时间': 订餐结果表_second.早餐取消时间,

                           '中餐食堂就餐预订数': 订餐结果表_second.中餐食堂就餐预订数, '中餐价格': 订餐食堂模版表_first.中餐价格,
                           '中餐食堂就餐签到': 订餐结果表_second.中餐食堂就餐签到, '中餐订餐时间': 订餐结果表_second.中餐订餐时间,
                           '中餐取消时间': 订餐结果表_second.中餐取消时间,

                           '晚餐食堂就餐预订数': 订餐结果表_second.晚餐食堂就餐预订数, '晚餐食堂就餐签到': 订餐结果表_second.晚餐食堂就餐签到,
                           '晚餐价格': 订餐食堂模版表_first.晚餐价格, '晚餐订餐时间': 订餐结果表_second.晚餐订餐时间, '晚餐取消时间': 订餐结果表_second.晚餐取消时间}
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
        wx_login_get_openid_dict = tool.wx_login_get_openid(request)
        用户 = 订餐用户表.objects(openid=wx_login_get_openid_dict['openid']).first()
        if 用户 == None:
            自定义登录状态 = {'描述': '未注册手机号', 'name': name, 'page_name': page_name, 'page_desc': page_desc,
                'lou_yu_list': [], }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        主界面表first = 订餐主界面表.objects(手机号=用户.手机号).first()
        if 主界面表first == None:
            自定义登录状态 = {'描述': '没有权限', 'name': name, 'page_name': page_name, 'page_desc': page_desc, 'lou_yu_list': [], }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)

        异步计算菜单(page_name)
        订餐菜单表first = 订餐菜单表.objects(食堂名称=page_name).first()
        if 订餐菜单表first == None:
            分工list = [{'dan_yuan_id': 0, 'dan_yuan_name': '2019-03-31_市公司食堂_中餐', 'dan_yuan': [{'lou_ceng_id': 0,
                'ceng': [
                    {'men_pai_id': '2019-03-31_市公司食堂_中餐_青菜', 'men_pai_hao': '青菜', 'zhuang_tai': 'placeholder_grey'},
                    {'men_pai_id': '2019-03-31_市公司食堂_中餐_白菜', 'men_pai_hao': '白菜', 'zhuang_tai': 'placeholder_red'},
                    {'men_pai_id': '2019-03-31_市公司食堂_中餐_黄花菜', 'men_pai_hao': '黄花菜',
                        'zhuang_tai': 'placeholder_grey'}, ]}, {'lou_ceng_id': 1,
                'ceng': [{'men_pai_id': '2019-03-31_市公司食堂_中餐_黄鱼', 'men_pai_hao': '黄鱼', 'zhuang_tai': 'placeholder_red'},
                    {'men_pai_id': '2019-03-31_市公司食堂_中餐_泥鳅', 'men_pai_hao': '泥鳅', 'zhuang_tai': 'placeholder_red'},
                    {'men_pai_id': '2019-03-31_市公司食堂_中餐_咸鱼', 'men_pai_hao': '咸鱼',
                        'zhuang_tai': 'placeholder_red'}, ]}, ]},
                {'dan_yuan_id': 1, 'dan_yuan_name': '2019-03-31_市公司食堂_晚餐', 'dan_yuan': [{'lou_ceng_id': 0, 'ceng': [
                    {'men_pai_id': '2019-03-31_市公司食堂_晚餐_青菜', 'men_pai_hao': '青菜', 'zhuang_tai': 'placeholder_green'},
                    {'men_pai_id': '2019-03-31_市公司食堂_晚餐_白菜', 'men_pai_hao': '白菜', 'zhuang_tai': 'placeholder_green'},
                    {'men_pai_id': '2019-03-31_市公司食堂_晚餐_黄花菜', 'men_pai_hao': '黄花菜',
                        'zhuang_tai': 'placeholder_green'}, ]}, {'lou_ceng_id': 1, 'ceng': [
                    {'men_pai_id': '2019-03-31_市公司食堂_晚餐_黄鱼', 'men_pai_hao': '黄鱼', 'zhuang_tai': 'placeholder_green'},
                    {'men_pai_id': '2019-03-31_市公司食堂_晚餐_泥鳅', 'men_pai_hao': '泥鳅', 'zhuang_tai': 'placeholder_green'},
                    {'men_pai_id': '2019-03-31_市公司食堂_晚餐_咸鱼', 'men_pai_hao': '咸鱼',
                        'zhuang_tai': 'placeholder_green'}, ]}, ]}, ]
        else:
            分工list = 订餐菜单表first.菜单列表
        分工list_len = len(分工list)
        分工list_len_取整除 = 分工list_len // 订餐菜单分页
        分工list_len_取整除 = 分工list_len_取整除 + 1
        countries = list(range(0, 分工list_len_取整除))
        countries_val = 0
        分工list_slice = 分工list[countries_val * 订餐菜单分页: (countries_val + 1) * 订餐菜单分页]
        自定义登录状态 = {'描述': '成功', 'name': name, 'page_name': page_name, 'page_desc': page_desc, 'countries': countries,
            'lou_yu_list': 分工list_slice, }
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
        wx_login_get_openid_dict = tool.wx_login_get_openid(request)
        用户 = 订餐用户表.objects(openid=wx_login_get_openid_dict['openid']).first()
        if 用户 == None:
            自定义登录状态 = {'描述': '未注册手机号', 'name': name, 'page_name': page_name, 'page_desc': page_desc,
                'lou_yu_list': [], }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        主界面表first = 订餐主界面表.objects(手机号=用户.手机号).first()
        if 主界面表first == None:
            自定义登录状态 = {'描述': '没有权限', 'name': name, 'page_name': page_name, 'page_desc': page_desc, 'lou_yu_list': [], }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        录入分工表first = 订餐菜单表.objects(食堂名称=page_name).first()
        if 录入分工表first == None:
            分工list = [{'dan_yuan_id': 0, 'dan_yuan_name': '2019-03-31_中餐', 'dan_yuan': [{'lou_ceng_id': 0,
                'ceng': [{'men_pai_id': '2019-03-31_中餐_青菜', 'men_pai_hao': '青菜', 'zhuang_tai': 'placeholder_red'},
                    {'men_pai_id': '2019-03-31_中餐_白菜', 'men_pai_hao': '白菜', 'zhuang_tai': 'placeholder_red'},
                    {'men_pai_id': '2019-03-31_中餐_黄花菜', 'men_pai_hao': '黄花菜', 'zhuang_tai': 'placeholder_red'},

                ]}, {'lou_ceng_id': 1,
                'ceng': [{'men_pai_id': '2019-03-31_中餐_黄鱼', 'men_pai_hao': '黄鱼', 'zhuang_tai': 'placeholder_red'},
                    {'men_pai_id': '2019-03-31_中餐_泥鳅', 'men_pai_hao': '泥鳅', 'zhuang_tai': 'placeholder_red'},
                    {'men_pai_id': '2019-03-31_中餐_咸鱼', 'men_pai_hao': '咸鱼', 'zhuang_tai': 'placeholder_red'},

                ]}, ]

            }, {'dan_yuan_id': 1, 'dan_yuan_name': '2019-03-31_晚餐', 'dan_yuan': [{'lou_ceng_id': 0,
                'ceng': [{'men_pai_id': '2019-03-31_晚餐_青菜', 'men_pai_hao': '青菜', 'zhuang_tai': 'placeholder_green'},
                    {'men_pai_id': '2019-03-31_晚餐_白菜', 'men_pai_hao': '白菜', 'zhuang_tai': 'placeholder_green'},
                    {'men_pai_id': '2019-03-31_晚餐_黄花菜', 'men_pai_hao': '黄花菜', 'zhuang_tai': 'placeholder_green'},

                ]}, {'lou_ceng_id': 1,
                'ceng': [{'men_pai_id': '2019-03-31_晚餐_黄鱼', 'men_pai_hao': '黄鱼', 'zhuang_tai': 'placeholder_green'},
                    {'men_pai_id': '2019-03-31_晚餐_泥鳅', 'men_pai_hao': '泥鳅', 'zhuang_tai': 'placeholder_green'},
                    {'men_pai_id': '2019-03-31_晚餐_咸鱼', 'men_pai_hao': '咸鱼', 'zhuang_tai': 'placeholder_green'},

                ]}, ]

            }, ]
        else:
            分工list = 录入分工表first.录入分工
        分工list_slice = 分工list[countries_val * 订餐菜单分页: (countries_val + 1) * 订餐菜单分页]
        自定义登录状态 = {'描述': '成功', 'name': name, 'page_name': page_name, 'page_desc': page_desc,
            'lou_yu_list': 分工list_slice, }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')


def 订餐采集初始化(request):
    try:
        js_code = request.GET['code']
        wx_login_get_openid_dict = tool.wx_login_get_openid(request)
        用户 = 订餐用户表.objects(openid=wx_login_get_openid_dict['openid']).first()
        if 用户 == None:
            自定义登录状态 = {'描述': '未注册手机号', 'countries': [''], 'countries2': [''], 'countries3': [''],
                'chang_suo_lou_yu_zong_dong_shu': '', 'xian_chang_jing_du': '', 'xian_chang_wei_du': '',
                'lou_yu_ceng_shu': '', 'di_xia_shi_ceng_shu': '', 'dian_ti_shu_liang': '', 'dx_xia_zai': '',
                'dx_shang_chuang': '', 'yd_xia_zai': '', 'yd_shang_chuang': '',
                'shi_fou_you_di_xia_ting_cha_chang': False, 'shi_fou_you_yi_wang_shi_feng': False,
                'shi_fou_you_yi_kan_cha': False}
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
        订餐日期 = bindMenPaiHao_id_list[0]
        食堂名称 = bindMenPaiHao_id_list[1]
        订餐类型 = bindMenPaiHao_id_list[2]
        菜谱名称 = bindMenPaiHao_id_list[3]
        订餐菜单评价表first = 订餐菜单评价表.objects(订餐日期=订餐日期, 食堂名称=食堂名称, 订餐类型=订餐类型, 菜谱名称=菜谱名称, ).first()
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
        自定义登录状态 = {'描述': '成功', 'countries': [订餐日期], 'countries2': [食堂名称], 'countries3': [菜谱名称],
            'chang_suo_lou_yu_zong_dong_shu': 场所楼宇总栋数, 'xian_chang_jing_du': 现场经度, 'xian_chang_wei_du': 现场纬度,
            'lou_yu_ceng_shu': 楼宇层数, 'di_xia_shi_ceng_shu': 地下室层数, 'dian_ti_shu_liang': 电梯数量, 'dx_xia_zai': 电信下载速率,
            'dx_shang_chuang': 电信上传速率, 'yd_xia_zai': 移动下载速率, 'yd_shang_chuang': 移动上传速率,
            'shi_fou_you_di_xia_ting_cha_chang': shi_fou_you_di_xia_ting_cha_chang,
            'shi_fou_you_yi_wang_shi_feng': shi_fou_you_yi_wang_shi_feng,
            'shi_fou_you_yi_kan_cha': shi_fou_you_yi_kan_cha, }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')


def 订餐评价初始化(request):
    try:
        js_code = request.GET['code']
        wx_login_get_openid_dict = tool.wx_login_get_openid(request)
        用户 = 订餐用户表.objects(openid=wx_login_get_openid_dict['openid']).first()
        queryset0 = 订餐主界面表.objects(手机号=用户.手机号).first()
        if queryset0 == None:
            自定义登录状态 = {'描述': '用户未授权', 'ping_jia_list': []}
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        订餐评论表objs = 订餐评论表.objects(二级部门=queryset0.二级部门)
        ping_jia_list = []
        for 订餐评论表obj in 订餐评论表objs:
            ping_jia_dict = {'ping_jia_id': 订餐评论表obj.创建时间, 'biao_ti': 订餐评论表obj.手机号, 'nei_rong': 订餐评论表obj.评论内容,
                'image_url': 'https://wx.wuminmin.top/ding_can_image/?obj_id=' + str(订餐评论表obj.id)}
            ping_jia_list.append(ping_jia_dict)
        自定义登录状态 = {'描述': '成功', 'ping_jia_list': ping_jia_list}
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
            wx_login_get_openid_dict = tool.wx_login_get_openid(request)
            用户 = 订餐用户表.objects(openid=wx_login_get_openid_dict['openid']).first()
            if 用户 == None:
                return HttpResponse('未注册手机号')
            订餐主界面表first = 订餐主界面表.objects(手机号=用户.手机号).first()
            if 订餐主界面表first == None:
                return HttpResponse('用户未授权')
            ping_jia_txt = request.GET['ping_jia_txt']
            path = myConfig.django_root_path + '/' + 'mysite' + '/' + '404.png'
            outfile = open(path, 'rb')
            创建时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            订餐评论表(手机号=订餐主界面表first.手机号, 姓名=订餐主界面表first.姓名, 二级部门=订餐主界面表first.二级部门, 三级部门=订餐主界面表first.三级部门,
                四级部门=订餐主界面表first.四级部门, 创建时间=创建时间, 评论内容=ping_jia_txt, 评论图片=outfile).save()
            return HttpResponse('成功')
        if request.method == 'POST':
            js_code = request.POST['code']
            wx_login_get_openid_dict = tool.wx_login_get_openid(request)
            用户 = 订餐用户表.objects(openid=wx_login_get_openid_dict['openid']).first()
            if 用户 == None:
                return HttpResponse('未注册手机号')
            订餐主界面表first = 订餐主界面表.objects(手机号=用户.手机号).first()
            if 订餐主界面表first == None:
                return HttpResponse('用户未授权')
            ping_jia_txt = request.POST['ping_jia_txt']
            tu_pian = request.FILES.get('file')
            订餐评论表first = 订餐评论表.objects(手机号=订餐主界面表first.手机号, 姓名=订餐主界面表first.姓名, 二级部门=订餐主界面表first.二级部门,
                三级部门=订餐主界面表first.三级部门, 四级部门=订餐主界面表first.四级部门, 评论内容=ping_jia_txt, ).first()
            创建时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if 订餐评论表first == None:
                订餐评论表(手机号=订餐主界面表first.手机号, 姓名=订餐主界面表first.姓名, 二级部门=订餐主界面表first.二级部门, 三级部门=订餐主界面表first.三级部门,
                    四级部门=订餐主界面表first.四级部门, 创建时间=创建时间, 评论内容=ping_jia_txt, 评论图片=tu_pian).save()
                return HttpResponse('上传图片成功')
            else:
                订餐评论表first.update(评论图片=tu_pian)
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

#银联支付下订单
def ding_can_chinaums_pay_order(totalAmount,goods,wx_login_get_openid_dict):
    try:
        totalAmount = '1' #支付1分钱
        totalAmount = str(totalAmount)
        print('totalAmount----',totalAmount)
        totalAmount_list = totalAmount.split('.')
        totalAmount = totalAmount_list[0]

        print('ding_can_chinaums_pay_order------------------',wx_login_get_openid_dict)
        scrit_key = myConfig.chinaums_scrit_key
        msgId = myConfig.chinaums_msgId
        msgSrc = myConfig.chinaums_msgSrc
        msgType = myConfig.chinaums_msgType
        requestTimestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        merOrderId = myConfig.chinaums_msgId+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        mid = myConfig.chinaums_mid
        tid = myConfig.chinaums_tid
        instMid = myConfig.chinaums_instMid
        tradeType = myConfig.chinaums_tradeType
        subAppId = myConfig.chinaums_subAppId
        subOpenId = wx_login_get_openid_dict['openid']
        # subOpenId = myConfig.chinaums_subOpenId
        # goods = [
        #     {'body':'微信二维码测试',
        #     'price': '1',
        #     'goodsName': '微信二维码测试',
        #     'goodsId': '1',
        #     'quantity': '1',
        #     'goodsCategory': 'TEST'}
        # ]
        wmm_json = {
            'msgId': msgId, 'msgSrc': msgSrc, 'msgType': msgType, 'requestTimestamp': requestTimestamp,
                'merOrderId': merOrderId, 'mid': mid, 'tid': tid, 'totalAmount': totalAmount,
                'subOpenId': subOpenId,'goods':goods,
                'tradeType': tradeType, 'subAppId': subAppId, 'subOpenId': subOpenId, 'instMid': instMid
            }
        wmm_list = list(wmm_json.keys())
        list.sort(wmm_list)
        wmm_str = ''
        for one in wmm_list:
            if wmm_json[one] == '' or wmm_json[one] == None:
                pass
            else:
                if one == 'goods':
                    wmm_str = wmm_str+one+'='+json.dumps(wmm_json[one]).encode('utf-8').decode('unicode_escape').replace(' ','')+'&'
                else:
                    wmm_str = wmm_str+one+'='+wmm_json[one]+'&'
        wmm_str = wmm_str.rstrip('&')
        wmm_str = wmm_str + scrit_key
        import hashlib
        wmm_sign = hashlib.md5(wmm_str.encode('utf-8')).hexdigest()
        wmm_json['sign'] = wmm_sign
        import requests
        r = requests.post(
            'https://qr.chinaums.com/netpay-route-server/api/', json=wmm_json)
        
        json_res = r.json()
        print(json_res)
        from . import models
        models.ding_can_chinaums_pay_order_res_col(json_res=json_res,openid=wx_login_get_openid_dict['openid']).save()
        if json_res['errCode'] == 'SUCCESS':
            自定义登录状态 = {'描述': '成功', 'miniPayRequest': json_res['miniPayRequest']}
        else:
            自定义登录状态 = {'描述': '失败', 'miniPayRequest': {}}
        return 自定义登录状态
    except:
        print(traceback.format_exc())
        自定义登录状态 = {'描述': '500', 'miniPayRequest': {}}
        return 自定义登录状态

def wx_pay_success(request):
    from . import models
    try:
        app_id = request.GET['app_id']
        state = request.GET['state']
        state_json = json.loads(state)
        oid = state_json['oid']
        totalAmount = state_json['totalAmount']
        子菜单page_name = state_json['子菜单page_name']
        二级部门 = state_json['二级部门']
        wx_login_get_openid_dict = tool.wx_pay_success_get_openid(app_id,oid)
        from bson import ObjectId
        qset1 = models.订餐结果临时表.objects(id=ObjectId(oid)).first()
        if qset1 == None:
            描述 = '订单不存在'
            订餐结果描述 = '订单不存在'
            oid = ''
        else:
            qset3 = models.订餐钱包表.objects(openid=wx_login_get_openid_dict['openid']).first()
            qset2 = models.订餐结果表.objects(
                手机号=qset1.手机号,
                主菜单name=qset1.主菜单name,
                子菜单page_name=qset1.子菜单page_name,
                子菜单page_desc=qset1.子菜单page_desc, 
                用餐日期=qset1.用餐日期).first()
            if qset2 == None:
                models.订餐结果表(
                    手机号=qset1.手机号,
                    主菜单name=qset1.主菜单name,
                    子菜单page_name=qset1.子菜单page_name,
                    子菜单page_desc=qset1.子菜单page_desc, 
                    用餐日期=qset1.用餐日期,
                    产品 = qset1.产品
                ).save()
                异步计算消费金额(wx_login_get_openid_dict)
            else:
                qset2.update(
                    产品 = qset1.产品
                )
                异步计算消费金额(wx_login_get_openid_dict)
            if qset3 == None:
                models.订餐钱包表(
                    openid=wx_login_get_openid_dict['openid'],
                    已充值=totalAmount
                ).save()
            else:
                qset3.update(已充值 = qset3.已充值+totalAmount)
            qset2095 = models.订餐结果表.objects(
                手机号=qset1.手机号,
                子菜单page_name=qset1.子菜单page_name,
                用餐日期=qset1.用餐日期).first()
            oid = str(qset2095.id)
            描述 = '上传成功'
            订餐结果描述 = '上传成功'
        自定义登录状态 = {'描述': 描述,'oid':oid, '会话': '123456', '订餐结果描述': 订餐结果描述}
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        # 异步计算订餐结果(子菜单page_name, 二级部门)
        异步统计产品(子菜单page_name, 二级部门,wx_login_get_openid_dict)
        return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        自定义登录状态 = {'描述': '系统错误', '会话': '123456', '订餐结果描述': '系统错误'}
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        return HttpResponse(自定义登录状态)

@deprecated_async
def async_import_excel(mydata,flag,action):
    # from mysite import ding_can_mongo as ding_can_mongo #老版订餐后台
    from . import models as ding_can_mongo  #新版订餐后台
    print(mydata)
    try:
        if action == '上传用餐人员清单':
            df_main = pandas.read_json(mydata,encoding="utf-8", orient='records')
            手机号_list = []
            主菜单id_list = []
            for row_main in df_main.iterrows():
                手机号 = str(row_main[1]['手机号'])
                主菜单id = row_main[1]['主菜单id']
                if 手机号 in 手机号_list:
                    pass
                else:
                    手机号_list.append(手机号)
                if 主菜单id in 主菜单id_list:
                    pass
                else:
                    主菜单id_list.append(主菜单id)
            for 手机号 in 手机号_list:
                主界内容 = []
                df_手机号 = df_main.loc[(df_main['手机号'] == int(手机号))]
                for row in df_手机号.iterrows():
                    创建时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    描述 = str(row[1]['描述'])
                    主页标题 = str(row[1]['主页标题'])
                    主页描述 = str(row[1]['主页描述'])
                    验证码标题 = str(row[1]['验证码标题'])
                    验证码描述 = str(row[1]['验证码描述'])
                    二级部门 = str(row[1]['二级部门'])
                    三级部门 = str(row[1]['三级部门'])
                    四级部门 = str(row[1]['四级部门'])
                    姓名 = str(row[1]['姓名'])
                    主菜单name = str(row[1]['主菜单name'])
                    主菜单id = str(row[1]['主菜单id'])
                    df_手机号_主菜单name = df_main.loc[(df_main['手机号'] == int(手机号)) & (df_main['主菜单name'] == 主菜单name)]
                    pages = []
                    for index, row in df_手机号_主菜单name.iterrows():
                        子菜单page_name = row['子菜单page_name']
                        子菜单page_desc = row['子菜单page_desc']
                        子菜单url = row['子菜单url']
                        page = {}
                        page['url'] = 子菜单url
                        page['page_name'] = 子菜单page_name
                        page['page_desc'] = 子菜单page_desc
                        if page in pages:
                            pass
                        else:
                            pages.append(page)
                    主菜单id_dict = {
                        'id': 主菜单id,
                        'name': 主菜单name,
                        'open': False,
                        'pages': pages
                    }
                    if 主菜单id_dict in 主界内容:
                        pass
                    else:
                        主界内容.append(主菜单id_dict)
                    主界面表_one = ding_can_mongo.订餐主界面表.objects(手机号=str(手机号)).first()
                    if 主界面表_one == None:
                        ding_can_mongo.订餐主界面表(手机号=str(手机号), 描述=str(描述), 创建时间=str(创建时间), 主页标题=str(主页标题), 主页描述=str(主页描述), 验证码标题=str(验证码标题)
                            , 验证码描述=str(验证码描述),二级部门=二级部门,三级部门=三级部门,四级部门=四级部门,姓名=姓名, 主界内容=主界内容).save()
                    else:
                        主界面表_one.update(手机号=str(手机号), 描述=str(描述), 创建时间=str(创建时间), 主页标题=str(主页标题), 主页描述=str(主页描述), 验证码标题=str(验证码标题)
                            , 验证码描述=str(验证码描述),二级部门=二级部门,三级部门=三级部门,四级部门=四级部门,姓名=姓名, 主界内容=主界内容)
            ding_can_mongo1 = ding_can_mongo.订餐导入时间戳表.objects(flag=flag).first()
            if ding_can_mongo1 == None:
                ding_can_mongo.订餐导入时间戳表(
                    flag=flag,
                    isOk=True
                ).save()
            else:
                ding_can_mongo1.update(isOk=True)
        elif action == '上传充值清单':
            df_main = pandas.read_json(mydata,encoding="utf-8", orient='records')
            for row_main in df_main.iterrows():
                手机号 = str(row_main[1]['手机号'])
                充值金额 = row_main[1]['充值金额']
                备注 = row_main[1]['备注']
                ding_can_mongo.订餐钱包充值表(
                    手机号=手机号,
                    充值金额 = int(充值金额),
                    充值时间=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                    备注 = 备注
                ).save()
            ding_can_mongo1 = ding_can_mongo.订餐导入时间戳表.objects(flag=flag).first()
            if ding_can_mongo1 == None:
                ding_can_mongo.订餐导入时间戳表(
                    flag=flag,
                    isOk=True
                ).save()
            else:
                ding_can_mongo1.update(isOk=True)
        else:
            print('无效请求')

    except:
        r = traceback.format_exc()
        print(r)
        ding_can_mongo1 = ding_can_mongo.订餐导入时间戳表.objects(flag=flag).first()
        if ding_can_mongo1 == None:
            ding_can_mongo.订餐导入时间戳表(
                flag=flag,
                isOk=False,
                eLog={'log':r}
            ).save()
        else:
            ding_can_mongo1.update(isOk=False,eLog={'log':r})

def userInfoUpload(request):
    from . import models as ding_can_mongo #老版订餐后台
    # from . import models as ding_can_mongo  #新版订餐后台
    try:
        access_token = request.POST['access_token']
        if access_token in  ding_can_mongo.管理员手机号清单:
            action = request.POST['action']
            if action == '上传用餐人员清单':
                flag = request.POST['flag']
                mydata = request.POST['excel']
                async_import_excel(mydata,flag,action)
                response = HttpResponse('正在处理')
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"
                return response
            elif action == '上传充值清单':
                flag = request.POST['flag']
                mydata = request.POST['excel']
                async_import_excel(mydata,flag,action)
                response = HttpResponse('正在处理')
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"
                return response
            elif action == '查询结果':
                flag = request.POST['flag']
                from mysite import ding_can_mongo
                ding_can_mongo1 = ding_can_mongo.订餐导入时间戳表.objects(flag=flag).first()
                if ding_can_mongo1 == None:
                    res = '正在处理'
                else:
                    if ding_can_mongo1.isOk :
                        res = '成功'
                    else:
                        res = '失败'+ding_can_mongo1.eLog['log']
                response = HttpResponse(res)
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"
                return response
            else:
                response = HttpResponse('无效请求')
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"
                return response
        else:
            response = HttpResponse('认证失败')
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
            response["Access-Control-Max-Age"] = "1000"
            response["Access-Control-Allow-Headers"] = "*"
            return response
        
    except:
        r = traceback.format_exc()
        print(r)
        response = HttpResponse(r)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

def get_ding_dan(request):
    import json
    from bson.objectid import ObjectId
    # from . import models as ding_can_mongo #老版订餐后台
    from . import models as ding_can_mongo  #新版订餐后台
    try:
        code = request.GET['code']
        日期 = request.GET['date']
        if 日期 == '':
            日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        name = request.GET['name']
        page_name = request.GET['page_name']
        page_desc = request.GET['page_desc']
        js_code = request.GET['code']
        print(code,日期,name,page_name,page_desc)
        wx_login_get_openid_dict = tool.wx_login_get_openid(request)
        用户 = 订餐用户表.objects(openid=wx_login_get_openid_dict['openid']).first()
        if 用户 == None:
            response = HttpResponse(json.dumps({'描述':'无手机号','数据':[]}))
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
            response["Access-Control-Max-Age"] = "1000"
            response["Access-Control-Allow-Headers"] = "*"
            return response
        else:
            手机号 = 用户.手机号
            ding_can_mongo1 = ding_can_mongo.订餐主界面表.objects(手机号=手机号).first()
            if ding_can_mongo1 == None:
                response = HttpResponse(json.dumps({'描述':'无权限','数据':[]}))
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"
                return response
            ding_can_mongo2 = ding_can_mongo.订餐结果表.objects(手机号=手机号,用餐日期=日期,
            子菜单page_name=page_name).first()
            if ding_can_mongo2 == None:
                response = HttpResponse(json.dumps({'描述':'无订餐记录','数据':[]}))
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"
                return response
            else:
                订餐结果列表 = []
                for one in ding_can_mongo.产品全局字典[wx_login_get_openid_dict['app_id']]['产品名称列表']:
                    if one in ding_can_mongo2.产品:
                        number = ding_can_mongo2.产品[one]['预定数量']
                        if not number == 0 or number == None:
                            订餐结果列表.append(
                                {
                                    'oid':str(ding_can_mongo2.id),
                                    'name':one,
                                    'number':number,
                                    'ordertime':ding_can_mongo2.产品[one]['预定时间'],
                                    'price':ding_can_mongo2.产品[one]['价格'],
                                    'mark':ding_can_mongo2.产品[one]['签到']
                                }
                            )
                response = HttpResponse(json.dumps({'描述':'成功','数据':订餐结果列表}))
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"
                return response

    except:
        r = traceback.format_exc()
        print(r)
        response = HttpResponse(json.dumps({'描述':'系统错误','数据':[]}))
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

def get_none_prep_ding_dan(request):
    import json
    from bson.objectid import ObjectId
    # from . import models as ding_can_mongo #老版订餐后台
    from . import models as ding_can_mongo  #新版订餐后台
    try:
        code = request.GET['code']
        日期 = request.GET['date']
        # if 日期 == '':
        日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        name = request.GET['name']
        page_name = request.GET['page_name']
        page_desc = request.GET['page_desc']
        print(code,日期,name,page_name,page_desc)
        wx_login_get_openid_dict = tool.wx_login_get_openid(request)
        用户 = 订餐用户表.objects(openid=wx_login_get_openid_dict['openid']).first()
        if 用户 == None:
            response = HttpResponse(json.dumps({'描述':'无手机号','数据':[]}))
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
            response["Access-Control-Max-Age"] = "1000"
            response["Access-Control-Allow-Headers"] = "*"
            return response
        else:
            手机号 = 用户.手机号
            ding_can_mongo1 = ding_can_mongo.订餐主界面表.objects(手机号=手机号).first()
            if ding_can_mongo1 == None:
                response = HttpResponse(json.dumps({'描述':'无权限','数据':[]}))
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"
                return response
            # ding_can_mongo2 = ding_can_mongo.订餐结果表.objects(手机号=手机号,用餐日期=日期,
            # 子菜单page_name=page_name).first()
            # if ding_can_mongo2 == None:
            #     response = HttpResponse(json.dumps({'描述':'无订餐记录','数据':[]}))
            #     response["Access-Control-Allow-Origin"] = "*"
            #     response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
            #     response["Access-Control-Max-Age"] = "1000"
            #     response["Access-Control-Allow-Headers"] = "*"
            #     return response
            else:
                订餐结果列表 = []
                # 非预定产品名称列表 = ding_can_mongo.产品全局字典[wx_login_get_openid_dict['app_id']]['非预定产品名称列表']
                非预定产品列表 = ding_can_mongo.产品全局字典[wx_login_get_openid_dict['app_id']]['非预定产品列表']
                for one in 非预定产品列表:
                    # if one in ding_can_mongo2.产品:
                    订餐结果列表.append(
                            {
                            'oid':'',
                            'name':one['名称'],
                            'number':1,
                            'ordertime':'',
                            'price':one['价格'],
                            'mark':'没吃'
                        }
                    )
                response = HttpResponse(json.dumps({'描述':'成功','数据':订餐结果列表}))
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"
                return response
    except:
        r = traceback.format_exc()
        print(r)
        response = HttpResponse(json.dumps({'描述':'系统错误','数据':[]}))
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
        
def buy_product(request):
    from . import models
    try:
        wx_login_get_openid_dict = tool.wx_login_get_openid(request)
        当前时间戳 = time.time()
        当前时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        当前日期加一天 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400))
        当前日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        当前月份 = time.strftime('%Y-%m', time.localtime(time.time()))
        订餐用户表_one = 订餐用户表.objects(openid=wx_login_get_openid_dict['openid']).first()
        if 订餐用户表_one == None:
            自定义登录状态 = "{\"描述\":\"用户不存在\",\"会话\":\"\"}"
            return HttpResponse(自定义登录状态)
        else:
            手机号 = 订餐用户表_one.手机号
            订餐主界面表_first = 订餐主界面表.objects(手机号=手机号).first()
            主菜单name = request.GET['name']
            子菜单page_name = request.GET['page_name']
            子菜单page_desc = request.GET['page_desc']
            用餐日期 = request.GET['date']
            # if 用餐日期 == '':
            用餐日期 = 当前日期
            product_name = request.GET['product_name']
            product_nbr = int(request.GET['product_nbr'])
            product_price = int(request.GET['product_price'])
            totalAmount_int = int(product_nbr)*int(product_price)
            qset11 = models.订餐钱包表.objects(openid=wx_login_get_openid_dict['openid']).first()
            if qset11 == None:
                models.订餐钱包表(openid=wx_login_get_openid_dict['openid'],已充值=0).save()
                qset11 = models.订餐钱包表.objects(openid=wx_login_get_openid_dict['openid']).first()
                已充值 = qset11.已充值
            else:
                已充值 = qset11.已充值
            if 已充值 - totalAmount_int - qset11.已消费 - qset11.预消费  >= 0:
                qset22 = models.订餐结果表.objects(
                    手机号=手机号,
                    子菜单page_name=子菜单page_name,
                    用餐日期=用餐日期
                ).first()
                if qset22 == None:
                    models.订餐结果表(
                        手机号=手机号,
                        子菜单page_name=子菜单page_name,
                        用餐日期=用餐日期,
                        产品 =  {
                            product_name:{
                                '预定时间':当前时间,
                                '预定数量':product_nbr,
                                '签到':'没吃',
                                '价格':product_price,
                                '签到时间':''
                            }
                        }
                    ).save()
                    异步计算消费金额(wx_login_get_openid_dict)
                else:
                    产品 = qset22.产品
                    产品[product_name] = {
                                '预定时间':当前时间,
                                '预定数量':product_nbr,
                                '签到':'没吃',
                                '价格':product_price,
                                '签到时间':''
                            }
                    qset22.update( 产品 = 产品  )
                    异步计算消费金额(wx_login_get_openid_dict)
                订餐结果表2505 = models.订餐结果表.objects(
                    手机号=手机号,
                    子菜单page_name=子菜单page_name,
                    用餐日期=用餐日期
                ).first()
                oid = str(订餐结果表2505.id)
                描述 = '上传成功'
                订餐结果描述 = '上传成功'
                自定义登录状态 = {'描述': 描述,'oid':oid, '会话': '123456', '订餐结果描述': 订餐结果描述}
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                异步计算订餐结果(子菜单page_name, 订餐主界面表_first.二级部门)
                异步统计产品(子菜单page_name, 订餐主界面表_first.二级部门,wx_login_get_openid_dict)
                return HttpResponse(自定义登录状态)
            else:
                qset22 = models.订餐结果表.objects(
                    手机号=手机号,
                    子菜单page_name=子菜单page_name,
                    用餐日期=用餐日期
                ).first()
                if qset22 == None:
                    qset2526 = models.订餐结果临时表.objects(
                        手机号=手机号,
                        子菜单page_name=子菜单page_name,
                        用餐日期=用餐日期
                    ).first()
                    if qset2526 == None:
                        models.订餐结果临时表(
                            手机号=手机号,
                            子菜单page_name=子菜单page_name,
                            用餐日期=用餐日期,
                            产品 =  {
                                product_name:{
                                    '预定时间':当前时间,
                                    '预定数量':product_nbr,
                                    '签到':'没吃',
                                    '价格':product_price,
                                    '签到时间':''
                                }
                            }
                        ).save()
                    else:
                        qset2526.update(
                            产品 =  {
                                product_name:{
                                    '预定时间':当前时间,
                                    '预定数量':product_nbr,
                                    '签到':'没吃',
                                    '价格':product_price,
                                    '签到时间':''
                                }
                            }
                        )
                else:
                    产品 = qset22.产品
                    产品[product_name] = {
                            '预定时间':当前时间,
                            '预定数量':product_nbr,
                            '签到':'没吃',
                            '价格':product_price,
                            '签到时间':''
                        }
                    qset2567 = models.订餐结果临时表.objects(
                        手机号=手机号,
                        子菜单page_name=子菜单page_name,
                        用餐日期=用餐日期
                    ).first()
                    if qset2567 == None:
                        models.订餐结果临时表(
                            手机号=手机号,
                            子菜单page_name=子菜单page_name,
                            用餐日期=用餐日期,
                            产品 = 产品
                        ).save()
                    else:
                        qset2567.update(产品 = 产品)
                qset2581 = models.订餐结果临时表.objects(
                        手机号=手机号,
                        子菜单page_name=子菜单page_name,
                        用餐日期=用餐日期
                    ).first()
                goods = []
                ding_can_chinaums_pay_order_res = ding_can_chinaums_pay_order(str(totalAmount_int),goods,wx_login_get_openid_dict)
                print(ding_can_chinaums_pay_order_res)
                描述 = '银联下单'
                订餐结果描述 = '银联下单'
                其他参数 = {
                    'totalAmount':totalAmount_int,
                    'oid':str(qset2581.id),
                    '子菜单page_name':子菜单page_name,
                    '二级部门':订餐主界面表_first.二级部门
                }
                自定义登录状态 = {
                    '描述': 描述, '会话': '',
                    '订餐结果描述': 订餐结果描述,
                    'miniPayRequest':ding_can_chinaums_pay_order_res['miniPayRequest'],
                    'state': 其他参数 
                }
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')

def ti_xing_fa_huo(request):
    try:
        data = request.GET['data']
        print(data)
        data = json.loads(data)
        if 'code' in data and 'oid' in data and 'name' in data and 'key' in data:
            app_id = data['app_id']
            code = data['code']
            oid = data['oid']
            name = data['name']
            key = data['key']
            qset1 = db.查询第一个订单结果(oid)
            if qset1 == None:
                return tool.my_httpResponse(0,{},'订单不存在')
            产品 = qset1.产品
            if not name in 产品:
                return tool.my_httpResponse(0,{},'产品不存在')
            if not name in 产品:
                return tool.my_httpResponse(0,{},name+'不存在')
            if not '签到' in 产品[name]:
                return tool.my_httpResponse(0,{},'签到不存在')
            签到 = 产品[name]['签到']
            if 签到 == '吃过':
                return tool.my_httpResponse(0,{},'已吃过,不能提醒')
            用餐日期 = qset1.用餐日期
            预定数量 = 产品[name]['预定数量']
            手机号 = qset1.手机号
            qset2 = models.订餐主界面表.objects(手机号=手机号).first()
            if qset2 == None:
                return tool.my_httpResponse(0,{},'手机号未注册')
            姓名 = qset2.姓名
            微信认证 = tool.微信认证(code,app_id)
            openid = 微信认证['openid']
            app_id = 微信认证['app_id']
            create_date = tool.get_str_date(0)
            create_time = tool.get_str_time(0)
            db.创建订餐提醒发货表(
                oid,name,
                {
                'oid':oid,
                '手机号':手机号,
                '预定数量':预定数量,
                '用餐日期':用餐日期,
                '姓名':姓名,
                'name':name,
                'create_date': create_date,
                'create_time': create_time
            })
            return tool.my_httpResponse(1,{},'成功')
        return tool.my_httpResponse(0,{},'参数出错误')
    except:
        print(traceback.format_exc())
        return  tool.my_httpResponse(0,{},'异常')

def start_voice(request):
    try:
        data = request.GET['data']
        print(data)
        data = json.loads(data)
        if not 'code' in data and 'app_id' in data:
            return  tool.my_httpResponse(0,{},'参数错误')
        code = data['code']
        app_id = data['app_id']
        微信认证 = tool.微信认证(code,app_id)
        now_date = tool.get_str_date(0)
        qset1 = models.订餐提醒发货表.objects(__raw__={
            'd.用餐日期':now_date,
        }).order_by('create_time').first()
        if qset1 == None:
            return  tool.my_httpResponse(2,{},'无提醒')
        dict1 = qset1.d
        # dict1['create_time'] = tool.get_str_time(-10)
        # qset1.update(d=dict1)
        qset1.delete()
        return  tool.my_httpResponse(1,dict1,'成功')
    except:
        print(traceback.format_exc())
        return  tool.my_httpResponse(0,{},'异常')

def send_goods(request):
    try:
        data = request.GET['data']
        print(data)
        data = json.loads(data)
        if not 'code' in data and 'app_id' in data and 'order' in data:
            return  tool.my_httpResponse(0,{},'参数错误')
        code = data['code']
        app_id = data['app_id']
        微信认证 = tool.微信认证(code,app_id)
        openid = 微信认证['openid']
        app_id = 微信认证['app_id']
        order = data['order']
        if not 'oid' in order:
            return tool.my_httpResponse(0,{},'订单号错误')
        oid = order['oid']
        qset1 = db.查询第一个订单结果(oid)
        if qset1 == None:
            return tool.my_httpResponse(0,{},'订单不存在')
        产品 = qset1.产品
        name = order['name']
        产品[name]['签到'] = '吃过'
        qset1.update(产品=产品)
        return  tool.my_httpResponse(1,{},'成功')
    except:
        print(traceback.format_exc())
        return  tool.my_httpResponse(0,{},'异常')