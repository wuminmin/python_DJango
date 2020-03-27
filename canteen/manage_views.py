
def myHttpResponse(res):#合并跨域配置
    import json
    from django.http import HttpResponse, FileResponse
    response = HttpResponse(json.dumps(res))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def login(request):#vue管理后台登录
    import json
    import traceback
    from . import manage_models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse 
    try:
        req_body = request.body.decode('utf-8')
        req_json = json.loads(req_body)
        username = req_json['username']
        password = req_json['password']
        print(username,password)
        q1 = manage_models.MyUsers.objects(__raw__ = {'username':username,'password':password}).first()
        if q1 == None:
            code = 60204
            data = {'token': ''}
            message = '账号或者密码错误'
            res = {'code':code,'data':data,'message':message} 
        else:
            code = 20000
            data = {'token': 'admin-token'}
            message = '登录成功'
            res = {'code':code,'data':data,'message':message} 
        return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        res = {'code':500,'data':{},'message':'系统故障'} 
        return myHttpResponse(res)