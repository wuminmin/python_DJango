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
from tieta import models

def images(request):
    try:
        id = request.GET['id']
        qset = models.tou_piao_image_col.objects(wxyl_id=id).first()
        print(qset)
        if qset == None:
            path = myConfig.django_root_path + '/' + 'mysite' + '/' + '404.png'
            outfile = open(path, 'rb')
            response = FileResponse(outfile)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="%s"' % "image.jpg"
            return response
        else:
            image = qset.wxyl_image.read()
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

def dl(request):
    from . import models
    from urllib import parse
    myOtherUrl = parse.quote('https://wx.wuminmin.top/tieta/dl_2')
    my_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid='+myConfig.mskj_appid+'&redirect_uri='+myOtherUrl+'&response_type=code&scope=snsapi_userinfo&state=123#wechat_redirect'
    from django.shortcuts import redirect
    return redirect(my_url)

def dl_2(request):
    from . import models
    from django.shortcuts import redirect
    js_code = request.GET['code']
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
    payload = {'appid': myConfig.mskj_appid, 'secret': myConfig.mskj_scrit, 'code': js_code,
                'grant_type': myConfig.mskj_grant_type}
    r = requests.get(url=url, params=payload)
    r_json = json.loads(r.text)
    access_token = r_json['access_token']
    refresh_token = r_json['refresh_token']
    openid = r_json['openid']
    qset0 = models.铁塔用户表.objects(openid=openid).first()
    if qset0 == None:
        models.铁塔用户表(
            openid=openid,
            access_token=access_token,
            refresh_token=refresh_token
        ).save()
        return redirect(models.react_url+'tietazhuche'+'?access_token='+access_token+'&refresh_token='+refresh_token)
    else:
        qset0.update(
            access_token=access_token,
            refresh_token=refresh_token
        )
        if qset0.手机号 == '':
            return redirect(models.react_url+'tietazhuche'+'?access_token='+access_token+'&refresh_token='+refresh_token)
        else:
            手机号 = qset0.手机号
            姓名 = qset0.其它['姓名']
            身份证号码 = qset0.其它['身份证号码']
            return redirect(
                models.react_url+'tieta'+'?\
                access_token='+access_token+\
                '&refresh_token='+refresh_token+\
                '&手机号='+手机号+\
                '&姓名='+姓名+\
                '&身份证号码='+身份证号码)

def 提交办事申请(request):
    try:
        myState = str(request.GET['myState'])
        myState_json = json.loads(myState)
        access_token = myState_json['access_token']
        refresh_token = myState_json['refresh_token']
        qset0 = models.铁塔用户表.objects(refresh_token=refresh_token).first()
        if qset0 == None:
            response = HttpResponse('用户不存在')
        else:
            qset1 = models.铁塔资料表.objects(openid=qset0.openid).first()
            if qset1 == None:
                models.铁塔资料表(
                    openid = qset0.openid,
                    手机号 =  qset0.手机号,
                    资料 = myState_json
                ).save()
            else:
                qset1.update(资料 = myState_json)
            response = HttpResponse('成功')
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
                r = models.铁塔验证码表(验证码=验证码, 手机号=手机号).save()
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
        qset0 = models.铁塔用户表.objects(access_token=access_token).first()
        if qset0 == None:
            response = HttpResponse('用户未注册')
        else:
            姓名 = myState_json['姓名']
            验证码 = myState_json['验证码']
            手机号 = myState_json['手机号']
            身份证号码 = myState_json['身份证号码']
            qset1 = models.铁塔验证码表.objects(验证码=验证码,手机号=手机号).first()
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
