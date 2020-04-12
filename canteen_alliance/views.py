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
            msg = '已超时，请重新登录'
            res = {'status': code, 'data': data, 'msg': msg}
            return myHttpResponse(res)
        else:
            wx_organization_match_main_id36 = models.wx_organization_match_main_id.objects(__raw__ = {
                'd.main_id' : wx_user25.d['main_id'],
                'd.certificate_for_uniform_social_credit_code':wx_user25.d['active_organization']
            }).first()
            super_admin = False
            normal_admin = False
            user = False
            if wx_organization_match_main_id36 == None:
                pass
            else:
                if 'super_admin' in  wx_organization_match_main_id36.d['role']:
                    super_admin = True
                elif 'normal_admin' in wx_organization_match_main_id36.d['role']:
                    nomarl_admin = True
                elif 'user' in wx_organization_match_main_id36.d['role']:
                    user = True
                else:
                    pass
            role_dict = {
                    'role_list':['super_admin','nomarl_admin','user'],
                    'main_id':wx_user25.d['main_id'],
                    'certificate_for_uniform_social_credit_code':wx_user25.d['active_organization'],
                    'super_admin':super_admin,
                    'normal_admin':normal_admin,
                    'user':user
            }
            return (True,wx_user25,role_dict)
    except:
        print(traceback.format_exc())
        code = 0
        data = {}
        msg = '系统异常'
        res = {'status': code, 'data': data, 'msg': msg}
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
            msg = '未注册'
            res = {'status': code, 'data': data, 'msg': msg}
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
            # wx_organization_match_main_id101 = models.wx_organization_match_main_id.objects(__raw__ = {
            #     'd.main_id':wx_user97.d['main_id']
            # })
            # if len(list(wx_organization_match_main_id101)) == 0:
            #     organizationInfo = {'hasOrganization':False,'organizationInfoList':[]}
            # else:
            #     organizationInfoList = wx_organization_match_main_id101.to_json().encode('utf-8').decode('unicode_escape')
            #     organizationInfoList = json.loads(organizationInfoList)
            #     organizationInfo = {'hasOrganization':True,'organizationInfoList':organizationInfoList}
            # data = {'userInfo':userInfo,'organizationInfo':organizationInfo}
            data = {'userInfo':userInfo}
            userInfo['session_key'] = session_key
            wx_user97.update(d=userInfo)
            code = 1
            msg = '登录成功'
            res = {'status': code, 'data': data, 'msg': msg}
            return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        res = {'code': 500, 'data': {}, 'msg': '系统故障'}
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
            msg = '验证码不正确'
            res = {'status': code, 'data': data, 'msg': msg}
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
                    'active_organization':'', #正在使用的组织统一代码
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
                d['token'] = token #更新token
                # d['app_id'] = app_id
                # d['session_key'] = session_key
                # d['mobile'] = mobile
                # d['nickname'] = nickname
                # d['portrait'] = portrait
                wx_user97.update(d=d)
            code = 1
            data = {'main_id': 1,'token':token,'mobile':mobile,'nickname':nickname,'portrait':portrait}
            msg = '注册成功'
            res = {'status': code, 'data': data, 'msg': msg}
            return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        code = 0
        data = {'main_id': 0,'token':'','mobile':'','nickname':'','portrait':''}
        msg = '系统异常'
        res = {'status': code, 'data': data, 'msg': msg}
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
            msg = '不可以重复注册'
            res = {'status': code, 'data': data, 'msg': msg}
            return myHttpResponse(res)
        sendData = request.GET['sendData']
        sendData_json = json.loads(sendData)
        mobile = sendData_json['mobile']
        if mobile == '':
            code = 2
            data = {}
            msg = '手机号为空'
            res = {'status': code, 'data': data, 'msg': msg}
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
                msg = r2['Code']
                res = {'status': code, 'data': data, 'msg': msg}
                return myHttpResponse(res)
            code = 3
            data = {}
            msg = r2['Code']
            res = {'status': code, 'data': data, 'msg': msg}
            return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        code = 0
        data = {}
        msg = '系统异常'
        res = {'status': code, 'data': data, 'msg': msg}
        return myHttpResponse(res)

def wx_search_organization(request):
    import json
    import traceback
    import time
    from . import models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        my_token_login_request = my_token_login(request)
        if my_token_login_request[0]:
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
            msg = ''
            res = {'status': code, 'data': data, 'msg': msg}
            return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        code = 0
        data = {}
        msg = '系统异常'
        res = {'status': code, 'data': data, 'msg': msg}
        return myHttpResponse(res)

def wx_joinDepartment(request):
    import json
    import traceback
    import time
    from . import models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        my_token_login_request = my_token_login(request)
        if my_token_login_request[0]:
            sendData = request.GET['sendData']
            sendData_json = json.loads(sendData)
            certificate_for_uniform_social_credit_code = sendData_json['certificate_for_uniform_social_credit_code']
            name = sendData_json['name']
            department = sendData_json['department']
            labor_contract = sendData_json['labor_contract']
            wx_join_organization_apply311 = models.wx_join_organization_apply.objects(__raw__ ={
                'd.certificate_for_uniform_social_credit_code':certificate_for_uniform_social_credit_code,
                'd.apply_person_main_id':my_token_login_request[1].d['main_id']
            }).first()
            import datetime
            if wx_join_organization_apply311 == None:
                d = {
                    'certificate_for_uniform_social_credit_code':certificate_for_uniform_social_credit_code,
                    'apply_person_main_id':my_token_login_request[1].d['main_id'],
                    'apply_person_name':name,
                    'apply_for_department':department,
                    'apply_for_labor_contract':labor_contract,
                    'apply_time':datetime.datetime.now(),
                    'apply_status':'todo',
                    'is_accept':False,
                    'approval_person_main_id':'',
                    'approval_time':'',
                }
                models.wx_join_organization_apply(d=d).save()
                code = 1
                data = {}
                msg = '已收到申请'
                res = {'status': code, 'data': data, 'msg': msg}
                return myHttpResponse(res)
            else:
                d = wx_join_organization_apply311.d
                d['apply_person_name'] = name
                d['apply_for_department'] = department
                d['apply_for_labor_contract'] = labor_contract
                d['apply_time'] = datetime.datetime.now()
                d['apply_status'] = 'todo',
                d['is_accept'] = False
                d['approval_person_main_id'] = ''
                d['approval_time'] = ''
                wx_join_organization_apply311.update(d=d)
                code = 1
                data = {}
                msg = '已更新申请'
                res = {'status': code, 'data': data, 'msg': msg}
                return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        code = 0
        data = {}
        msg = '系统异常'
        res = {'status': code, 'data': data, 'msg': msg}
        return myHttpResponse(res)

def wx_createDepartment(request):
    import json
    import traceback
    import time
    from . import models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        my_token_login_request = my_token_login(request)
        if my_token_login_request[0]:
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
                        'main_id':my_token_login_request[1].d['main_id'],
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
                        {'name':'管控部门'},{'name':'销售部门'},{'name':'生产部门'}
                    ],
                    'labor_contract':[
                        {'name':'合同制'},{'name':'派遣制'},{'name':'第三方'},{'name':'实习生'},{'name':'其它'}
                    ],
                    'create_time':datetime.datetime.now(),
                    'create_person_main_id':my_token_login_request[1].d['main_id'],
                }
                models.wx_organization(d=d).save()
                wx_organization_match_main_id405 = models.wx_organization_match_main_id.objects(__raw__ = {
                    'd.certificate_for_uniform_social_credit_code':certificate_for_uniform_social_credit_code,
                    'd.main_id':my_token_login_request[1].d['main_id'],
                }).first()
                if wx_organization_match_main_id405 == None:
                    d = {
                        'certificate_for_uniform_social_credit_code':certificate_for_uniform_social_credit_code,
                        'organization_name':organization_name,
                        'organization_address':organization_address,
                        'main_id':my_token_login_request[1].d['main_id'],
                        'role':['super_admin','nomarl_admin','user'],
                        'department':'管理员',
                        'labor_contract':'合同制',
                    }
                    models.wx_organization_match_main_id(d=d).save()
                else:
                    d = wx_organization_match_main_id405.d
                    wx_organization_match_main_id405.update(d=d)
                d = my_token_login_request[1].d
                d['active_organization'] = certificate_for_uniform_social_credit_code #更新用户默认关联的组织
                my_token_login_request[1].update(d=d)
                code = 1
                data = {}
                msg = '创建成功'
                res = {'status': code, 'data': data, 'msg': msg}
                return myHttpResponse(res)
            else:
                code = 2
                data = {}
                msg = '组织已存在！'
                res = {'status': code, 'data': data, 'msg': msg}
                return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        code = 0
        data = {}
        msg = '系统异常'
        res = {'status': code, 'data': data, 'msg': msg}
        return myHttpResponse(res)

def wx_get_organizationInfo_list(request):
    import json
    import traceback
    import time
    from . import models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        my_token_login_request = my_token_login(request)
        if my_token_login_request[0]:
            sendData = request.GET['sendData']
            print(sendData,'-----------------wx_get_organizationInfo_list')
            sendData_json = json.loads(sendData)
            searchVal = sendData_json['searchVal']
            main_id = my_token_login_request[1].d['main_id']
            if searchVal == '':
                wx_organization_match_main_id478 = models.wx_organization_match_main_id.objects(__raw__ = {
                    'd.main_id' : main_id
                }).limit(10)
            else:
                wx_organization_match_main_id478 = models.wx_organization_match_main_id.objects(__raw__ = {
                    {'d.main_id' : main_id},
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
                })
            wx_organization_match_main_id478_len = len(list(wx_organization_match_main_id478))
            if(wx_organization_match_main_id478_len == 0):
                code = 2
                data = {}
                msg = '无关联组织'
                res = {'status': code, 'data': data, 'msg': msg}
                return myHttpResponse(res)
            else:
                organization_list = wx_organization_match_main_id478.to_json().encode('utf-8').decode('unicode_escape')
                organization_list = json.loads(organization_list)
                code = 1
                data = {'organization_list':organization_list}
                msg = '查询到'+str(wx_organization_match_main_id478_len)+'个！'
                res = {'status': code, 'data': data, 'msg': msg}
                return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        code = 0
        data = {}
        msg = '系统异常'
        res = {'status': code, 'data': data, 'msg': msg}
        return myHttpResponse(res)

def wx_swicth_organization(request):
    import json
    import traceback
    import time
    from . import models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        my_token_login_request = my_token_login(request)
        if my_token_login_request[0]:
            sendData = request.GET['sendData']
            print(sendData,'-----------------wx_swicth_organization')
            sendData_json = json.loads(sendData)
            organizationInfo = sendData_json['organizationInfo']
            main_id = my_token_login_request[1].d['main_id']
            certificate_for_uniform_social_credit_code = organizationInfo['d']['certificate_for_uniform_social_credit_code']
            wx_organization_match_main_id537 = models.wx_organization_match_main_id.objects(__raw__ = {
                'd.certificate_for_uniform_social_credit_code' : certificate_for_uniform_social_credit_code,
                'd.main_id' : main_id
            }).first()
            if wx_organization_match_main_id537 == None:
                code = 3
                data = {}
                msg = '你不属于该组织'
                res = {'status': code, 'data': data, 'msg': msg}
                return myHttpResponse(res)
            else:
                d = my_token_login_request[1].d
                d['active_organization'] = certificate_for_uniform_social_credit_code
                my_token_login_request[1].update(d=d)
                d['openid'] = '' #删除敏感信息
                d['session_key'] = '' #删除敏感信息
                code = 1
                data = {'userInfo':d}
                msg = '切换成功'
                res = {'status': code, 'data': data, 'msg': msg}
                return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        code = 0
        data = {}
        msg = '系统异常'
        res = {'status': code, 'data': data, 'msg': msg}
        return myHttpResponse(res)

def wx_get_apply_for_join_organization(request):
    import json
    import traceback
    import time
    import datetime
    from . import models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        my_token_login_request = my_token_login(request)
        if my_token_login_request[0]:
            sendData = request.GET['sendData']
            print(sendData,'-----------------wx_get_apply_for_join_organization')
            sendData_json = json.loads(sendData)
            main_id = my_token_login_request[1].d['main_id']
            active_organization = my_token_login_request[1].d['active_organization']
            if 'apply_status' in sendData_json:
                apply_status = sendData_json['apply_status']
                if apply_status == 'todo':
                    wx_join_organization_apply_id584 = models.wx_join_organization_apply.objects(__raw__ = {
                        'd.certificate_for_uniform_social_credit_code' : active_organization,
                        'd.apply_status':apply_status
                    })
                else:
                    code = 5
                    data = {}
                    msg = 'TODO'
                    res = {'status': code, 'data': data, 'msg': msg}
                    return myHttpResponse(res)
            else:
                code = 4
                data = {}
                msg = '参数错误'
                res = {'status': code, 'data': data, 'msg': msg}
                return myHttpResponse(res)
            wx_join_organization_apply_id584_len = len(list(wx_join_organization_apply_id584))
            if wx_join_organization_apply_id584_len == 0:
                code = 3
                data = {}
                msg = '暂无申请'
                res = {'status': code, 'data': data, 'msg': msg}
                return myHttpResponse(res)
            else:
                organization_apply_list = wx_join_organization_apply_id584.to_json().encode('utf-8').decode('unicode_escape')
                organization_apply_list = json.loads(organization_apply_list)
                code = 1
                data = {'organization_apply_list':organization_apply_list}
                msg = '查询成功'
                res = {'status': code, 'data': data, 'msg': msg}
                return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        code = 0
        data = {}
        msg = '系统异常'
        res = {'status': code, 'data': data, 'msg': msg}
        return myHttpResponse(res)

def wx_appral_apply_for_join_organization(request):
    import json
    import traceback
    import time
    import datetime
    from . import models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        my_token_login_request = my_token_login(request)
        if my_token_login_request[0]:
            def update_wx_join_organization_apply(my_token_login_request,apply,param):
                certificate_for_uniform_social_credit_code = my_token_login_request[1].d['active_organization']
                apply_person_main_id = apply['d']['apply_person_main_id']
                wx_join_organization_apply662 = models.wx_join_organization_apply.objects(__raw__ = {
                    'd.certificate_for_uniform_social_credit_code':certificate_for_uniform_social_credit_code,
                    'd.apply_person_main_id':apply_person_main_id
                }).first()
                if wx_join_organization_apply662 == None:
                    pass
                else:
                    d = wx_join_organization_apply662.d
                    if param == 'yes':
                        d['is_accept'] = True
                        d['apply_status'] = 'accept'
                        d['approval_person_main_id'] = my_token_login_request[1].d['main_id']
                        d['approval_time'] = datetime.datetime.now()
                        wx_join_organization_apply662.update(d=d)
                    elif param == 'no':
                        d['apply_status'] = 'deny'
                        d['approval_person_main_id'] = my_token_login_request[1].d['main_id']
                        d['approval_time'] = datetime.datetime.now()
                        wx_join_organization_apply662.update(d=d)
                    else:
                        pass
            sendData = request.GET['sendData']
            print(sendData,'-----------------wx_appral_apply_for_join_organization')
            sendDataJson =  json.loads(sendData)
            apply = sendDataJson['apply']
            apply_person_main_id = apply['d']['apply_person_main_id']
            param = sendDataJson['param']
            if not (my_token_login_request[2]['super_admin'] or my_token_login_request[2]['normal_admin']): #权限验证
                code = 4
                data = {}
                msg = '没有权限'
                res = {'status': code, 'data': data, 'msg': msg}
                return myHttpResponse(res)
            if param == 'yes':
                wx_organization_match_main_id666 = models.wx_organization_match_main_id.objects(__raw__ = {
                    'd.certificate_for_uniform_social_credit_code':apply['d']['certificate_for_uniform_social_credit_code'],
                    'd.main_id':apply_person_main_id
                }).first()
                if wx_organization_match_main_id666 == None:
                    wx_user713 = models.wx_user.objects(__raw__ = {
                        'd.main_id':apply_person_main_id
                    }).first()
                    if wx_user713 == None:
                        code = 5
                        data = {}
                        msg = '申请人主数据异常'
                        res = {'status': code, 'data': data, 'msg': msg}
                        return myHttpResponse(res)
                    d = {
                        'certificate_for_uniform_social_credit_code': apply['d']['certificate_for_uniform_social_credit_code'],
                        'main_id': apply_person_main_id,
                        'role': ['user'],
                        'department': apply['d']['apply_department']['name'],
                        'labor_contract': apply['d']['apply_for_labor_contract']['name'],
                    }
                    wx_organization_match_main_id(d=d).save()
                    d_wx_user713 = wx_user713.d
                    d['active_organization'] = apply['d']['apply_person_main_id']
                    wx_user713.update(d=d_wx_user713)
                    
                    update_wx_join_organization_apply(my_token_login_request,apply,param)
                    code = 1
                    data = {}
                    msg = '审批通过'
                    res = {'status': code, 'data': data, 'msg': msg}
                    return myHttpResponse(res)
                else:
                    d = wx_organization_match_main_id666.d
                    d['department'] = apply['d']['apply_for_department']['name']
                    d['labor_contract'] = apply['d']['apply_for_labor_contract']['name']
                    wx_organization_match_main_id666.update(d=d)
                    update_wx_join_organization_apply(my_token_login_request,apply,param)
                    code = 1
                    data = {}
                    msg = '更新成功'
                    res = {'status': code, 'data': data, 'msg': msg}
                    return myHttpResponse(res)
            elif param == 'no':
                update_wx_join_organization_apply(my_token_login_request,apply,param)
                code = 1
                data = {}
                msg = '已拒绝'
                res = {'status': code, 'data': data, 'msg': msg}
                return myHttpResponse(res)
            else:
                pass
        code = 0
        data = {}
        msg = '参数异常'
        res = {'status': code, 'data': data, 'msg': msg}
        return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        code = 0
        data = {}
        msg = '系统异常'
        res = {'status': code, 'data': data, 'msg': msg}
        return myHttpResponse(res)























