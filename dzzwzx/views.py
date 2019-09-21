from . import models
import datetime
import hashlib
import json
import traceback
import uuid
import pandas
import pytz
import requests
import time
from django.http import HttpResponse, FileResponse
from django.shortcuts import render_to_response,render
import myConfig
from . import models
import sys
from django.shortcuts import redirect

#微信认证
def wx(request):
    signature = request.GET["signature"]
    timestamp = request.GET["timestamp"]
    nonce = request.GET["nonce"]
    echostr = request.GET["echostr"]
    token = myConfig.wxyy_token
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

# Create your views here.
def zc(request):
    # code = request.GET['code']
    # print(code)
    # return HttpResponse('{"openid":code}')
    code = request.GET['code']
    js_code = request.GET['code']
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
    payload = {'appid': myConfig.mskj_appid, 'secret': myConfig.mskj_scrit, 'code': js_code,
                'grant_type': myConfig.mskj_grant_type}
    r = requests.get(url=url, params=payload)
    r_json = json.loads(r.text)
    print(r_json)
    access_token = r_json['access_token']
    refresh_token = r_json['refresh_token']
    openid = r_json['openid']

    print(code)
    res = '{"openid":'+openid+'}'
    response = HttpResponse(res)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def dl(request):
    from urllib import parse
    myOtherUrl = parse.quote('https://wx.wuminmin.top/dzzwzx/dl_2/')
    my_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid='+myConfig.wxyy_appid+'&redirect_uri='+myOtherUrl+'&response_type=code&scope=snsapi_userinfo&state=123#wechat_redirect'
    return redirect(my_url)

def dl_2(request):
    js_code = request.GET['code']
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
    payload = {'appid': myConfig.wxyy_appid, 'secret': myConfig.wxyy_scrit, 'code': js_code,
                'grant_type': myConfig.wxyy_grant_type}
    r = requests.get(url=url, params=payload)
    print(r.text)
    r_json = json.loads(r.text)
    access_token = r_json['access_token']
    refresh_token = r_json['refresh_token']
    openid = r_json['openid']
    qset0 = models.微信预约用户表.objects(openid=openid).first()
    if qset0 == None:
        return redirect(models.react_url+'zhuce')
    else:
        return redirect(models.react_url+'contact')
    # res = '{"openid":'+openid+'}'
    # response = HttpResponse(res)
    # response["Access-Control-Allow-Origin"] = "*"
    # response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    # response["Access-Control-Max-Age"] = "1000"
    # response["Access-Control-Allow-Headers"] = "*"
    # return response
    # return redirect('http://www.baidu.com')

def sendSms(request):
    try:
        手机号 = str(request.GET['手机号'])
        if 手机号 == '':
            # return HttpResponse("手机号为空")
            response = HttpResponse('手机号为空')
           
        else:
            import random
            j = 6
            验证码 = ''.join(str(i) for i in random.sample(range(0, 9), j))  # sample(seq, n) 从序列seq中选择n个随机且独立的元素；
            __business_id = uuid.uuid1()
            params = "{\"code\":\"" + 验证码 + "\"}"
            from mysite.demo_sms_send import send_sms
            r = send_sms(__business_id, 手机号, sign_name, template_code, params)
            r2 = json.loads(r)
            if r2['Code'] == 'OK':
                r = models.微信预约验证码表(验证码=验证码, 手机号=手机号).save()
            response = HttpResponse(r2['Code'])
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    except:
        response = HttpResponse('500')
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    