def deprecated_async(f): # 异步函数
    def wrapper(*args, **kwargs):
        from threading import Thread
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

def myHttpResponse(res):  # 合并跨域配置
    import json
    from django.http import HttpResponse, FileResponse
    response = HttpResponse(json.dumps(res))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def wx_login_get_openid(request): #解析openid
    import json
    import requests
    import myConfig
    import traceback
    try:
        js_code = request.GET['code']
        app_id = request.GET['app_id']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': app_id, 'secret': myConfig.appid_secret_dict[app_id], 'js_code': js_code,
                    'grant_type': 'authorization_code'}
        r = requests.get(url=url, params=payload)
        print(r.text,'------------wx_login_get_openid')
        r_json = json.loads(r.text)
        openid = r_json['openid']
        session_key = r_json['session_key']
        return {'openid':openid,'session_key':session_key,'app_id':app_id}
    except:
        print(traceback.format_exc())
        return None

def wx_login(request):  # vue管理后台登录
    import json
    import traceback
    import time
    from . import models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        res = wx_login_get_openid(request)
        print(res)
        openid = res['openid']
        session_key = res['session_key']
        wx_user97 = models.wx_user.objects(__raw__ = {
            'd.openid':openid
        }).first()
        if wx_user97 == None:
            code = 2
            data = {'id': 1,'mobile':'','nickname':'','portrait':''}
            message = '未注册'
            res = {'status': code, 'data': data, 'msg': message}
            return myHttpResponse(res)
        else:
            d = wx_user97.d
            d['id'] = str(wx_user97.id)
            d['mobile'] = wx_user97.d['mobile']
            d['nickname'] = wx_user97.d['nickname']
            d['portrait'] = wx_user97.d['portrait']
            code = 1
            message = '登录成功'
            res = {'status': code, 'data': d, 'msg': message}
            return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        res = {'code': 500, 'data': {}, 'message': '系统故障'}
        return myHttpResponse(res)

def wx_register(request):  #wx注册
    import json
    import traceback
    import time
    from . import models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        res = wx_login_get_openid(request)
        print(res)
        openid = res['openid']
        session_key = res['session_key']
        sendData = request.GET['sendData']
        sendData_json = json.loads(sendData)
        mobile = sendData_json['mobile']
        password = sendData_json['password']
        wx_sms87 = models.wx_sms.objects(__raw__ = {
            'd.mobile':mobile,'d.password':password
        }).first()
        if wx_sms87 == None:
            code = 2
            data = {'id': 1,'mobile':mobile,'nickname':'nickname','portrait':'https://dss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=3788695993,2392089703&fm=111&gp=0.jpg'}
            message = '验证码不正确'
            res = {'status': code, 'data': data, 'msg': message}
            return myHttpResponse(res)
        else:
            wx_user97 = models.wx_user.objects(__raw__ = {
                'd.openid':openid
            }).first()
            if wx_user97 == None:
                d =  {
                    'openid':openid,'mobile':mobile,'nickname':'','portrait':''
                }
                models.wx_user(d=d).save()
            else:
                nickname = ''
                portrait = ''
                d = wx_user97.d
                d['mobile'] = mobile
                d['nickname'] = nickname
                d['portrait'] = portrait
                wx_user97.update(d=d)
            code = 1
            data = {'id': 1,'mobile':mobile,'nickname':'nickname','portrait':'https://dss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=3788695993,2392089703&fm=111&gp=0.jpg'}
            message = '注册成功'
            res = {'status': code, 'data': data, 'msg': message}
            return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        code = 0
        data = {'id': 0,'mobile':'','nickname':'nickname'}
        message = '系统异常'
        res = {'status': code, 'data': data, 'msg': message}
        return myHttpResponse(res)

def info(request):  # vue后台获取用户信息
    import json
    import traceback
    from . import models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        token = request.GET['token']
        print(token)
        q1 = models.my_user.objects(__raw__ = {'d.token':token}).first()
        if q1 == None:
            code = 50008
            data = {}
            message = '已超时，请重新登录'
            res = {'code':code,'data':data,'message':message}
        else:
            code = 20000
            data = {
                'roles': ['admin'],
                'introduction': 'I am a super administrator',
                'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
                'name': 'Super Admin'
            }
            message = '登录成功'
            res = {'code': code, 'data': data, 'message': message}
        return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        res = {'code': 500, 'data': {}, 'message': '系统故障'}
        return myHttpResponse(res)
