import csv
import hashlib
import json
import random
import traceback
import uuid
from email.mime.multipart import MIMEMultipart

import bson
import pandas
import requests
import time
from django.http import HttpResponse, FileResponse
import pymongo
from pandocfilters import Math
from pymongo import MongoClient
import myConfig
from mysite.ftp_test import ftpconnect, uploadfile

client = MongoClient('mongodb://' + myConfig.username + ':' + myConfig.password + '@' + str(myConfig.host) + ':' + str(myConfig.port) + '/'+myConfig.db)
db = client['mydb']
from myConfig import chou_jiang_appid, chou_jiang_secret, chou_jiang_grant_type, sign_name, template_code
from mysite.chou_jiang_mongo import 抽奖用户表, 抽奖登录状态表, 抽奖验证码表, 抽奖主界面表, 没中奖, 抽奖开关, 中奖人数字典, 中奖金额字典, 抽奖状态表, 一等奖, \
    二等奖, 抽奖参与者, 全体奖, 三等奖, 四等奖, 未开始, 抽奖开始, 抽奖结束, 抽奖全体奖状态表, 抽奖按钮状态, 采集模版表, 采集分工表, 采集录入分工表, 建筑物主键分隔符, 可录入, 已录入, 新录入, 分页
from mysite.demo_sms_send import send_sms
from mysite.settings import 两高楼宇采集新界面开关, 两高楼宇采集审核开关, 两高楼宇采集template_id
from myConfig import 两高楼宇采集host, 两高楼宇采集port, 两高楼宇采集username, 两高楼宇采集password

#异步函数
def deprecated_async(f):
    def wrapper(*args, **kwargs):
        from threading import Thread
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

def 抽奖登录检查(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': chou_jiang_appid, 'secret': chou_jiang_secret, 'js_code': js_code,
                   'grant_type': chou_jiang_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        查询结果 = 抽奖用户表.objects(openid=r_json['openid']).first()
        if 查询结果 == None:
            自定义登录状态 = "{\"描述\":\"用户不存在\",\"会话\":\"\"}"
            # 自定义登录状态 = {"描述":"用户不存在","会话":""}
            return HttpResponse(自定义登录状态)
        elif 两高楼宇采集新界面开关:
            自定义登录状态 = "{\"描述\":\"新界面\",\"会话\":\"123456\"}"
            return HttpResponse(自定义登录状态)
        else:
            r = 抽奖登录状态表(session_key=r_json['session_key'], openid=r_json['openid']).save()
            自定义登录状态 = "{\"描述\":\"验证通过\",\"会话\":\"" + str(r.id) + "\"}"
            return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')

def 抽奖发送验证码(request):
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
                r = 抽奖验证码表(验证码=验证码, 手机号=手机号).save()
            return HttpResponse(r2['Code'])
    except:
        print(traceback.format_exc())
        return HttpResponse(traceback.format_exc())

def 抽奖校验验证码(request):
    手机号 = str(request.GET['phone'])
    验证码 = str(request.GET['sms_code'])
    js_code = request.GET['code']
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    payload = {'appid': chou_jiang_appid, 'secret': chou_jiang_secret, 'js_code': js_code,
               'grant_type': chou_jiang_grant_type}
    r = requests.get(url=url, params=payload)
    r_json = json.loads(r.text)
    openid = r_json['openid']
    抽奖验证码表_objects = 抽奖验证码表.objects(手机号=手机号)
    for 抽奖验证码表_obj in 抽奖验证码表_objects:
        if 抽奖验证码表_obj.验证码 == 验证码:
            抽奖用户表_first = 抽奖用户表.objects(手机号=手机号).first()
            if 抽奖用户表_first == None:
                抽奖用户表(手机号=手机号, openid=openid).save()
            else:
                抽奖用户表_first.update(openid=openid)
            return HttpResponse('绑定成功')
    return HttpResponse('绑定失败')

def 抽奖下载主界面数据(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': chou_jiang_appid, 'secret': chou_jiang_secret, 'js_code': js_code,
                   'grant_type': chou_jiang_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 抽奖用户表.objects(openid=r_json['openid']).first()
        主界面 = 抽奖主界面表.objects(手机号=用户.手机号).first()
        if 主界面 == None:
            if 两高楼宇采集审核开关:
                创建时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                描述 = '下载成功'
                主页标题 = '楼宇采集'
                主页描述 = '楼宇采集'
                验证码标题 = '网优班'
                验证码描述 = '测试用户'
                二级部门 = '测试用户'
                三级部门 = '池州市'
                四级部门 = '网优班'
                姓名 = '测试用户'
                主界内容 = [
                    {
                        'id': 'ce_shi',
                        'name': '测试用户',
                        'open': False,
                        'pages': [
                            {
                                'url': 'lu_ru',
                                'page_name': '东至县',
                                'page_desc': '楼宇采集'
                            },
                        ]
                    }
                ]
                # 主界内容 = [
                #     {
                #         'id': 'ce_shi',
                #         'name': '测试用户',
                #         'open': False,
                #         'pages': [
                #             {
                #                 'url': 'lu_ru',
                #                 'page_name': '谢时乐',
                #                 'page_desc': '楼宇采集'
                #             },
                #             {
                #                 'url': 'lu_ru',
                #                 'page_name': '王皓',
                #                 'page_desc': '楼宇采集'
                #             },
                #             {
                #                 'url': 'lu_ru',
                #                 'page_name': '王名鑫',
                #                 'page_desc': '楼宇采集'
                #             },
                #             {
                #                 'url': 'lu_ru',
                #                 'page_name': '路斌',
                #                 'page_desc': '楼宇采集'
                #             },
                #             {
                #                 'url': 'lu_ru',
                #                 'page_name': '王宇',
                #                 'page_desc': '楼宇采集'
                #             },
                #             {
                #                 'url': 'lu_ru',
                #                 'page_name': '柯英杰',
                #                 'page_desc': '楼宇采集'
                #             },
                #             {
                #                 'url': 'lu_ru',
                #                 'page_name': '吴师诚',
                #                 'page_desc': '楼宇采集'
                #             },
                #             {
                #                 'url': 'lu_ru',
                #                 'page_name': '吴敏民',
                #                 'page_desc': '楼宇采集'
                #             },
                #             {
                #                 'url': 'lu_ru',
                #                 'page_name': '皋亮亮',
                #                 'page_desc': '楼宇采集'
                #             },
                #         ]
                #     }
                # ]
                订餐主界面表_save = 抽奖主界面表(手机号=str(用户.手机号), 描述=str(描述), 创建时间=str(创建时间),
                       主页标题=str(主页标题),主页描述=str(主页描述), 验证码标题=str(验证码标题),
                       验证码描述=str(验证码描述), 二级部门=二级部门, 三级部门=三级部门, 四级部门=四级部门, 姓名=姓名,
                       主界内容=主界内容).save()
                自定义登录状态 = 订餐主界面表_save.to_json().encode('utf-8').decode('unicode_escape')
                return HttpResponse(自定义登录状态)
            自定义登录状态 = "{\"描述\":\"没有数据\",\"会话\":\"" + r_json['session_key'] + "\"}"
            return HttpResponse(自定义登录状态)
        else:
            抽奖参与者_first = 抽奖参与者.objects(手机号=主界面.手机号).first()
            if 抽奖参与者_first == None:
                抽奖参与者(
                    手机号=主界面.手机号,
                    姓名=主界面.姓名
                ).save()
            else:
                抽奖参与者_first.update(
                    手机号=主界面.手机号,
                    姓名=主界面.姓名
                )
            自定义登录状态 = 主界面.to_json().encode('utf-8').decode('unicode_escape')
            return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')

@deprecated_async
def 随机抽奖(类型):
    中奖人数 = 中奖人数字典[类型]
    中奖金额 = 中奖金额字典[类型]
    开关_first = 抽奖开关.objects.first()
    if 开关_first == None:
        抽奖开关(开关=True).save()
        随机抽奖(类型)
    else:
        开关 = 开关_first.开关
        while(开关):
            开关_first = 抽奖开关.objects.first()
            if 开关_first == None:
                开关 = False
            else:
                开关 = 开关_first.开关
            if 类型 == 全体奖:
                中奖金额上限 = int(中奖金额 * 1.5)
                中奖金额下限 = int(中奖金额 * 0.5)
                全体奖字典 = {k.手机号: random.randint(中奖金额下限, 中奖金额上限) for k in 抽奖参与者.objects}
                全体奖状态表_first = 抽奖全体奖状态表.objects.first()
                if 全体奖状态表_first == None:
                    抽奖全体奖状态表(quan_ti_jiang=全体奖字典).save()
                else:
                    全体奖状态表_first.update(quan_ti_jiang=全体奖字典)
            else:
                pipeline = [{'$sample': {'size': 中奖人数 }}]
                flex_list = []
                中奖金额上限 = int(中奖金额 * 1.5)
                中奖金额下限 = int(中奖金额 * 0.5)
                for doc in 抽奖参与者.objects(中奖类型=没中奖).aggregate(*pipeline):
                    奖金 = random.randint(中奖金额下限,中奖金额上限)
                    中奖详情 = {
                        'name': doc['姓名']+doc['手机号']+类型+str(奖金)+'元',
                        'flag':False,
                        '奖金':奖金,
                        '手机号':doc['手机号'],
                        '姓名':doc['姓名']
                    }
                    flex_list.append(中奖详情)
                抽奖状态表_first = 抽奖状态表.objects(lei_xing=类型).first()
                if 抽奖状态表_first == None:
                    抽奖状态表(lei_xing=类型,flex_list=flex_list).save()
                else:
                    抽奖状态表_first.update(flex_list=flex_list)

def 抽奖下载名单(request):
    form_target_id = request.GET['form_target_id']
    抽奖按钮状态_first = 抽奖按钮状态.objects.first()
    if 抽奖按钮状态_first == None:
        jie_guo = 未开始
        lei_xing = ''
        ti_shi = 未开始
        flex_list = [
        ]
        自定义登录状态 = {
            'jie_guo': jie_guo,
            'lei_xing': lei_xing,
            'ti_shi':ti_shi,
            'flex_list': flex_list
        }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)
    else:
        lei_xing = form_target_id
        if lei_xing == 全体奖:
            js_code = request.GET['code']
            url = 'https://api.weixin.qq.com/sns/jscode2session'
            payload = {'appid': chou_jiang_appid, 'secret': chou_jiang_secret, 'js_code': js_code,
                       'grant_type': chou_jiang_grant_type}
            r = requests.get(url=url, params=payload)
            r_json = json.loads(r.text)
            用户 = 抽奖用户表.objects(openid=r_json['openid']).first()
            抽奖参与者_first = 抽奖参与者.objects(手机号=用户.手机号).first()
            全体奖状态表_first = 抽奖全体奖状态表.objects.first()
            if 抽奖参与者_first == None or 全体奖状态表_first == None :
                flex_list = []
            else:
                if 用户.手机号 in 全体奖状态表_first.quan_ti_jiang:
                    奖金 = 全体奖状态表_first.quan_ti_jiang[用户.手机号]
                else:
                    奖金 = 0
                flex_list = [{
                    'name': 抽奖参与者_first.姓名 + 抽奖参与者_first.手机号 + ' 奖金：' + str(奖金) + '元',
                    'flag': False,
                    '奖金': 奖金,
                    '手机号': 抽奖参与者_first.手机号,
                    '姓名': 抽奖参与者_first.姓名
                }]
            自定义登录状态 = {
                'jie_guo': 抽奖按钮状态_first.jie_guo,
                'lei_xing': lei_xing+'结果：',
                'ti_shi': 抽奖按钮状态_first.ti_shi,
                'flex_list': flex_list
            }
        else:
            抽奖状态表_first = 抽奖状态表.objects(lei_xing=lei_xing).first()
            if 抽奖状态表_first == None:
                flex_list = []
            else:
                flex_list = 抽奖状态表_first.flex_list
            自定义登录状态 = {
                'jie_guo': 抽奖按钮状态_first.jie_guo,
                'lei_xing': lei_xing+'结果：',
                'ti_shi': 抽奖按钮状态_first.ti_shi,
                'flex_list': flex_list
            }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)

def 抽奖按钮(request):
    btn_id = request.GET['btn_id']
    抽奖按钮状态_first = 抽奖按钮状态.objects.first()
    if 抽奖按钮状态_first == None:
        jie_guo = 未开始
        ti_shi = 未开始
        btn_list = [
            {'name': 全体奖, 'flag': False, 'flag_2': False},
            {'name': 一等奖, 'flag': False, 'flag_2': False},
            {'name': 二等奖, 'flag': False, 'flag_2': False},
            {'name': 三等奖, 'flag': False, 'flag_2': False},
            {'name': 四等奖, 'flag': False, 'flag_2': False}
        ]
        自定义登录状态 = {
            'jie_guo': jie_guo,
            'ti_shi': ti_shi,
            'btn_list': btn_list,
        }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)
    else:
        jie_guo = 抽奖开始
        lei_xing = btn_id
        ti_shi = 抽奖开始
        btn_list = []
        for btn_list_one in 抽奖按钮状态_first.btn_list:
            if btn_list_one['name'] == btn_id:
                if btn_list_one['flag_2']:
                    #结束抽奖
                    开关_first = 抽奖开关.objects.first()
                    if 开关_first == None:
                        抽奖开关(开关=False).save()
                    else:
                        开关_first.update(开关=False)
                    jie_guo = 抽奖结束
                    ti_shi = 抽奖结束
                    btn_list = [
                        {'name': 全体奖, 'flag': False, 'flag_2': False},
                        {'name': 一等奖, 'flag': False, 'flag_2': False},
                        {'name': 二等奖, 'flag': False, 'flag_2': False},
                        {'name': 三等奖, 'flag': False, 'flag_2': False},
                        {'name': 四等奖, 'flag': False, 'flag_2': False}
                    ]
                    开关_first2 = 抽奖开关.objects.first()
                    if 开关_first2 == None:
                        抽奖开关(开关=False).save()
                    else:
                        开关2 = 开关_first2.开关
                        if 开关2:
                            pass
                        else:
                            if btn_id == 全体奖:
                                pass
                            else:
                                抽奖状态表_first = 抽奖状态表.objects(lei_xing=btn_id).first()
                                for flex_one in 抽奖状态表_first.flex_list:
                                    抽奖参与者_first = 抽奖参与者.objects(手机号=flex_one['手机号']).first()
                                    if 抽奖参与者_first == None:
                                        pass
                                    else:
                                        抽奖参与者_first.update(中奖类型=btn_id)
                    break
                else:
                    # 开始抽奖
                    开关_first = 抽奖开关.objects.first()
                    if 开关_first == None:
                        抽奖开关(开关=True).save()
                    else:
                        开关_first.update(开关=True)
                    随机抽奖(btn_id)
                    btn_list_one['flag_2'] = True
            else:
                btn_list_one['flag'] = True
            btn_list.append(btn_list_one)
        抽奖按钮状态_first.update(
            jie_guo=jie_guo,
            lei_xing=lei_xing,
            ti_shi=ti_shi,
            btn_list=btn_list
        )
        自定义登录状态 = {
            'jie_guo': jie_guo,
            'lei_xing':lei_xing,
            'ti_shi': ti_shi,
            'btn_list': btn_list,
        }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)

def 抽奖管理初始化(request):
    抽奖按钮状态_first = 抽奖按钮状态.objects.first()
    if 抽奖按钮状态_first == None:
        jie_guo = 未开始
        lei_xing = ''
        ti_shi = 未开始
        btn_list = [
            {'name': 全体奖, 'flag': False, 'flag_2': False},
            {'name': 一等奖, 'flag': False, 'flag_2': False},
            {'name': 二等奖, 'flag': False, 'flag_2': False},
            {'name': 三等奖, 'flag': False, 'flag_2': False},
            {'name': 四等奖, 'flag': False, 'flag_2': False}
        ]
        form_list = [
            {'name': 全体奖, 'flag': False, 'flag_2': False},
            {'name': 一等奖, 'flag': False, 'flag_2': False},
            {'name': 二等奖, 'flag': False, 'flag_2': False},
            {'name': 三等奖, 'flag': False, 'flag_2': False},
            {'name': 四等奖, 'flag': False, 'flag_2': False}
        ]

        抽奖按钮状态(jie_guo=jie_guo,lei_xing = lei_xing,ti_shi=ti_shi, btn_list=btn_list).save()
        自定义登录状态 = {
            'jie_guo': jie_guo,
            'lei_xing': '',
            'ti_shi': ti_shi,
            'btn_list': btn_list,
            'form_list':form_list
        }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)
    else:
        form_list = [
            {'name': 全体奖, 'flag': False, 'flag_2': False},
            {'name': 一等奖, 'flag': False, 'flag_2': False},
            {'name': 二等奖, 'flag': False, 'flag_2': False},
            {'name': 三等奖, 'flag': False, 'flag_2': False},
            {'name': 四等奖, 'flag': False, 'flag_2': False}
        ]
        自定义登录状态 = {
            'jie_guo': 抽奖按钮状态_first.jie_guo,
            'lei_xing': 抽奖按钮状态_first.lei_xing,
            'ti_shi': 抽奖按钮状态_first.ti_shi,
            'btn_list': 抽奖按钮状态_first.btn_list,
            'form_list':form_list
        }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)

def 抽奖推送微信验证(request):
    signature = request.GET["signature"]
    timestamp = request.GET["timestamp"]
    nonce = request.GET["nonce"]
    echostr = request.GET["echostr"]
    token = myConfig.令牌
    list = [token, timestamp, nonce]
    list.sort()
    list2 = ''.join(list)
    sha1 = hashlib.sha1()
    sha1.update(list2.encode('utf-8'))
    hashcode = sha1.hexdigest()
    if hashcode == signature:
        return HttpResponse(echostr)
    else:
        return HttpResponse(echostr)

def chou_jiang_getAccessToken():
    url = 'https://api.weixin.qq.com/cgi-bin/token'
    payload = {'appid': chou_jiang_appid,'secret': chou_jiang_secret,'grant_type':'client_credential'}
    r = requests.get(url=url, params=payload)
    r_json = json.loads(r.text)
    # 用户 = 抽奖用户表.objects(openid=r_json['openid']).first()
    if 'access_token' in r_json:
        return r_json['access_token']
    else:
        return ''

@deprecated_async
def chou_jiang_sendTemplateMessage(access_token,openid,form_id,data):
    url = 'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token='+access_token
    payload = {
        'touser': openid,
        'template_id': 两高楼宇采集template_id,
        'form_id': form_id,
        'data': data
    }
    r = requests.post(url=url, json =payload)
    r_json = json.loads(r.text)

def test(form_target_id):
    r = 抽奖用户表.objects(手机号='13355661100').first()
    access_token = chou_jiang_getAccessToken()
    openid = r.openid
    form_id = r.formId
    data = {
        'keyword1': {
            'value': 'aaa'
        },
        'keyword2': {
            'value': 'aa 10'
        },
        'keyword3': {
            'value': '13355661100'
        },
        'keyword4': {
            'value': 'bbb'
        }
    }
    chou_jiang_sendTemplateMessage(access_token, openid, form_id, data)

def 抽奖获得form_id(request):
    try:
        form_target_id = request.GET['form_target_id']
        js_code = request.GET['code']
        formId = request.GET['formId']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': chou_jiang_appid, 'secret': chou_jiang_secret, 'js_code': js_code,
                   'grant_type': chou_jiang_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        抽奖用户表_first = 抽奖用户表.objects(openid=r_json['openid']).first()
        if 抽奖用户表_first == None:
            自定义登录状态 = "{\"描述\":\"用户不存在\",\"会话\":\"\"}"
            return HttpResponse(自定义登录状态)
        else:
            抽奖按钮状态_first = 抽奖按钮状态.objects.first()
            if 抽奖按钮状态_first == None:
                pass
            else:
                if 抽奖按钮状态_first.lei_xing == form_target_id:
                    if 抽奖按钮状态_first.ti_shi == 抽奖结束:
                        form_target_id_formId_dict = 抽奖用户表_first.formId_dict
                        form_target_id_formId_dict[form_target_id] = formId
                        抽奖用户表_first.update(formId_dict=form_target_id_formId_dict)
                        if form_target_id == 全体奖:
                            抽奖状态表_first = 抽奖全体奖状态表.objects.first()
                            if 抽奖状态表_first == None:
                                pass
                            else:
                                抽奖参与者_first = 抽奖参与者.objects(手机号=抽奖用户表_first.手机号).first()
                                if 抽奖参与者_first == None:
                                    姓名 = ''
                                else:
                                    姓名 = 抽奖参与者_first.姓名
                                金额 = str(抽奖状态表_first.quan_ti_jiang[抽奖用户表_first.手机号])
                                access_token = chou_jiang_getAccessToken()
                                openid = 抽奖用户表_first.openid
                                form_id = 抽奖用户表_first.formId_dict[form_target_id]
                                data = {
                                    'keyword1': {
                                        'value': '快乐抽奖888'
                                    },
                                    'keyword2': {
                                        'value': 姓名+抽奖用户表_first.手机号+全体奖+金额+'元'
                                    },
                                    'keyword3': {
                                        'value': 抽奖用户表_first.手机号
                                    },
                                    'keyword4': {
                                        'value': '请联系我们领取'
                                    }
                                }
                                chou_jiang_sendTemplateMessage(access_token, openid, form_id, data)
                        else:
                            抽奖状态表_first = 抽奖状态表.objects(lei_xing=form_target_id).first()
                            if 抽奖状态表_first == None:
                                pass
                            else:
                                for flex_one in 抽奖状态表_first.flex_list:
                                    if flex_one['手机号'] == 抽奖用户表_first.手机号:
                                        name = str(flex_one['name'])
                                        access_token = chou_jiang_getAccessToken()
                                        openid = 抽奖用户表_first.openid
                                        form_id = 抽奖用户表_first.formId_dict[form_target_id]
                                        data = {
                                            'keyword1': {
                                                'value': '快乐抽奖888'
                                            },
                                            'keyword2': {
                                                'value': name
                                            },
                                            'keyword3': {
                                                'value': 抽奖用户表_first.手机号
                                            },
                                            'keyword4': {
                                                'value': '请联系我们领取'
                                            }
                                        }
                                        chou_jiang_sendTemplateMessage(access_token, openid, form_id, data)
                else:
                    form_target_id_formId_dict = 抽奖用户表_first.formId_dict
                    form_target_id_formId_dict[form_target_id] = formId
                    抽奖用户表_first.update(formId_dict=form_target_id_formId_dict)
                    if form_target_id == 全体奖:
                        抽奖状态表_first = 抽奖全体奖状态表.objects.first()
                        if 抽奖状态表_first == None:
                            pass
                        else:
                            抽奖参与者_first = 抽奖参与者.objects(手机号=抽奖用户表_first.手机号).first()
                            if 抽奖参与者_first == None:
                                姓名 = ''
                            else:
                                姓名 = 抽奖参与者_first.姓名
                            金额 = str(抽奖状态表_first.quan_ti_jiang[抽奖用户表_first.手机号])
                            access_token = chou_jiang_getAccessToken()
                            openid = 抽奖用户表_first.openid
                            form_id = 抽奖用户表_first.formId_dict[form_target_id]
                            data = {
                                'keyword1': {
                                    'value': '快乐抽奖888'
                                },
                                'keyword2': {
                                    'value': 姓名 + 抽奖用户表_first.手机号 + 全体奖 + 金额 + '元'
                                },
                                'keyword3': {
                                    'value': 抽奖用户表_first.手机号
                                },
                                'keyword4': {
                                    'value': '请联系我们领取'
                                }
                            }
                            chou_jiang_sendTemplateMessage(access_token, openid, form_id, data)
                    else:
                        抽奖状态表_first = 抽奖状态表.objects(lei_xing=form_target_id).first()
                        if 抽奖状态表_first == None:
                            pass
                        else:
                            for flex_one in 抽奖状态表_first.flex_list:
                                if flex_one['手机号'] == 抽奖用户表_first.手机号:
                                    name = str(flex_one['name'])
                                    access_token = chou_jiang_getAccessToken()
                                    openid = 抽奖用户表_first.openid
                                    form_id = 抽奖用户表_first.formId_dict[form_target_id]
                                    data = {
                                        'keyword1': {
                                            'value': '快乐抽奖888'
                                        },
                                        'keyword2': {
                                            'value': name
                                        },
                                        'keyword3': {
                                            'value': 抽奖用户表_first.手机号
                                        },
                                        'keyword4': {
                                            'value': '请联系我们领取'
                                        }
                                    }
                                    chou_jiang_sendTemplateMessage(access_token, openid, form_id, data)
            自定义登录状态 = "{\"描述\":\"新界面\",\"会话\":\"123456\"}"
            return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')


def 采集初始化(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': chou_jiang_appid, 'secret': chou_jiang_secret, 'js_code': js_code,
                   'grant_type': chou_jiang_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 抽奖用户表.objects(openid=r_json['openid']).first()
        抽奖主界面表first = 抽奖主界面表.objects(手机号=用户.手机号).first()
        if 抽奖主界面表first == None:
            四级部门 = ''
        else:
            四级部门 = 抽奖主界面表first.四级部门
        bindMenPaiHao_id = request.GET['bindMenPaiHao_id']
        bindMenPaiHao_id_list = bindMenPaiHao_id.split(建筑物主键分隔符)
        print(bindMenPaiHao_id_list)
        责任人 = bindMenPaiHao_id_list[0]
        场所名称 = bindMenPaiHao_id_list[1]
        建筑物编号 = bindMenPaiHao_id_list[2]
        建筑物名称 = bindMenPaiHao_id_list[3]
        采集分工表objs = 采集分工表.objects(手机号=四级部门)
        countries = []
        for 采集分工表obj in 采集分工表objs:
            if 采集分工表obj.分工['场所名称'] in countries:
                pass
            else:
                countries.append(采集分工表obj.分工['场所名称'])
        采集模版表first = 采集模版表.objects(建筑物编号=建筑物编号).first()
        if 采集模版表first == None:
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
            手机号 = 采集模版表first.手机号
            当前时间 = 采集模版表first.当前时间
            建筑物编号 = 采集模版表first.建筑物编号
            采集内容 = 采集模版表first.采集内容
            场所楼宇总栋数 = 采集内容['chang_suo_lou_yu_zong_dong_shu']
            现场经度 = 采集内容['xian_chang_jing_du']
            现场纬度 = 采集内容['xian_chang_wei_du']
            楼宇层数 = 采集内容['lou_yu_ceng_shu']
            地下室层数 = 采集内容['di_xia_shi_ceng_shu']
            电梯数量 = 采集内容['dian_ti_shu_liang']
            电信下载速率 = 采集内容['dx_xia_zai']
            电信上传速率 = 采集内容['dx_shang_chuang']
            移动下载速率 = 采集内容['yd_xia_zai']
            移动上传速率 = 采集内容['yd_shang_chuang']
            if 'shi_fou_you_di_xia_ting_cha_chang' in 采集内容.keys():
                shi_fou_you_di_xia_ting_cha_chang = 采集内容['shi_fou_you_di_xia_ting_cha_chang']
            else:
                shi_fou_you_di_xia_ting_cha_chang = False
            if 'shi_fou_you_yi_wang_shi_feng' in 采集内容.keys():
                shi_fou_you_yi_wang_shi_feng = 采集内容['shi_fou_you_yi_wang_shi_feng']
            else:
                shi_fou_you_yi_wang_shi_feng = False
            if 'shi_fou_you_yi_kan_cha' in 采集内容.keys():
                shi_fou_you_yi_kan_cha = 采集内容['shi_fou_you_yi_kan_cha']
            else:
                shi_fou_you_yi_kan_cha = False
        自定义登录状态 = {
            '描述': '成功',
            'countries': [场所名称],
            'countries2': [建筑物编号],
            'countries3': [建筑物名称],
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
            'shi_fou_you_yi_kan_cha': shi_fou_you_yi_kan_cha

        }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')




def 下载建筑物名称(request):
    try:
        js_code = request.GET['code']
        countries_val = request.GET['countries_val']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': chou_jiang_appid, 'secret': chou_jiang_secret, 'js_code': js_code,
                   'grant_type': chou_jiang_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 抽奖用户表.objects(openid=r_json['openid']).first()
        抽奖主界面表first = 抽奖主界面表.objects(手机号=用户.手机号).first()
        if 抽奖主界面表first == None:
            四级部门 = ''
        else:
            四级部门 = 抽奖主界面表first.四级部门
        采集分工表objs = 采集分工表.objects(手机号=四级部门)
        countries2 = []
        countries3 = []
        for 采集分工表obj in 采集分工表objs:
            if 采集分工表obj.分工['场所名称'] == countries_val:
                countries2.append(采集分工表obj.分工['建筑物ID'])
                countries3.append(采集分工表obj.分工['建筑物名称'])
        自定义登录状态 = {
            '描述': '成功',
            'countries2': countries2,
            'countries3': countries3,
        }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')

def 上传采集结果(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': chou_jiang_appid, 'secret': chou_jiang_secret, 'js_code': js_code,
                   'grant_type': chou_jiang_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        # r_json = {'openid':'oPngn4yfqDljEh7wvTMD0NHddOOQ','session_key':'session_key'}
        当前时间戳 = time.time()
        当前时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        当前日期加一天 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400))
        当前日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        抽奖用户表first = 抽奖用户表.objects(openid=r_json['openid']).first()
        if 抽奖用户表first == None:
            自定义登录状态 = {
                '描述': '用户不存在',
                '会话': ''
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            手机号 = 抽奖用户表first.手机号
            建筑物编号 = request.GET['jian_zhu_wi_id']
            if request.GET['shi_fou_you_di_xia_ting_cha_chang'] == 'true':
                shi_fou_you_di_xia_ting_cha_chang = True
            else:
                shi_fou_you_di_xia_ting_cha_chang = False
            if request.GET['shi_fou_you_yi_wang_shi_feng'] == 'true':
                shi_fou_you_yi_wang_shi_feng = True
            else:
                shi_fou_you_yi_wang_shi_feng = False
            if request.GET['shi_fou_you_yi_kan_cha'] == 'true':
                shi_fou_you_yi_kan_cha = True
            else:
                shi_fou_you_yi_kan_cha = False
            采集内容 = {
                'chang_suo_lou_yu_zong_dong_shu':request.GET['chang_suo_lou_yu_zong_dong_shu'],
                'xian_chang_jing_du': request.GET['xian_chang_jing_du'],
                'xian_chang_wei_du': request.GET['xian_chang_wei_du'],
                'lou_yu_ceng_shu': request.GET['lou_yu_ceng_shu'],
                'di_xia_shi_ceng_shu': request.GET['di_xia_shi_ceng_shu'],
                'dian_ti_shu_liang': request.GET['dian_ti_shu_liang'],
                'dx_xia_zai': request.GET['dx_xia_zai'],
                'dx_shang_chuang': request.GET['dx_shang_chuang'],
                'yd_xia_zai': request.GET['yd_xia_zai'],
                'yd_shang_chuang': request.GET['yd_shang_chuang'],
                'shi_fou_you_di_xia_ting_cha_chang': shi_fou_you_di_xia_ting_cha_chang,
                'shi_fou_you_yi_wang_shi_feng': shi_fou_you_yi_wang_shi_feng,
                'shi_fou_you_yi_kan_cha': shi_fou_you_yi_kan_cha,
            }
            采集模版表first = 采集模版表.objects(建筑物编号=建筑物编号).first()
            if 采集模版表first == None:
                采集模版表(
                    手机号=手机号,
                    当前时间=当前时间,
                    建筑物编号=建筑物编号,
                    采集内容=采集内容
                ).save()
            else:
                采集模版表first.update(
                    手机号=手机号,
                    当前时间=当前时间,
                    建筑物编号=建筑物编号,
                    采集内容=采集内容
                )
            自定义登录状态 = {
                '描述':'上传成功',
                '会话':'',
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')

'''
FTP： 61.191.111.21:21613
User：wumm
Pass：CzCQT$0305
'''
def 上传图片(request):
    if request.method == 'POST':
        js_code = request.POST['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': chou_jiang_appid, 'secret': chou_jiang_secret, 'js_code': js_code,
                   'grant_type': chou_jiang_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        抽奖用户表first = 抽奖用户表.objects(openid=r_json['openid']).first()
        if 抽奖用户表first == None:
            自定义登录状态 = {
                '描述': '用户不存在',
                '会话': ''
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            手机号 = 抽奖用户表first.手机号
            抽奖主界面表first = 抽奖主界面表.objects(手机号=手机号).first()
            if 抽奖主界面表first == None:
                自定义登录状态 = {
                    '描述': '用户不存在',
                    '会话': ''
                }
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
            else:
                分公司 = 抽奖主界面表first.三级部门
                chang_suo_ming_cheng =  request.POST['chang_suo_ming_cheng']
                jian_zhu_wi_id = request.POST['jian_zhu_wu_id']
                jian_zhu_wu_ming_cheng = request.POST['jian_zhu_wu_ming_cheng']

                当前时间 = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
                采集模版表first = 采集模版表.objects(
                    建筑物编号=jian_zhu_wi_id
                ).first()
                if 采集模版表first == None:
                    pass
                else:
                    img_file = request.FILES.get('file')
                    folder = request.path.replace("/", "_")
                    uploaded_filename = 手机号+'_'+chang_suo_ming_cheng+'_'+jian_zhu_wi_id+'_'+jian_zhu_wu_ming_cheng+'_'+当前时间+'.jpg'
                    采集内容 = 采集模版表first.采集内容
                    采集内容['图片名称'] = uploaded_filename
                    采集模版表first.update(
                        采集内容=采集内容
                    )
                    with open(myConfig.django_root_path + '/'+folder+ '/'+uploaded_filename , 'wb+') as destination:
                        for chunk in img_file.chunks():
                            destination.write(chunk)
                    ftp = ftpconnect(两高楼宇采集host, 两高楼宇采集port, 两高楼宇采集username, 两高楼宇采集password)
                    uploadfile(ftp, '/' + 分公司 +'/' + uploaded_filename, myConfig.django_root_path + '/' + folder + '/' + uploaded_filename)
                    ftp.quit()
    return HttpResponse('200')

def write_csv(data,filename):
    with open(filename, 'w+' , newline='') as outf:
        writer = csv.DictWriter(outf, data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def 发邮件( 邮箱,文件名,姓名):
    import smtplib
    from email.header import Header
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    mail_host = 'smtp.qq.com'
    # receivers = '15305513057@189.cn'
    receivers = [邮箱]
    sender = myConfig.qq_mail_send
    passwd = myConfig.qq_mail_passwd
    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = Header("两高楼宇采集微信小程序", 'utf-8')
    message['To'] = Header(姓名, 'utf-8')
    subject = '两高楼宇采集表'
    message['Subject'] = Header(subject, 'utf-8')
    # 邮件正文内容
    message.attach(
        MIMEText(
            '这是两高楼宇采集微信小程序自动发出的邮件，请不要回复。若附件后缀名不可用，请下载后自行修改为 .csv',
            'plain',
            'utf-8'
        )
    )
    # 文件名 = '13093452622常柯仁淮南市20190323123702.csv'
    文件路径 = myConfig.django_root_path + '/' + 文件名
    # 构造附件1，传送当前目录下的 test.txt 文件
    att1 = MIMEText(open(文件路径, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="file.csv"'
    message.attach(att1)
    try:
        server = smtplib.SMTP_SSL(mail_host)
        server.login(sender, passwd)
        server.sendmail(sender, receivers, message.as_string())
        print('发送成功')
        return True
    except smtplib.SMTPException:
        print('无法发送')
        return False

@deprecated_async
def 异步执行两高采集表发邮件(抽奖用户表first,mail_addr):
    手机号 = 抽奖用户表first.手机号
    抽奖主界面表obj = 抽奖主界面表.objects(手机号=手机号).first()
    try:
        手机号 = 抽奖主界面表obj.手机号
        姓名 = 抽奖主界面表obj.姓名
        三级部门 = 抽奖主界面表obj.三级部门
        主界内容 = 抽奖主界面表obj.主界内容
        page_name_list = []
        for 主界内容one in 主界内容:
            pages = 主界内容one['pages']
            for page in pages:
                page_name = page['page_name']
                if page_name in page_name_list:
                    pass
                else:
                    page_name_list.append(page_name)
        手机号list = []
        当前时间1list = []
        建筑物编号list = []
        场所楼宇总栋数1list = []
        现场经度list = []
        现场纬度list = []
        楼宇层数list = []
        地下室层数list = []
        电梯数量list = []
        电信下载速率list = []
        电信上传速率list = []
        移动下载速率list = []
        移动上传速率list = []
        区市县list = []
        场所名称list = []
        建筑物名称list = []
        是否有地下停车场list = []
        是否有异网室分list = []
        是否已勘查list = []
        for page_name_list_one in page_name_list:
            采集分工表objs = 采集分工表.objects(
                手机号=page_name_list_one
            )
            for 采集分工表one in 采集分工表objs:
                建筑物编号 = 采集分工表one.建筑物编号
                采集模版表first = 采集模版表.objects(建筑物编号=建筑物编号).first()
                if 采集模版表first == None:
                    continue
                else:
                    区市县 = 采集分工表one.分工['区市县']
                    场所名称 = 采集分工表one.分工['场所名称']
                    建筑物名称 = 采集分工表one.分工['建筑物名称']
                    采集内容 = 采集模版表first.采集内容
                    场所楼宇总栋数 = 采集内容['chang_suo_lou_yu_zong_dong_shu']
                    现场经度 = 采集内容['xian_chang_jing_du']
                    现场纬度 = 采集内容['xian_chang_wei_du']
                    楼宇层数 = 采集内容['lou_yu_ceng_shu']
                    地下室层数 = 采集内容['di_xia_shi_ceng_shu']
                    电梯数量 = 采集内容['dian_ti_shu_liang']
                    电信下载速率 = 采集内容['dx_xia_zai']
                    电信上传速率 = 采集内容['dx_shang_chuang']
                    移动下载速率 = 采集内容['yd_xia_zai']
                    移动上传速率 = 采集内容['yd_shang_chuang']
                    if 'shi_fou_you_di_xia_ting_cha_chang' in 采集内容:
                        shi_fou_you_di_xia_ting_cha_chang = 采集内容['shi_fou_you_di_xia_ting_cha_chang']
                    else:
                        shi_fou_you_di_xia_ting_cha_chang = False
                    if 'shi_fou_you_yi_wang_shi_feng' in 采集内容:
                        shi_fou_you_yi_wang_shi_feng = 采集内容['shi_fou_you_yi_wang_shi_feng']
                    else:
                        shi_fou_you_yi_wang_shi_feng = False
                    if 'shi_fou_you_yi_kan_cha' in 采集内容:
                        shi_fou_you_yi_kan_cha = 采集内容['shi_fou_you_yi_kan_cha']
                    else:
                        shi_fou_you_yi_kan_cha = False
                    if shi_fou_you_di_xia_ting_cha_chang:
                        是否有地下停车场 = '是'
                    else:
                        是否有地下停车场 = '否'
                    if shi_fou_you_yi_wang_shi_feng:
                        是否有异网室分 = '是'
                    else:
                        是否有异网室分 = '否'
                    if shi_fou_you_yi_kan_cha:
                        是否已勘查 = '是'
                    else:
                        是否已勘查 = '否'
                    当前时间 = 采集模版表first.当前时间
                    区市县list.append(区市县)
                    场所名称list.append(场所名称)
                    建筑物名称list.append(建筑物名称)
                    手机号list.append(手机号)
                    当前时间1list.append(当前时间)
                    建筑物编号list.append(建筑物编号)
                    场所楼宇总栋数1list.append(场所楼宇总栋数)
                    现场经度list.append(现场经度)
                    现场纬度list.append(现场纬度)
                    楼宇层数list.append(楼宇层数)
                    地下室层数list.append(地下室层数)
                    电梯数量list.append(电梯数量)
                    电信下载速率list.append(电信下载速率)
                    电信上传速率list.append(电信上传速率)
                    移动下载速率list.append(移动下载速率)
                    移动上传速率list.append(移动上传速率)
                    是否有地下停车场list.append(是否有地下停车场)
                    是否有异网室分list.append(是否有异网室分)
                    是否已勘查list.append(是否已勘查)
        jie_guo_df = pandas.DataFrame({
            '区市县': 区市县list,
            '场所名称': 场所名称list,
            '建筑物名称': 建筑物名称list,
            '手机号': 手机号list,
            '当前时间': 当前时间1list,
            '建筑物编号': 建筑物编号list,
            '场所楼宇总栋数': 场所楼宇总栋数1list,
            '现场经度': 现场经度list,
            '现场纬度': 现场纬度list,
            '楼宇层数': 楼宇层数list,
            '地下室层数': 地下室层数list,
            '电梯数量': 电梯数量list,
            '电信下载速率': 电信下载速率list,
            '电信上传速率': 电信上传速率list,
            '移动下载速率': 移动下载速率list,
            '移动上传速率': 移动上传速率list,
            '是否有地下停车场': 是否有地下停车场list,
            '是否有异网室分': 是否有异网室分list,
            '是否已勘查': 是否已勘查list,
        })
        创建时间 = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        file_name = 手机号 + 姓名 + 三级部门 + 创建时间 + '.csv'
        jie_guo_df.to_csv(file_name, encoding='gbk')
        邮箱 = mail_addr
        文件名 = file_name
        发邮件(邮箱, 文件名, 姓名)
    except:
        print(traceback.format_exc())

def 两高采集表发邮件(request):
    js_code = request.GET['code']
    mail_addr = request.GET['mail_addr']
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    payload = {'appid': chou_jiang_appid, 'secret': chou_jiang_secret, 'js_code': js_code,
               'grant_type': chou_jiang_grant_type}
    r = requests.get(url=url, params=payload)
    r_json = json.loads(r.text)
    抽奖用户表first = 抽奖用户表.objects(openid=r_json['openid']).first()
    if 抽奖用户表first == None:
        自定义登录状态 = {
            '描述': '用户不存在',
            '会话': ''
        }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)
    else:
        try:
            import re
            re_rule = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
            if re.match(re_rule, mail_addr):
                手机号 = 抽奖用户表first.手机号
                抽奖主界面表obj = 抽奖主界面表.objects(手机号=手机号).first()
                if 抽奖主界面表obj == None:
                    自定义登录状态 = {
                        '描述': '用户不存在',
                        '会话': ''
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                else:
                    抽奖主界面表obj.update(
                        验证码标题 = mail_addr
                    )
                    异步执行两高采集表发邮件(抽奖主界面表obj,mail_addr)
                    自定义登录状态 = {
                        '描述': '成功',
                        '会话': ''
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
        except:
            print(traceback.format_exc())
        自定义登录状态 = {
            '描述': '邮箱格式错误',
            '会话': ''
        }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)

def 下载数据(request):
    采集模版表objs = 采集模版表.objects
    手机号list = []
    当前时间1list = []
    建筑物编号list = []
    场所楼宇总栋数1list = []
    现场经度list = []
    现场纬度list = []
    楼宇层数list = []
    地下室层数list = []
    电梯数量list = []
    电信下载速率list = []
    电信上传速率list = []
    移动下载速率list = []
    移动上传速率list = []
    区市县list = []
    场所名称list = []
    建筑物名称list = []
    是否有地下停车场list = []
    是否有异网室分list = []
    是否已勘查list = []
    for 采集模版表one in 采集模版表objs:
        手机号 = 采集模版表one.手机号
        当前时间 = 采集模版表one.当前时间
        建筑物编号 = 采集模版表one.建筑物编号
        采集分工表first = 采集分工表.objects(建筑物编号=建筑物编号).first()
        if 采集分工表first == None:
            区市县 = ''
            场所名称 = ''
            建筑物名称 = ''
        else:
            区市县 = 采集分工表first.分工['区市县']
            场所名称 = 采集分工表first.分工['场所名称']
            建筑物名称 =采集分工表first.分工['建筑物名称']
        采集内容 = 采集模版表one.采集内容
        场所楼宇总栋数 = 采集内容['chang_suo_lou_yu_zong_dong_shu']
        现场经度 = 采集内容['xian_chang_jing_du']
        现场纬度 = 采集内容['xian_chang_wei_du']
        楼宇层数 = 采集内容['lou_yu_ceng_shu']
        地下室层数 = 采集内容['di_xia_shi_ceng_shu']
        电梯数量 = 采集内容['dian_ti_shu_liang']
        电信下载速率 = 采集内容['dx_xia_zai']
        电信上传速率 = 采集内容['dx_shang_chuang']
        移动下载速率 = 采集内容['yd_xia_zai']
        移动上传速率 = 采集内容['yd_shang_chuang']
        if 'shi_fou_you_di_xia_ting_cha_chang' in 采集内容:
            shi_fou_you_di_xia_ting_cha_chang = 采集内容['shi_fou_you_di_xia_ting_cha_chang']
        else:
            shi_fou_you_di_xia_ting_cha_chang = False
        if 'shi_fou_you_yi_wang_shi_feng' in 采集内容:
            shi_fou_you_yi_wang_shi_feng = 采集内容['shi_fou_you_yi_wang_shi_feng']
        else:
            shi_fou_you_yi_wang_shi_feng = False
        if 'shi_fou_you_yi_kan_cha' in 采集内容:
            shi_fou_you_yi_kan_cha = 采集内容['shi_fou_you_yi_kan_cha']
        else:
            shi_fou_you_yi_kan_cha = False
        if shi_fou_you_di_xia_ting_cha_chang:
            是否有地下停车场 = '是'
        else:
            是否有地下停车场 = '否'
        if shi_fou_you_yi_wang_shi_feng:
            是否有异网室分 = '是'
        else:
            是否有异网室分 = '否'
        if shi_fou_you_yi_kan_cha:
            是否已勘查 = '是'
        else:
            是否已勘查 = '否'
        区市县list.append(区市县)
        场所名称list.append(场所名称)
        建筑物名称list.append(建筑物名称)
        手机号list.append(手机号)
        当前时间1list.append(当前时间)
        建筑物编号list.append(建筑物编号)
        场所楼宇总栋数1list.append(场所楼宇总栋数)
        现场经度list.append(现场经度)
        现场纬度list.append(现场纬度)
        楼宇层数list.append(楼宇层数)
        地下室层数list.append(地下室层数)
        电梯数量list.append(电梯数量)
        电信下载速率list.append(电信下载速率)
        电信上传速率list.append(电信上传速率)
        移动下载速率list.append(移动下载速率)
        移动上传速率list.append(移动上传速率)
        是否有地下停车场list.append(是否有地下停车场)
        是否有异网室分list.append(是否有异网室分)
        是否已勘查list.append(是否已勘查)
    jie_guo_df = pandas.DataFrame({
        '区市县':区市县list,
        '场所名称':场所名称list,
        '建筑物名称':建筑物名称list,
        '手机号': 手机号list,
        '当前时间': 当前时间1list,
        '建筑物编号': 建筑物编号list,
        '场所楼宇总栋数': 场所楼宇总栋数1list,
        '现场经度': 现场经度list,
        '现场纬度': 现场纬度list,
        '楼宇层数': 楼宇层数list,
        '地下室层数': 地下室层数list,
        '电梯数量': 电梯数量list,
        '电信下载速率': 电信下载速率list,
        '电信上传速率': 电信上传速率list,
        '移动下载速率': 移动下载速率list,
        '移动上传速率': 移动上传速率list,
        '是否有地下停车场': 是否有地下停车场list,
        '是否有异网室分': 是否有异网室分list,
        '是否已勘查': 是否已勘查list,
    })
    创建时间 = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    file_name = '采集模版表' + 创建时间 + '.csv'
    jie_guo_df.to_csv(file_name, encoding='gbk')
    path = myConfig.django_root_path + '/' + file_name
    outfile = open(path, 'rb')
    response = FileResponse(outfile)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s"' % "采集模版表.csv"
    return response

def 下载采集内容(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': chou_jiang_appid, 'secret': chou_jiang_secret, 'js_code': js_code,
                   'grant_type': chou_jiang_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 抽奖用户表.objects(openid=r_json['openid']).first()
        jian_zhu_wu_id_val = request.GET['jian_zhu_wu_id_val']
        采集模版表first = 采集模版表.objects(建筑物编号=jian_zhu_wu_id_val).first()
        if 采集模版表first == None:
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
            手机号 = 采集模版表first.手机号
            当前时间 = 采集模版表first.当前时间
            建筑物编号 = 采集模版表first.建筑物编号
            采集内容 = 采集模版表first.采集内容
            场所楼宇总栋数 = 采集内容['chang_suo_lou_yu_zong_dong_shu']
            现场经度 = 采集内容['xian_chang_jing_du']
            现场纬度 = 采集内容['xian_chang_wei_du']
            楼宇层数 = 采集内容['lou_yu_ceng_shu']
            地下室层数 = 采集内容['di_xia_shi_ceng_shu']
            电梯数量 = 采集内容['dian_ti_shu_liang']
            电信下载速率 = 采集内容['dx_xia_zai']
            电信上传速率 = 采集内容['dx_shang_chuang']
            移动下载速率 = 采集内容['yd_xia_zai']
            移动上传速率 = 采集内容['yd_shang_chuang']
            if 'shi_fou_you_di_xia_ting_cha_chang' in 采集内容.keys():
                shi_fou_you_di_xia_ting_cha_chang = 采集内容['shi_fou_you_di_xia_ting_cha_chang']
            else:
                shi_fou_you_di_xia_ting_cha_chang = False
            if 'shi_fou_you_yi_wang_shi_feng' in 采集内容.keys():
                shi_fou_you_yi_wang_shi_feng = 采集内容['shi_fou_you_yi_wang_shi_feng']
            else:
                shi_fou_you_yi_wang_shi_feng = False
            if 'shi_fou_you_yi_kan_cha' in 采集内容.keys():
                shi_fou_you_yi_kan_cha = 采集内容['shi_fou_you_yi_kan_cha']
            else:
                shi_fou_you_yi_kan_cha = False
        自定义登录状态 = {
            '描述': '成功',
            'chang_suo_lou_yu_zong_dong_shu':场所楼宇总栋数,
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
            'shi_fou_you_yi_kan_cha': shi_fou_you_yi_kan_cha
        }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        print(自定义登录状态)
        return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')

def 修改基本信息(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': chou_jiang_appid, 'secret': chou_jiang_secret, 'js_code': js_code,
                   'grant_type': chou_jiang_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 抽奖用户表.objects(openid=r_json['openid']).first()
        if 用户 == None:
            自定义登录状态 = {
                '描述':'未注册的用户'
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            抽奖主界面表first = 抽奖主界面表.objects(手机号=用户.手机号).first()
            if 抽奖主界面表first == None:
                自定义登录状态 = {
                    '描述': '没有权限'
                }
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
            else:
                chang_suo_ming_cheng = request.GET['chang_suo_ming_cheng']
                jian_zhu_wu_id = request.GET['jian_zhu_wu_id']
                jian_zhu_wu_ming_cheng = request.GET['jian_zhu_wu_ming_cheng']
                采集分工表first = 采集分工表.objects(建筑物编号=jian_zhu_wu_id).first()
                if 采集分工表first == None:
                    自定义登录状态 = {
                        '描述': '没有分工'
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                else:
                    分工 = 采集分工表first.分工
                    if jian_zhu_wu_id == 分工['建筑物ID']:
                        场所名称 = 分工['场所名称']
                        建筑物名称 =  分工['建筑物名称']
                        分工['场所名称'] = chang_suo_ming_cheng
                        分工['建筑物名称'] = jian_zhu_wu_ming_cheng
                        修改记录 = {
                            '修改人':用户.手机号,
                            '修改时间':  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                            '老场所名称':场所名称,
                            '老建筑物名称': 建筑物名称,
                            '新场所名称':chang_suo_ming_cheng,
                            '新建筑物名称':jian_zhu_wu_ming_cheng
                        }
                        采集分工表first.update(
                            分工=分工,
                            修改记录 = 修改记录
                        )
                        自定义登录状态 = {
                            '描述': '成功',
                        }
                        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                        自定义登录状态 = str(自定义登录状态)
                        return HttpResponse(自定义登录状态)
                自定义登录状态 = {
                    '描述': '建筑物编号不存在',
                }
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')

@deprecated_async
def 异步计算录入情况(page_name):
    采集分工表objs = 采集分工表.objects(
        手机号=page_name
    )
    场所名称list = []
    for 采集分工表obj in 采集分工表objs:
        分工 = 采集分工表obj.分工
        场所名称 = 分工['场所名称']
        if 场所名称 in 场所名称list:
            pass
        else:
            场所名称list.append(场所名称)
    print('场所名称list',len(场所名称list))
    print('采集分工表objs',len(采集分工表objs))
    分工list = []
    for index, 场所名称one in enumerate(场所名称list):
        lou_ceng_list = []
        lou_ceng_index = 0
        ceng_list = []
        i = 0
        for 采集分工表obj in 采集分工表objs:
            分工 = 采集分工表obj.分工
            场所名称 = 分工['场所名称']
            if 场所名称one == 场所名称:
                i = i + 1
                建筑物ID = str(分工['建筑物ID'])
                建筑物名称 = str(分工['建筑物名称'])
                采集模版表first = 采集模版表.objects(
                    建筑物编号=建筑物ID
                ).first()
                if 采集模版表first == None:
                    zhuang_tai = 可录入
                else:
                    if 'shi_fou_you_yi_kan_cha' in 采集模版表first.采集内容:
                        if 采集模版表first.采集内容['shi_fou_you_yi_kan_cha']:
                            昨天 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - 604800))
                            当前时间 = 采集模版表first.当前时间
                            if 当前时间 > 昨天:
                                zhuang_tai = 新录入
                            else:
                                zhuang_tai = 已录入
                        else:
                            zhuang_tai = 可录入
                    else:
                        zhuang_tai = 可录入
                men_pai_dict = {
                    'men_pai_id': page_name + 建筑物主键分隔符 + 场所名称 + 建筑物主键分隔符 + 建筑物ID + 建筑物主键分隔符 + 建筑物名称,
                    'men_pai_hao': 建筑物名称,
                    'zhuang_tai': zhuang_tai,
                }
                ceng_list.append(men_pai_dict)
                if i % 3 == 0:
                    lou_ceng_dict = {
                        'lou_ceng_id': lou_ceng_index,
                        'ceng': ceng_list
                    }
                    ceng_list = []
                    lou_ceng_list.append(lou_ceng_dict)
                    lou_ceng_index = lou_ceng_index + 1
        if i % 3 == 1 or i % 3 == 2:
            lou_ceng_dict = {
                'lou_ceng_id': lou_ceng_index,
                'ceng': ceng_list
            }
            lou_ceng_list.append(lou_ceng_dict)
        dan_yuan_list = {
            'dan_yuan_id': index,
            'dan_yuan_name': 场所名称one,
            'dan_yuan': lou_ceng_list
        }
        分工list.append(dan_yuan_list)
    录入分工表first = 采集录入分工表.objects(
        责任人=page_name
    ).first()
    if 录入分工表first == None:
        采集录入分工表(
            责任人 = page_name,
            录入分工 = 分工list
        ).save()
    else:
        录入分工表first.update(
            责任人=page_name,
            录入分工=分工list
        )

def 下载录入数据(request):
    try:
        js_code = request.GET['code']
        name = request.GET['name']
        page_name = request.GET['page_name']
        page_desc = request.GET['page_desc']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': chou_jiang_appid, 'secret': chou_jiang_secret, 'js_code': js_code,
                   'grant_type': chou_jiang_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 抽奖用户表.objects(openid=r_json['openid']).first()
        主界面表first = 抽奖主界面表.objects(手机号=用户.手机号).first()
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


        异步计算录入情况(page_name)
        录入分工表first = 采集录入分工表.objects(
            责任人=page_name
        ).first()
        if 录入分工表first == None:
            分工list = []
        else:
            分工list = 录入分工表first.录入分工
        分工list_len = len(分工list)
        分工list_len_取整除 = 分工list_len // 分页
        分工list_len_取整除 = 分工list_len_取整除 +1
        countries = list( range(0,分工list_len_取整除) )
        countries_val = 0
        分工list_slice = 分工list[countries_val * 分页: (countries_val + 1) * 分页]
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


def 下载图片(request):
    try:
        bindMenPaiHao_id = request.GET['bindMenPaiHao_id']
        bindMenPaiHao_id_list = bindMenPaiHao_id.split(建筑物主键分隔符)
        print(bindMenPaiHao_id_list)
        责任人 = bindMenPaiHao_id_list[0]
        场所名称 = bindMenPaiHao_id_list[1]
        建筑物编号 = bindMenPaiHao_id_list[2]
        建筑物名称 = bindMenPaiHao_id_list[3]
        采集模版表first = 采集模版表.objects(建筑物编号=建筑物编号).first()
        if 采集模版表first == None:
            path = myConfig.django_root_path + '/' + 'mysite' + '/' + '404.jpg'
            outfile = open(path, 'rb')
            response = FileResponse(outfile)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="%s"' % "采集模版表.csv"
            return response
        else:
            uploaded_filename = 采集模版表first.采集内容['图片名称']
            path = myConfig.django_root_path + '/' + '_chou_jiang_shang_chuang_tu_pian_' + '/' + uploaded_filename
            outfile = open(path, 'rb')
            response = FileResponse(outfile)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="%s"' % "采集模版表.csv"
            return response
    except:
        print(traceback.format_exc())
        return HttpResponse('500')


def 录入分页(request):
    try:
        js_code = request.GET['code']
        name = request.GET['name']
        page_name = request.GET['page_name']
        page_desc = request.GET['page_desc']
        countries_val = int( request.GET['countries_val'] )

        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': chou_jiang_appid, 'secret': chou_jiang_secret, 'js_code': js_code,
                   'grant_type': chou_jiang_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 抽奖用户表.objects(openid=r_json['openid']).first()
        主界面表first = 抽奖主界面表.objects(手机号=用户.手机号).first()
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

        录入分工表first = 采集录入分工表.objects(
            责任人=page_name
        ).first()
        if 录入分工表first == None:
            分工list = []
        else:
            分工list = 录入分工表first.录入分工

        分工list_slice = 分工list[ countries_val*分页 : (countries_val+1)*分页 ]
        print(分工list_slice)

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


