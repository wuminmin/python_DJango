
def myHttpResponse(res):  # 合并跨域配置
    import json
    from django.http import HttpResponse, FileResponse
    response = HttpResponse(json.dumps(res))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def login(request):  # vue管理后台登录
    import json
    import traceback
    import time
    from . import manage_models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        req_body = request.body.decode('utf-8')
        req_json = json.loads(req_body)
        username = req_json['username']
        password = req_json['password']
        print(username, password)
        q1 = manage_models.my_user.objects(
            __raw__={'d.username': username, 'd.password': password}
        ).first()
        if q1 == None:
            code = 60204
            data = {'token': ''}
            message = '账号或者密码错误'
            res = {'code': code, 'data': data, 'message': message}
        else:
            tmp_d = q1.d
            now_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            tmp_d['token'] = now_time
            q1.update(d = tmp_d )
            code = 20000
            data = {'token': now_time}
            message = '登录成功'
            res = {'code': code, 'data': data, 'message': message}
        return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        res = {'code': 500, 'data': {}, 'message': '系统故障'}
        return myHttpResponse(res)


def info(request):  # vue后台获取用户信息
    import json
    import traceback
    from . import manage_models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        token = request.GET['token']
        print(token)
        q1 = manage_models.my_user.objects(__raw__ = {'d.token':token}).first()
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

def logout(request):
    import json
    import traceback
    from . import manage_models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        req_body = request.body.decode('utf-8')
        print(req_body)
        code = 20000
        data = 'success'
        message = '退出成功'
        res = {'code': code, 'data': data, 'message': message}
        return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        res = {'code': 500, 'data': {}, 'message': '系统故障'}
        return myHttpResponse(res)