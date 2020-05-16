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
from tou_piao import models

def images(request):
    try:
        id = request.GET['id']
        qset = models.tou_piao_image_col.objects(wxyl_id=id).first()
        print(qset)
        if qset == None:
            path = myConfig.django_root_path + '/' + 'mysite' + '/' + '404'
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
        path = myConfig.django_root_path + '/' + 'mysite' + '/' + '404'
        outfile = open(path, 'rb')
        response = FileResponse(outfile)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s"' % "image.jpg"
        return response

def dl(request):
    from . import models
    from urllib import parse
    myOtherUrl = parse.quote('https://wx.wuminmin.top/tou_piao/dl_2')
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
    qset0 = models.微信投票用户表.objects(openid=openid).first()
    if qset0 == None:
        models.微信投票用户表(
            openid=openid,
            access_token=access_token,
            refresh_token=refresh_token
        ).save()
        return redirect(models.react_url+'tou_piao'+'?access_token='+access_token+'&refresh_token='+refresh_token)
    else:
        qset0.update(
            access_token=access_token,
            refresh_token=refresh_token
        )
        if qset0.手机号 == '':
            return redirect(models.react_url+'tou_piao'+'?access_token='+access_token+'&refresh_token='+refresh_token)
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

def 提交办事申请(request):
    try:
        myState = str(request.GET['myState'])
        myState_json = json.loads(myState)
        access_token = myState_json['access_token']
        refresh_token = myState_json['refresh_token']
        qset0 = models.微信投票用户表.objects(refresh_token=refresh_token).first()
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
            # 上午办事区间 = ['9:00-10:00','10:00-11:00','11:00-12:00']
            # 下午办事区间 = ['14:00-15:00','15:00-16:00','16:00-17:30']
            当前日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            当前日期五天后 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 432000))
            当前小时 = time.strftime('%H:%M:%S', time.localtime(time.time()))
            print(当前日期,当前小时,办事日期)
            if 办事区间 == '':
                response = HttpResponse('未选择，请重新输入')
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"
                return response
            if '投票结果' in qset0.其它:
                qset1 = models.微信投票用户表.objects
                s1 = 0
                s2 = 0
                for one in qset1:
                    if '投票结果' in one.其它:
                        if one.其它['投票结果'] == '样式1':
                            s1 = s1+1
                        if one.其它['投票结果'] == '样式2':
                            s2 = s2+1
                response = HttpResponse('您已投了'+qset0.其它['投票结果']+';目前样式一：'+str(s1)+',样式二：'+str(s2)+'.')
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"
                return response
            if 办事区间 == '样式1':
                其它 = {'投票结果':'样式1'}
                qset0.update(其它=其它)
                response = HttpResponse('投票成功，样式1')
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"
                return response
            if 办事区间 == '样式2':
                其它 = {'投票结果':'样式2'}
                qset0.update(其它=其它)
                response = HttpResponse('投票成功,样式2')
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"
                return response
            response = HttpResponse('投票选项有误')
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
