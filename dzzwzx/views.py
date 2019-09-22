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
    code = request.GET['code']
    js_code = request.GET['code']
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
    payload = {'appid': myConfig.mskj_appid, 'secret': myConfig.mskj_scrit, 'code': js_code,
                'grant_type': myConfig.mskj_grant_type}
    r = requests.get(url=url, params=payload)
    r_json = json.loads(r.text)
    access_token = r_json['access_token']
    refresh_token = r_json['refresh_token']
    openid = r_json['openid']
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
    r_json = json.loads(r.text)
    access_token = r_json['access_token']
    refresh_token = r_json['refresh_token']
    openid = r_json['openid']
    qset0 = models.微信预约用户表.objects(openid=openid).first()
    if qset0 == None:
        models.微信预约用户表(
            openid=openid,
            access_token=access_token,
            refresh_token=refresh_token
        ).save()
        return redirect(models.react_url+'zhuce'+'?access_token='+access_token+'&refresh_token='+refresh_token)
    else:
        qset0.update(
            access_token=access_token,
            refresh_token=refresh_token
        )
        if qset0.手机号 == '':
            return redirect(models.react_url+'zhuce'+'?access_token='+access_token+'&refresh_token='+refresh_token)
        else:
            手机号 = qset0.手机号
            姓名 = qset0.其它['姓名']
            身份证号码 = qset0.其它['身份证号码']
            return redirect(
                models.react_url+'userInfo'+'?\
                access_token='+access_token+\
                '&refresh_token='+refresh_token+\
                '&手机号='+手机号+\
                '&姓名='+姓名+\
                '&身份证号码='+身份证号码)

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
            r = send_sms(__business_id, 手机号, myConfig.sign_name, myConfig.template_code, params)
            r2 = json.loads(r)
            if r2['Code'] == 'OK':
                r = models.微信预约验证码表(验证码=验证码, 手机号=手机号).save()
                response = HttpResponse('短信发送成功')
            response = HttpResponse('请输入正确的手机号')
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    except:
        import traceback
        print(traceback.format_exc())
        response = HttpResponse('系统故障')
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

def zhuce(request):
    try:
        myState = str(request.GET['myState'])
        print(myState)
        myState_json = json.loads(myState)
        access_token = myState_json['access_token']
        refresh_token = myState_json['refresh_token']
        qset0 = models.微信预约用户表.objects(access_token=access_token).first()
        if qset0 == None:
            response = HttpResponse('用户未注册')
        else:
            姓名 = myState_json['姓名']
            验证码 = myState_json['验证码']
            手机号 = myState_json['手机号']
            身份证号码 = myState_json['身份证号码']
            qset1 = models.微信预约验证码表.objects(验证码=验证码,手机号=手机号).first()
            if qset1 == None:
                response = HttpResponse('验证码错误')
            else:
                qset0.update(
                    手机号=手机号,
                    其它={'姓名':姓名,'身份证号码':身份证号码}
                )
                response = HttpResponse('注册成功')
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    except:
        import traceback
        print(traceback.format_exc())
        response = HttpResponse('系统故障')
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

#预约
def yy(request):
    from urllib import parse
    myOtherUrl = parse.quote('https://wx.wuminmin.top/dzzwzx/yy2/')
    my_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid='+myConfig.wxyy_appid+'&redirect_uri='+myOtherUrl+'&response_type=code&scope=snsapi_userinfo&state=123#wechat_redirect'
    return redirect(my_url)

#预约认证
def yy2(request):
    js_code = request.GET['code']
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
    payload = {'appid': myConfig.wxyy_appid, 'secret': myConfig.wxyy_scrit, 'code': js_code,
                'grant_type': myConfig.wxyy_grant_type}
    r = requests.get(url=url, params=payload)
    r_json = json.loads(r.text)
    access_token = r_json['access_token']
    refresh_token = r_json['refresh_token']
    openid = r_json['openid']
    qset0 = models.微信预约用户表.objects(openid=openid).first()
    if qset0 == None:
        models.微信预约用户表(
            openid=openid,
            access_token=access_token,
            refresh_token=refresh_token
        ).save()
        return redirect(models.react_url+'zhuce'+'?access_token='+access_token+'&refresh_token='+refresh_token)
    else:
        qset0.update(
            access_token=access_token,
            refresh_token=refresh_token
        )
        if qset0.手机号 == '':
            return redirect(models.react_url+'zhuce'+'?access_token='+access_token+'&refresh_token='+refresh_token)
        else:
            手机号 = qset0.手机号
            姓名 = qset0.其它['姓名']
            身份证号码 = qset0.其它['身份证号码']
            print('---------------------------------------',access_token)
            return redirect(
                models.react_url+'yuyue'+'?\
                access_token='+access_token+\
                '&refresh_token='+refresh_token+\
                '&手机号='+手机号+\
                '&姓名='+姓名+\
                '&身份证号码='+身份证号码)

def icon(request):
    from django.shortcuts import render
    import myConfig
    import datetime
    import json
    import traceback
    import uuid
    import os
    import pandas
    import requests
    import time
    from django.http import HttpResponse, FileResponse
    from . import models
    try:
        部门编号 = request.GET['id']
        qset = models.微信预约部门表.objects(部门编号=部门编号).first()
        if qset == None:
            path = myConfig.django_root_path + '/' + 'mysite' + '/' + '404.png'
            outfile = open(path, 'rb')
            response = FileResponse(outfile)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="%s"' % "image.jpg"
            return response
        else:
            image = qset.部门图标.read()
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

def 下载部门列表(request):
    jsonstr = models.微信预约部门表.objects.to_json().encode('utf-8').decode('unicode_escape')
    response = HttpResponse(jsonstr)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def 提交办事申请(request):
    try:
        myState = str(request.GET['myState'])
        myState_json = json.loads(myState)
        access_token = myState_json['access_token']
        refresh_token = myState_json['refresh_token']
        qset0 = models.微信预约用户表.objects(refresh_token=refresh_token).first()
        if qset0 == None:
            response = HttpResponse('用户未注册')
        else:
            姓名 = myState_json['姓名']
            验证码 = myState_json['验证码']
            手机号 = myState_json['手机号']
            身份证号码 = myState_json['身份证号码']
            部门编号 = myState_json['部门编号']
            部门名称 = myState_json['部门名称']
            办事内容 = myState_json['办事内容']
            办事日期 = myState_json['办事日期']
            办事区间 = myState_json['办事区间']
            其它 = {}
            qset1 = models.微信预约用户表.objects(refresh_token=refresh_token,手机号=手机号).first()
            if qset1 == None:
                response = HttpResponse('未绑定手机')
            else:
                qset2 = models.微信预约办事申请表.objects(openid=qset1.openid,部门编号=部门编号,
                部门名称=部门名称,办事日期=办事日期,办事区间=办事区间).first()
                if qset2 == None:
                    models.微信预约办事申请表(
                        openid = qset1.openid,
                        部门编号 = 部门编号,
                        部门名称 = 部门名称,
                        办事内容 = 办事内容,
                        办事日期 = 办事日期,
                        办事区间 = 办事区间,
                        其它 = 其它
                    ).save()
                    response = HttpResponse('预约成功')
                else:
                    qset2.update(
                        部门编号 = 部门编号,
                        部门名称 = 部门名称,
                        办事内容 = 办事内容,
                        办事日期 = 办事日期,
                        办事区间 = 办事区间,
                        其它 =其它
                    )
                    response = HttpResponse('更新预约成功')
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    except:
        import traceback
        print(traceback.format_exc())
        response = HttpResponse('系统故障')
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

def 下载预约列表(request):
    try:
        myState = str(request.GET['myState'])
        print('下载预约列表myState----------------',myState)
        myState_json = json.loads(myState)
        refresh_token = myState_json['refresh_token']
        qset0 = models.微信预约用户表.objects(refresh_token=refresh_token).first()
        if qset0 == None:
            response = HttpResponse('[]')
        else:
            jsonstr = models.微信预约办事申请表.objects(openid=qset0.openid).to_json().encode('utf-8').decode('unicode_escape')
            print(jsonstr)
            response = HttpResponse(jsonstr)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    except:
        import traceback
        print(traceback.format_exc())
        response = HttpResponse(['系统故障'])
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response