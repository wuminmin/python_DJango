
def deprecated_async(f): # 异步函数
    def wrapper(*args, **kwargs):
        from threading import Thread
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

def myHttpResponse(res):  # 合并跨域配置
    import json
    from django.http import HttpResponse
    response = HttpResponse(json.dumps(res))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET"
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
        # if request.method == 'OPTIONS':
        #     return myHttpResponse({})
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
            from . import manage_token
            import myConfig
            tokenprogramer = manage_token.Token(
                api_secret = myConfig.wx_app_id, #微信appid
                project_code = 'canteen', #项目名称
                account = username #用户名
            )
            tmp_d['token'] = tokenprogramer.get_token()
            q1.update(d = tmp_d )
            code = 20000
            data = {'token': tokenprogramer.get_token()}
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
        if request.method == 'OPTIONS':
            return myHttpResponse({})
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
        if request.method == 'OPTIONS':
            return myHttpResponse({})
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

def base_table_fetchList(request):
    import json
    import traceback
    from . import manage_models
    from . import models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    from . import models as ding_can_mongo  #新版订餐后台
    import myConfig
    from . import tool
    try:
        if request.method == 'OPTIONS':
            return myHttpResponse({})
        code = 0
        method_dict = {'table_name':'teacher_base_info'}
        if request.method == 'GET':
            code = request.GET['code']
            method_dict = json.loads(request.GET['method_dict'])
        if request.method == 'POST':
            code = request.POST['code']
            method_dict = json.loads(request.POST['method_dict'])
        if code == 1 or code == '1': #查询筛选条件
            data = request.GET['data']
            message = request.GET['message']
            res = tool.get_my_basic_filter_list(data,method_dict)
        elif code == 2 or code == '2': #查询基本信息
            data = request.GET['data']
            message = request.GET['message']
            res = tool.get_my_basic_table_list(data,method_dict)
        elif code == 3 or code == '3': #新增一行基本信息数据
            data = request.GET['data']
            message = request.GET['message']
            res = tool.create_row(data,method_dict)
        elif code == 4 or code == '4': #删除一行基本信息数据
            data = request.GET['data']
            message = request.GET['message']
            res = tool.delete_row(data,method_dict) 
        elif code == 5 or code == '5': #修改一行基本信息数据
            data = request.GET['data']
            message = request.GET['message']
            res = tool.update_row(data,method_dict) 
        elif code == 6 or code == '6': 
            data = request.GET['data']
            message = request.GET['message']
            res = tool.import_excel_init(data,method_dict) 
        elif code == 7 or code == '7': 
            data = request.GET['data']
            message = request.GET['message']
            res = tool.import_excel_data(data,method_dict) 
        else:
            res = {'code': 0, 'data': {}, 'message': '参数错误'}
        return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        res = {'code': 500, 'data': {}, 'message': '系统故障'}
        return myHttpResponse(res)




























