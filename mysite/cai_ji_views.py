import hashlib
import json
import random
import traceback
import uuid

import bson
import requests
import time
from django.http import HttpResponse
import pymongo
from pandocfilters import Math
from pymongo import MongoClient
import myConfig
from myConfig import chou_jiang_appid, chou_jiang_secret, chou_jiang_grant_type, sign_name, template_code
from mysite.chou_jiang_mongo import 抽奖用户表, 抽奖登录状态表, 抽奖验证码表, 抽奖主界面表, 没中奖, 抽奖开关, 中奖人数字典, 中奖金额字典, 抽奖状态表, 一等奖, \
    二等奖, 抽奖参与者, 全体奖, 三等奖, 四等奖, 未开始, 抽奖开始, 抽奖结束, 抽奖全体奖状态表, 抽奖按钮状态
from mysite.demo_sms_send import send_sms

def 采集推送微信验证(request):
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

def 采集登录检查(request):
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
        else:
            r = 抽奖登录状态表(session_key=r_json['session_key'], openid=r_json['openid']).save()
            自定义登录状态 = "{\"描述\":\"新界面\",\"会话\":\"" + str(r.id) + "\"}"
            return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')

def 采集发送验证码(request):
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
        return HttpResponse('500')

def 采集校验验证码(request):
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

def 采集下载主界面数据(request):
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



def 采集初始化(request):
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