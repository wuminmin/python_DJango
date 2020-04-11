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

def my_token_login(request):
    import json
    import requests
    import myConfig
    import traceback
    from . import models
    try:
        token = request.GET['token']
        wx_user25 = models.wx_user.objects(__raw__ = {
                'd.token':token
        }).first()
        if wx_user25 == None:
            code = 2
            data = {}
            message = '已超时，请重新登录'
            res = {'status': code, 'data': data, 'msg': message}
            return myHttpResponse(res)
        else:
            return (True,wx_user25)
    except:
        print(traceback.format_exc())
        code = 0
        data = {}
        message = '系统异常'
        res = {'status': code, 'data': data, 'msg': message}
        return myHttpResponse(res)

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
            data = {'main_id': 1,'token':'','mobile':'','nickname':'','portrait':''}
            message = '未注册'
            res = {'status': code, 'data': data, 'msg': message}
            return myHttpResponse(res)
        else:
            from . import tool
            tokenprogramer = tool.Token(
                api_secret = res['app_id'], #微信appid
                project_code = 'canteen_alliance', #项目名称
                account =  wx_user97.d['mobile'] #用户名
            )
            token = tokenprogramer.get_token()
            userInfo = wx_user97.d
            userInfo['main_id'] = wx_user97.d['main_id']
            userInfo['token'] = token
            userInfo['mobile'] = wx_user97.d['mobile']
            userInfo['nickname'] = wx_user97.d['nickname']
            userInfo['portrait'] = wx_user97.d['portrait']
            wx_organization_match_main_id101 = models.wx_organization_match_main_id.objects(__raw__ = {
                'd.main_id':wx_user97.d['main_id']
            })
            if len(list(wx_organization_match_main_id101)) == 0:
                organizationInfo = {'hasOrganization':False,'organizationInfoList':[]}
            else:
                organizationInfoList = wx_organization_match_main_id101.to_json().encode('utf-8').decode('unicode_escape')
                organizationInfoList = json.loads(organizationInfoList)
                organizationInfo = {'hasOrganization':True,'organizationInfoList':organizationInfoList}
            data = {'userInfo':userInfo,'organizationInfo':organizationInfo}
            userInfo['session_key'] = session_key
            wx_user97.update(d=userInfo)
            code = 1
            message = '登录成功'
            res = {'status': code, 'data': data, 'msg': message}
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
        app_id = res['app_id']
        session_key = res['session_key']
        sendData = request.GET['sendData']
        sendData_json = json.loads(sendData)
        nickname = sendData_json['nickname']
        mobile = sendData_json['mobile']
        password = sendData_json['password']
        wx_sms87 = models.wx_sms.objects(__raw__ = {
            'd.mobile':mobile,'d.password':password
        }).first()
        if wx_sms87 == None:
            code = 2
            data = {'main_id': '1','token':'','mobile':mobile,'nickname':'','portrait':''}
            message = '验证码不正确'
            res = {'status': code, 'data': data, 'msg': message}
            return myHttpResponse(res)
        else:
            from . import tool
            tokenprogramer = tool.Token(
                api_secret = res['app_id'], #微信appid
                project_code = 'canteen_alliance', #项目名称
                account = mobile #用户名
            )
            token = tokenprogramer.get_token()
            portrait = 'https://dss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=1676131907,2302520392&fm=111&gp=0.jpg'
            wx_user97 = models.wx_user.objects(__raw__ = {
                'd.openid':openid
            }).first()
            if wx_user97 == None:
                d =  {
                    'openid':openid,
                    'app_id':app_id,
                    'session_key':session_key,
                    'token':token,
                    'mobile':mobile,
                    'nickname':nickname,
                    'portrait':portrait,
                }
                models.wx_user(d=d).save()
                wx_user163 = models.wx_user.objects(__raw__ = {
                    'd.openid':openid
                }).first()
                d = wx_user163.d
                d['main_id'] = str(wx_user163.id)
                wx_user163.update(d=d)
            else:
                d = wx_user97.d
                d['token'] = token
                d['app_id'] = app_id
                d['session_key'] = session_key
                d['mobile'] = mobile
                d['nickname'] = nickname
                d['portrait'] = portrait
                wx_user97.update(d=d)
            code = 1
            data = {'main_id': 1,'token':token,'mobile':mobile,'nickname':nickname,'portrait':portrait}
            message = '注册成功'
            res = {'status': code, 'data': data, 'msg': message}
            return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        code = 0
        data = {'main_id': 0,'token':'','mobile':'','nickname':'','portrait':''}
        message = '系统异常'
        res = {'status': code, 'data': data, 'msg': message}
        return myHttpResponse(res)

def wx_send_sms(request): #wx发短信
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
        wx_user166 = models.wx_user.objects(__raw__ = {
                'd.openid':openid
            }).first()
        if wx_user166 == None:
            pass
        else:
            code = 4
            data = {}
            message = '不可以重复注册'
            res = {'status': code, 'data': data, 'msg': message}
            return myHttpResponse(res)
        sendData = request.GET['sendData']
        sendData_json = json.loads(sendData)
        mobile = sendData_json['mobile']
        if mobile == '':
            code = 2
            data = {}
            message = '手机号为空'
            res = {'status': code, 'data': data, 'msg': message}
            return myHttpResponse(res)
        else:
            import random
            import uuid
            import myConfig
            from . import tool
            j = 6
            sms_code = ''.join(str(i) for i in random.sample(range(0, 9), j))  # sample(seq, n) 从序列seq中选择n个随机且独立的元素；
            __business_id = uuid.uuid1()
            params = "{\"code\":\"" + sms_code + "\"}"
            r = tool.send_sms(__business_id, mobile, myConfig.sign_name, myConfig.template_code, params)
            print(r,'---------------阿里云短信网关')
            r2 = json.loads(r)
            if r2['Code'] == 'OK':
                wx_sms165 = models.wx_sms.objects(__raw__ = {'d.mobile':mobile}).first()
                if wx_sms165 == None:
                    d = {'mobile':mobile, 'password':sms_code}
                    models.wx_sms(d=d).save()
                else:
                    d = {'mobile':mobile, 'password':sms_code}
                    wx_sms165.update(d=d)
                code = 1
                data = {}
                message = r2['Code']
                res = {'status': code, 'data': data, 'msg': message}
                return myHttpResponse(res)
            code = 3
            data = {}
            message = r2['Code']
            res = {'status': code, 'data': data, 'msg': message}
            return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        code = 0
        data = {}
        message = '系统异常'
        res = {'status': code, 'data': data, 'msg': message}
        return myHttpResponse(res)

def wx_search_organization(request):
    import json
    import traceback
    import time
    from . import models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        if my_token_login(request)[0]:
            sendData = request.GET['sendData']
            sendData_json = json.loads(sendData)
            searchVal = sendData_json['searchVal']
            wx_organization249 = models.wx_organization.objects(__raw__ = {'$or':[
                    {
                        'd.organization_name':{
                            '$regex':".*"+searchVal+".*"
                        }
                    },
                    {
                        'd.certificate_for_uniform_social_credit_code':{
                             '$regex':".*"+searchVal+".*"
                            # '$regex':'/^([0-9A-HJ-NPQRTUWXY]{2}\d{6}[0-9A-HJ-NPQRTUWXY]{10}|[1-9]\d{14})$/'
                        }
                    }
                ]
            })
            organization_list = wx_organization249.to_json().encode('utf-8').decode('unicode_escape')
            code = 1
            data = {'organization_list':json.loads(organization_list)}
            message = ''
            res = {'status': code, 'data': data, 'msg': message}
            return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        code = 0
        data = {}
        message = '系统异常'
        res = {'status': code, 'data': data, 'msg': message}
        return myHttpResponse(res)

def wx_joinDepartment(request):
    import json
    import traceback
    import time
    from . import models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        if my_token_login(request)[0]:
            sendData = request.GET['sendData']
            sendData_json = json.loads(sendData)
            certificate_for_uniform_social_credit_code = sendData_json['certificate_for_uniform_social_credit_code']
            name = sendData_json['name']
            department = sendData_json['department']
            labor_contract = sendData_json['labor_contract']
            wx_join_organization_apply311 = models.wx_join_organization_apply.objects(__raw__ ={
                'd.certificate_for_uniform_social_credit_code':certificate_for_uniform_social_credit_code,
                'd.main_id':my_token_login(request)[1].d['main_id']
            }).first()
            import datetime
            if wx_join_organization_apply311 == None:
                d = {
                    'certificate_for_uniform_social_credit_code':certificate_for_uniform_social_credit_code,
                    'main_id':my_token_login(request)[1].d['main_id'],
                    'name':name,
                    'department':department,
                    'labor_contract':labor_contract,
                    'apply_time':datetime.datetime.now(),
                    'is_accept':False,
                    'approval_person_main_id':'',
                    'approval_time':'',
                }
                models.wx_join_organization_apply(d=d).save()
                code = 1
                data = {}
                message = '已收到申请'
                res = {'status': code, 'data': data, 'msg': message}
                return myHttpResponse(res)
            else:
                d = wx_join_organization_apply311.d
                d['name'] = name
                d['department'] = department
                d['labor_contract'] = labor_contract
                d['apply_time'] = datetime.datetime.now()
                d['is_accept'] = False
                d['approval_person_main_id'] = ''
                d['approval_time'] = ''
                wx_join_organization_apply311.update(d=d)
                code = 1
                data = {}
                message = '已更新申请'
                res = {'status': code, 'data': data, 'msg': message}
                return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        code = 0
        data = {}
        message = '系统异常'
        res = {'status': code, 'data': data, 'msg': message}
        return myHttpResponse(res)

def wx_createDepartment(request):
    import json
    import traceback
    import time
    from . import models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        if my_token_login(request)[0]:
            sendData = request.GET['sendData']
            sendData_json = json.loads(sendData)
            certificate_for_uniform_social_credit_code = sendData_json['certificate_for_uniform_social_credit_code']
            organization_name = sendData_json['organization_name']
            organization_address = sendData_json['organization_address']
            legal_person_name = sendData_json['legal_person_name']
            legal_person_mobile = sendData_json['legal_person_mobile']
            manage_person_name = sendData_json['manage_person_name']
            manage_person_mobile = sendData_json['manage_person_mobile']
            wx_organization373 = models.wx_organization.objects(__raw__ ={
                'd.certificate_for_uniform_social_credit_code':certificate_for_uniform_social_credit_code
            }).first()
            import datetime
            if wx_organization373 == None:
                d = {
                    'certificate_for_uniform_social_credit_code':certificate_for_uniform_social_credit_code,
                    'organization_name':organization_name,
                    'organization_address':organization_address,
                    'super_admin_person':{
                        'main_id':my_token_login(request)[1].d['main_id'],
                        'name':'',
                        'moile':'',
                    },
                    'legal_person':{
                        'name':legal_person_name,
                        'mobile':legal_person_mobile
                    },
                    'manage_person':{
                        'name':manage_person_name,
                        'mobile':manage_person_mobile
                    },
                    'department':[
                        {'name':'管理员'},{'name':'管控部门'},{'name':'销售部门'},{'name':'生产部门'}
                    ],
                    'labor_contract':[
                        {'name':'合同制'},{'name':'派遣制'},{'name':'第三方'},{'name':'实习生'},{'name':'其它'}
                    ],
                    'create_time':datetime.datetime.now(),
                    'create_person_main_id':my_token_login(request)[1].d['main_id'],
                }
                models.wx_organization(d=d).save()
                wx_organization_match_main_id405 = models.wx_organization_match_main_id.objects(__raw__ = {
                    'd.certificate_for_uniform_social_credit_code':certificate_for_uniform_social_credit_code,
                    'd.main_id':my_token_login(request)[1].d['main_id'],
                }).first()
                if wx_organization_match_main_id405 == None:
                    d = {
                        'certificate_for_uniform_social_credit_code':certificate_for_uniform_social_credit_code,
                        'organization_name':organization_name,
                        'organization_address':organization_address,
                        'main_id':my_token_login(request)[1].d['main_id'],
                        'role':['super_admin'],
                        'department':'管理员',
                        'labor_contract':'合同制',
                    }
                    models.wx_organization_match_main_id(d=d).save()
                else:
                    d = wx_organization_match_main_id405.d
                    wx_organization_match_main_id405.update(d=d)
                code = 1
                data = {}
                message = '创建成功'
                res = {'status': code, 'data': data, 'msg': message}
                return myHttpResponse(res)
            else:
                code = 2
                data = {}
                message = '组织已存在！'
                res = {'status': code, 'data': data, 'msg': message}
                return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        code = 0
        data = {}
        message = '系统异常'
        res = {'status': code, 'data': data, 'msg': message}
        return myHttpResponse(res)




















