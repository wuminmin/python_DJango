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
import sys

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