import datetime
import json
import traceback
import uuid

import pytz
import requests
import time
from django.http import HttpResponse

from myConfig import appid, secret, grant_type, sign_name, template_code, django_root_path
from mysite.demo_sms_send import send_sms
from mysite.yi_cha_mongo import 易查试卷结果表, 易查试卷模版表, 考试已结束, 考试进行中, 考试未开始, 易查主界面表, 易查试卷答案表, 易查验证码表, 易查用户表, 易查登录状态表, \
    易查政策宣传主界面, 易查套餐内容
import sys

#输出日志
# class Logger(object):
#     def __init__(self, fileN="Default.log"):
#         self.terminal = sys.stdout
#         self.log = open(fileN, "a")
#     def write(self, message):
#         self.terminal.write(message)
#         self.log.write(message)
#     def flush(self):
#         pass
# sys.stdout = Logger(根目录+'/'+'out.txt')  # 保存到D盘



def 登录检查(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = { 'appid':appid ,'secret':secret ,'js_code':js_code , 'grant_type':grant_type }
        r = requests.get(url=url , params=payload)
        r_json = json.loads(r.text)
        查询结果 = 易查用户表.objects(openid = r_json['openid']).first()
        if 查询结果 == None :
            自定义登录状态 = "{\"描述\":\"用户不存在\",\"会话\":\"\"}"
            # 自定义登录状态 = {"描述":"用户不存在","会话":""}
            return HttpResponse(自定义登录状态)
        else:
            r = 易查登录状态表(session_key=r_json['session_key'], openid=r_json['openid']).save()
            自定义登录状态 = "{\"描述\":\"验证通过\",\"会话\":\"" + str(r.id) + "\"}"
            # 自定义登录状态 = {"描述":"用户存在" ,"会话":r.id}
            return HttpResponse(自定义登录状态)
    except :
        print(traceback.format_exc())
        return HttpResponse('500')


def 交卷(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': appid, 'secret': secret, 'js_code': js_code, 'grant_type': grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户表_one = 易查用户表.objects(openid=r_json['openid']).first()
        if 用户表_one == None:
            自定义登录状态 = "{\"描述\":\"用户不存在\",\"会话\":\"\"}"
            return HttpResponse(自定义登录状态)
        else:
            考试大类 = request.GET['kao_shi_da_lei']
            考试小类 = request.GET['kao_shi_xiao_lei']
            考试结果 = json.loads( request.GET['radioItems_list'] )
            交卷时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            考生试卷表_one = 易查试卷结果表.objects(手机号=用户表_one.手机号, 考试大类=考试大类, 考试小类=考试小类).first()
            if 考生试卷表_one == None:
                试卷模版表_one = 易查试卷模版表.objects(子菜单page_name=考试大类,子菜单page_desc=考试小类).first()
                当前时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                考试开始时间 = 试卷模版表_one.考试开始时间
                考试结束时间 = 试卷模版表_one.考试结束时间
                if 试卷模版表_one == None:
                    自定义登录状态 = "{\"描述\":\"没有考试\",\"会话\":\"" + r_json['session_key'] + "\"}"
                    return HttpResponse(自定义登录状态)
                else:
                    if 当前时间 <= 考试结束时间 and  当前时间 >= 考试开始时间:
                        正确题数 = 0
                        试卷答案表_one = 易查试卷答案表.objects(考试大类=考试大类, 考试小类=考试小类).first()
                        for 选项组 in 考试结果:
                            radioItems = 选项组['radioItems']
                            for 选项 in radioItems:
                                if 'checked' in 选项:
                                    if 选项['checked']:
                                        for 正确答案序号 in 试卷答案表_one.考试答案:
                                            if 选项['value'] == 正确答案序号:
                                                正确题数 = 正确题数 + 1
                        考生试卷表_save=易查试卷结果表(手机号 = 用户表_one.手机号, 考试大类=考试大类, 考试小类=考试小类, 考试结果=考试结果
                                           , 正确题数=正确题数, 交卷时间=交卷时间).save()
                        题目总数 = 0
                        正确题数 = 0
                        if 考生试卷表_save == None:
                            pass
                        else:
                            正确题数 = 考生试卷表_save.正确题数
                            题目总数 = len(考生试卷表_save.考试结果)
                        描述 = '交卷成功'
                        自定义登录状态 = {'描述': 描述, '会话':  r_json['session_key'], '考试大类': 考试大类, '考试小类': 考试小类
                            , '考试开始时间': 考试开始时间, '考试结束时间': 考试结束时间, '正确题数': 正确题数, '题目总数': 题目总数}
                        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                        自定义登录状态 = str(自定义登录状态)
                        试卷模版表_one.update(考试结束时间=当前时间)
                        return HttpResponse(自定义登录状态)
                    elif 当前时间 > 考试结束时间:
                        题目总数 = 0
                        正确题数 = 0
                        描述 = '考试已结束'
                        自定义登录状态 = {'描述': 描述, '会话': r_json['session_key'], '考试大类': 考试大类, '考试小类': 考试小类
                            , '考试开始时间': 考试开始时间, '考试结束时间': 考试结束时间, '正确题数': 正确题数, '题目总数': 题目总数}
                        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                        自定义登录状态 = str(自定义登录状态)
                        return HttpResponse(自定义登录状态)
                    else:
                        自定义登录状态 = "{\"描述\":\""+考试未开始+"\",\"会话\":\"" + r_json['session_key'] + "\"}"
                        return HttpResponse(自定义登录状态)
            else:
                题目总数 = 0
                正确题数 = 0
                if 考生试卷表_one == None:
                    pass
                else:
                    正确题数 = 考生试卷表_one.正确题数
                    题目总数 = len(考生试卷表_one.考试结果)
                描述 = '不能重复交卷'
                自定义登录状态 = {'描述': 描述, '会话': r_json['session_key'], '考试大类': 考试大类, '考试小类': 考试小类
                    , '考试开始时间': '', '考试结束时间': 考生试卷表_one.交卷时间, '正确题数': 正确题数, '题目总数': 题目总数}
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')

def 下载试卷(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': appid, 'secret': secret, 'js_code': js_code, 'grant_type': grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        kao_shi_da_lei = request.GET['kao_shi_da_lei']
        kao_shi_xiao_lei = request.GET['kao_shi_xiao_lei']
        用户 = 易查用户表.objects(openid=r_json['openid']).first()
        手机号 = 用户.手机号
        易查主界面表_first = 易查主界面表.objects(手机号=手机号).first()
        试卷 = 易查试卷模版表.objects(子菜单page_name=kao_shi_da_lei, 子菜单page_desc=kao_shi_xiao_lei).first()
        if 试卷 == None:
            自定义登录状态 = "{\"描述\":\"没有考试\",\"会话\":\"" + r_json['session_key'] + "\"}"
            return HttpResponse(自定义登录状态)
        else:
            当前时间 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            考试开始时间 = 试卷.考试开始时间
            考试结束时间 = 试卷.考试结束时间
            考试大类 = 试卷.子菜单page_name
            考试小类 = 试卷.子菜单page_desc
            考试状态 = 试卷.考试状态
            考试时长 = 试卷.考试时长
            会话 = r_json['session_key']
            if 当前时间 > 考试结束时间:
                试卷.update(考试状态=考试已结束)
                描述 = 考试已结束
                题目总数 = 0
                正确题数 = 0
                考生试卷表_one = 易查试卷结果表.objects(手机号 = 用户.手机号, 考试大类=kao_shi_da_lei, 考试小类=kao_shi_xiao_lei).first()
                if 考生试卷表_one == None:
                    pass
                else:
                    正确题数 = 考生试卷表_one.正确题数
                    题目总数 = len(考生试卷表_one.考试结果)
                自定义登录状态 = {'描述': 描述, '会话': 会话, '考试大类': 考试大类, '考试小类': 考试小类
                    , '考试开始时间': 考试开始时间, '考试结束时间': 考试结束时间,'正确题数':正确题数,'题目总数':题目总数}
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
            elif 当前时间 <= 考试结束时间 and  当前时间 >= 考试开始时间 :
                if 考试状态 == 考试进行中:
                    试卷内容 = 试卷.试卷内容
                    描述 = '下载成功'
                    题目总数 = len(试卷内容)
                    正确题数 = '-'
                    自定义登录状态 = {'描述': 描述, '会话': 会话, '考试大类': 考试大类, '考试小类': 考试小类
                        , '试卷内容': 试卷内容, '考试开始时间': 考试开始时间, '考试结束时间': 考试结束时间
                        , '考试时长': 考试时长,'题目总数':题目总数,'正确题数':正确题数}
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                else:
                    交卷截止时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+考试时长 ))
                    考试结束时间 = 交卷截止时间
                    试卷.update(考试结束时间=考试结束时间)
                    试卷.update(考试状态=考试进行中)
                    试卷内容 = 试卷.试卷内容
                    描述 = '下载成功'
                    题目总数 = len(试卷内容)
                    正确题数 = '-'
                    自定义登录状态 = {'描述':描述 ,'会话':会话 ,'考试大类':考试大类 ,'考试小类':考试小类
                        ,'试卷内容':试卷内容,'考试开始时间':考试开始时间,'考试结束时间':考试结束时间
                        ,'考试时长':考试时长,'题目总数':题目总数,'正确题数':正确题数 }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str( 自定义登录状态 )
                    return HttpResponse(自定义登录状态)
            else:
                试卷.update(考试状态=考试未开始)
                描述 = 考试未开始
                自定义登录状态 = {'描述': 描述, '会话': 会话, '考试大类': 考试大类, '考试小类': 考试小类
                    , '考试开始时间': 考试开始时间, '考试结束时间': 考试结束时间}
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')

def utc_to_local(utc_time_str, utc_format='%Y-%m-%d %H:%M:%S'):
    local_tz = pytz.timezone('Asia/Beijing')
    local_format = "%Y-%m-%d %H:%M:%S"
    utc_dt = datetime.datetime.strptime(utc_time_str, utc_format)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    time_str = local_dt.strftime(local_format)
    return time_str

def 下载主界面数据(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': appid, 'secret': secret, 'js_code': js_code, 'grant_type': grant_type}
        r = requests.get(url=url, params=payload)
        print(r.text)
        r_json = json.loads(r.text)
        用户 = 易查用户表.objects(openid=r_json['openid']).first()
        # open_id = 'oPngn4yfqDljEh7wvTMD0NHddOOQ'
        # 用户 = 用户表.objects(openid=open_id).first()
        主界面 = 易查主界面表.objects(手机号 = 用户.手机号).first()
        if 主界面 == None:
            自定义登录状态 = "{\"描述\":\"没有数据\",\"会话\":\"" + r_json['session_key'] + "\"}"
            return HttpResponse(自定义登录状态)
        else:
            自定义登录状态 = 主界面.to_json().encode('utf-8').decode('unicode_escape')
            return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')

def 发送验证码(request):
    try:
        手机号 = str( request.GET['phone'] )
        if 手机号 == '' :
            return HttpResponse("手机号为空")
        else:
            import random
            j = 6
            验证码 = ''.join(str(i) for i in random.sample(range(0, 9), j))  # sample(seq, n) 从序列seq中选择n个随机且独立的元素；
            __business_id = uuid.uuid1()
            params = "{\"code\":\""+验证码+"\"}"
            r = send_sms(__business_id, 手机号, sign_name, template_code, params)
            r2 = json.loads(r)
            if r2['Code'] == 'OK' :
                r = 易查验证码表(验证码=验证码, 手机号 = 手机号).save()
            return HttpResponse(r2['Code'])
    except :
        return HttpResponse('500')


def 校验验证码(request):
    手机号 = str(request.GET['phone'])
    验证码 = str(request.GET['sms_code'])
    js_code = request.GET['code']
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    payload = {'appid': appid, 'secret': secret, 'js_code': js_code, 'grant_type': grant_type}
    r = requests.get(url=url, params=payload)
    r_json = json.loads(r.text)
    openid = r_json['openid']
    r = 易查验证码表.objects(手机号=手机号)
    for rr in r:
        if rr.验证码 == 验证码:
            易查用户表(手机号=手机号, openid=openid).save()
            return HttpResponse('绑定成功')
    return HttpResponse('绑定失败')


def 下载政策宣传主界面数据(request):
    try:
        js_code = request.GET['code']
        page_name = request.GET['page_name']
        page_desc = request.GET['page_desc']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': appid, 'secret': secret, 'js_code': js_code, 'grant_type': grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 易查用户表.objects(openid=r_json['openid']).first()
        易查政策宣传主界面first = 易查政策宣传主界面.objects(
            page_name=page_name,
            page_desc=page_desc
        ).first()
        if 易查政策宣传主界面first == None:
            主界内容 = []
            if page_desc == '融合套餐':
                主界内容 = [
                    {
                        'id': 'form',
                        'name': page_desc,
                        'open': False,
                        'pages': [
                            {
                                'url': 'toast',
                                'page_name': page_desc,
                                'page_desc': '融合109'
                            },
                            {
                                'url': 'toast',
                                'page_name': page_desc,
                                'page_desc': '融合139'
                            },
                            {
                                'url': 'toast',
                                'page_name': page_desc,
                                'page_desc': '融合199'
                            },
                            {
                                'url': 'toast',
                                'page_name': page_desc,
                                'page_desc': '大流量59'
                            },
                        ]
                    },

                ]
            if  page_desc == '单品套餐':
                主界内容 = [
                    {
                        'id': 'form',
                        'name': page_desc,
                        'open': False,
                        'pages': [
                            {
                                'url': 'toast',
                                'page_name': page_desc,
                                'page_desc': '宽+iTV'
                            },
                            {
                                'url': 'toast',
                                'page_name': page_desc,
                                'page_desc': '基础爽卡'
                            },
                            {
                                'url': 'toast',
                                'page_name': page_desc,
                                'page_desc': '步步高19'
                            },
                            {
                                'url': 'toast',
                                'page_name': page_desc,
                                'page_desc': '抖音卡49'
                            },
                            {
                                'url': 'toast',
                                'page_name': page_desc,
                                'page_desc': '大流量59'
                            },
                            {
                                'url': 'toast',
                                'page_name': page_desc,
                                'page_desc': '大流量79'
                            },
                            {
                                'url': 'toast',
                                'page_name': page_desc,
                                'page_desc': '畅享99'
                            },
                        ]
                    },
                ]
            主界面表_save = 易查政策宣传主界面(
                主界内容=主界内容,
                page_name=page_name,
                page_desc=page_desc
            ).save()
            自定义登录状态 = 主界面表_save.to_json().encode('utf-8').decode('unicode_escape')
            return HttpResponse(自定义登录状态)
        else:
            自定义登录状态 = 易查政策宣传主界面first.to_json().encode('utf-8').decode('unicode_escape')
            return HttpResponse(自定义登录状态)

    except:
        print(traceback.format_exc())
        return HttpResponse('500')


def 下载toast数据(request):
    try:
        js_code = request.GET['code']
        page_name = request.GET['page_name']
        page_desc = request.GET['page_desc']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': appid, 'secret': secret, 'js_code': js_code, 'grant_type': grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 易查用户表.objects(openid=r_json['openid']).first()
        易查政策宣传主界面first = 易查套餐内容.objects(
            page_name=page_name,
            page_desc=page_desc
        ).first()
        if 易查政策宣传主界面first == None:
            toast_data = ''
            if page_desc == '融合109':
                toast_data = '资费109元，内容：300分钟，20G流量降速，3张移动（1主2副，副卡0元），首部宽带（100M）和iTV免费加装，网关和机顶盒免费租用。第二部宽带（50M）480元/年，无优惠，办宽带赠送iTV,终端网关59元连接费租用，机顶盒自购。月付型10元智能组网，赠送千兆路由器。'
            if page_desc == '融合139':
                toast_data = '资费139元，内容：500分钟，20G+10G（待配置）流量降速，4张移动（1主3副，第三张副卡10元），首部宽带（200M）和iTV免费加装，网关和机顶盒免费租用。第二部宽带（50M）480元/年，优惠20元/月（协议期24个月），办宽带赠送iTV,终端网关59元连接费租用，机顶盒自购。月付型10元智能组网，赠送千兆路由器。加载橙分期，结算价585元。'
            if page_desc == '融合199':
                toast_data = '资费199元，内容：1000分钟，40G流量降速，5张移动（1主4副，副卡0元），首部宽带（300M）和iTV免费加装，网关和机顶盒免费租用。第二部宽带（50M）480元/年，优惠40元/月（协议期24个月），办宽带赠送iTV,终端网关59元连接费租用，机顶盒自购。0元智能组网，赠送千兆路由器。加载橙分期，结算价585元（改签）和780元（维系）'
            if page_desc == '大流量59':
                toast_data = '资费59元，200分钟，5G流量，50M宽带，ITV可选项。网关免费、机顶盒自购返还。（竞品，不针对单个用户开放、只针对活动洼地开放）'
            if page_desc == '宽+iTV':
                toast_data = '资费1680元，宽带（20M）1200元两年+iTV尊享两年，网关连接费59元，机顶盒免费。'
            if page_desc == '基础爽卡':
                toast_data = '资费5元，流量1元1G，2元/天封顶；100国内语音，超出0.1元/分钟；国内短/彩信：0.1元/条；不可办理副卡'
            if page_desc == '步步高19':
                toast_data = '资费19元，流量2G，100分钟语音，超出0.03元/M,语音0.15元/分钟；国内短/彩信：0.1元/条；不可办理副卡用户订购套餐生效满一年后，每月赠送1G全国通用流量,之后用户每增加一年，每月再叠加赠送一个1G全国通用流量，赠送至3G的全国通用流量封顶'
            if page_desc == '抖音卡49':
                toast_data = '''资费49元，流量30G；200分钟国内语音，超出0.1元分钟；不可办理副卡；国内短/彩信：0.1元/条 '''
            if page_desc == '大流量59':
                toast_data = ''' 资费59元，流量5G，200分钟国内语音，超出0.03元/M,语音0.15元/分钟；国内短/彩信：0.1元/条；可办理1张0元副卡'''
            if page_desc == '大流量79':
                toast_data = '''资费79元，流量10G，200分钟国内语音，超出0.03元/M,语音0.15元/分钟；国内短/彩信：0.1元/条；可办理1张0元副卡，加载橙分期，结算价585元 '''
            if page_desc == '畅享99':
                toast_data = '''资费99元：流量20G，300分钟国内语音，超出语音0.15元/分钟；国内短/彩信：0.1元/条；可办理2张0元副卡，加载橙分期，结算价975元 '''
            if page_desc == '':
                toast_data = ''' '''

            主界面表_save = 易查套餐内容(
                toast_data=toast_data,
                page_name=page_name,
                page_desc=page_desc
            ).save()
            自定义登录状态 = 主界面表_save.to_json().encode('utf-8').decode('unicode_escape')
            return HttpResponse(自定义登录状态)
        else:
            自定义登录状态 = 易查政策宣传主界面first.to_json().encode('utf-8').decode('unicode_escape')
            return HttpResponse(自定义登录状态)

    except:
        print(traceback.format_exc())
        return HttpResponse('500')