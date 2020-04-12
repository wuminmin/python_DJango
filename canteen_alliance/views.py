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
            #--------------公司或组织权限验证
            wx_organization_match_main_id36 = models.wx_organization_match_user.objects(__raw__ = {
                'd.main_id' : wx_user25.d['main_id'],
                'd.organization_main_id':wx_user25.d['active_organization']
            }).first()
            super_admin = False
            nomarl_admin = False
            user = False
            if wx_organization_match_main_id36 == None:
                pass
            else:
                if 'super_admin' in  wx_organization_match_main_id36.d['role']:
                    super_admin = True
                elif 'nomarl_admin' in wx_organization_match_main_id36.d['role']:
                    nomarl_admin = True
                elif 'user' in wx_organization_match_main_id36.d['role']:
                    user = True
                else:
                    pass
            role_dict_organization = {
                    'role_list':['super_admin','nomarl_admin','user'],
                    'main_id':wx_user25.d['main_id'],
                    'organization_main_id':wx_user25.d['active_organization'],
                    'super_admin':super_admin,
                    'nomarl_admin':nomarl_admin,
                    'user':user
            }
            #----------------

            #-----------供应商权限验证
            wx_supplier_match_main_id36 = models.wx_supplier_match_user.objects(__raw__ = {
                'd.main_id' : wx_user25.d['main_id'],
                'd.supplier_main_id':wx_user25.d['active_supplier']
            }).first()
            super_admin = False
            nomarl_admin = False
            user = False
            if wx_supplier_match_main_id36 == None:
                pass
            else:
                if 'super_admin' in  wx_supplier_match_main_id36.d['role']:
                    super_admin = True
                elif 'nomarl_admin' in wx_supplier_match_main_id36.d['role']:
                    nomarl_admin = True
                elif 'user' in wx_supplier_match_main_id36.d['role']:
                    user = True
                else:
                    pass
            role_dict_supplier = {
                    'role_list':['super_admin','nomarl_admin','user'],
                    'main_id':wx_user25.d['main_id'],
                    'supplier_main_id':wx_user25.d['active_supplier'],
                    'super_admin':super_admin,
                    'nomarl_admin':nomarl_admin,
                    'user':user
            }
            #----------------

            return (True,wx_user25,role_dict_organization,role_dict_supplier)
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
    from bson import ObjectId
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        d_wx_login_get_openid = wx_login_get_openid(request)
        print(d_wx_login_get_openid)
        openid = d_wx_login_get_openid['openid']
        session_key = d_wx_login_get_openid['session_key']
        wx_wx_info105 = models.wx_wx_info.objects(__raw__ = {
            'd.openid':openid
        }).first()
        if wx_wx_info105 == None:
            code = 2
            data = {'main_id': 1,'token':'','mobile':'','nickname':'','portrait':''}
            msg = '未注册'
            res = {'status': code, 'data': data, 'msg': msg}
            return myHttpResponse(res)
        else:
            d_wx_wx_info105 = wx_wx_info105.d
            d_wx_wx_info105['session_key'] = session_key
            wx_wx_info105.update(d=d_wx_wx_info105)
            main_id = wx_wx_info105.d['main_id']
            wx_user97 = models.wx_user.objects(__raw__={'d.main_id':main_id}).first()
            if wx_user97 == None:
                code = 4
                data = {'main_id': 1,'token':'','mobile':'','nickname':'','portrait':''}
                msg = '主数据不存在'
                res = {'status': code, 'data': data, 'msg': msg}
                return myHttpResponse(res)
            from . import tool
            tokenprogramer = tool.Token(
                api_secret = d_wx_login_get_openid['app_id'], #微信appid
                project_code = 'canteen_alliance', #项目名称
                account =  wx_user97.d['mobile'] #用户名
            )
            token = tokenprogramer.get_token()
            userInfo = wx_user97.d
            userInfo['token'] = token
            wx_user97.update(d=userInfo)
            organization_info = {}
            q_wx_organization129 = models.wx_organization.objects(
                __raw__ = {'d.organization_main_id':wx_user97.d['active_organization']}
            ).first()
            if q_wx_organization129 == None:
                pass
            else:
                organization_info = q_wx_organization129.d
            # goods_info = {}
            # q_wx_organization_match_supplier128 = models.wx_organization_match_supplier.objects(__raw__ = {
            #     'd.organization_main_id':wx_user97.d['active_organization']
            # }).first()
            # if q_wx_organization_match_supplier128 == None:
            #     pass
            # else:
            #     wx_goods_info135 = models.wx_goods_info.objects(id=ObjectId(q_wx_organization_match_supplier128.supplier_department_id)).first()
            #     if wx_supplier_info135 == None:
            #         pass
            #     else:
            #         goods_info = wx_goods_info135.d
            supplier_info = {}
            q_wx_supplier_info157 = models.wx_supplier_info.objects(__raw__ = {
                'd.supplier_main_id':wx_user97.d['active_supplier']
            }).first()
            if q_wx_supplier_info157 == None:
                pass
            else:
                supplier_info = q_wx_supplier_info157.d
            supplier_department_info = {}


            data = {
                'userInfo':userInfo,
                'organization_info':organization_info,
                'set_supplier_info':supplier_info,
                'set_supplier_department_info':supplier_department_info
            }
            print(data)
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
        d_wx_login_get_openid = wx_login_get_openid(request)
        print(d_wx_login_get_openid)
        openid = d_wx_login_get_openid['openid']
        app_id = d_wx_login_get_openid['app_id']
        session_key = d_wx_login_get_openid['session_key']
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
                api_secret = d_wx_login_get_openid['app_id'], #微信appid
                project_code = 'canteen_alliance', #项目名称
                account = mobile #用户名
            )
            token = tokenprogramer.get_token()
            portrait = 'https://dss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=1676131907,2302520392&fm=111&gp=0.jpg'
            q_wx_wx_info200 = models.wx_wx_info.objects(__raw__={'d.openid':openid}).first()
            if q_wx_wx_info200 == None:
                d = {
                    'openid':openid,
                    'app_id':app_id,
                    'session_key':session_key,
                    'mobile':mobile,
                }
                models.wx_wx_info(d=d).save()
            q_wx_wx_info209 = models.wx_wx_info.objects(__raw__={'d.openid':openid}).first()
            if q_wx_wx_info209 == None:
                code = 4
                data = {'main_id': '1','token':'','mobile':mobile,'nickname':'','portrait':''}
                msg = 'openid不存在'
                res = {'status': code, 'data': data, 'msg': msg}
                return myHttpResponse(res)
            else:
                d_wx_wx_info209 = q_wx_wx_info209.d
                wx_user97 = models.wx_user.objects(__raw__ = {
                    'd.mobile':mobile
                }).first()
                if wx_user97 == None:
                    d =  {
                        'main_id':str(q_wx_wx_info209.id),
                        'token':token,
                        'mobile':mobile,
                        'nickname':nickname,
                        'portrait':portrait,
                        'active_organization':'', #正在使用的组织统一代码
                    }
                    models.wx_user(d=d).save()
                    d_wx_wx_info209['main_id'] = str(q_wx_wx_info209.id)
                    q_wx_wx_info209.update(d=d_wx_wx_info209)
                else:
                    d_wx_user97 = wx_user97.d
                    d_wx_wx_info209['main_id'] = d_wx_user
                    q_wx_wx_info209.update(d=d_wx_wx_info209)
                    d_wx_user97['token'] = token #更新token
                    wx_user97.update(d=d_wx_user97)
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
        d_wx_login_get_openid = wx_login_get_openid(request)
        print(d_wx_login_get_openid)
        openid = d_wx_login_get_openid['openid']
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
                    'd.organization_main_id':{
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
        sendData = request.GET['sendData']
        sendData_json = json.loads(sendData)
        organization_main_id = sendData_json['organization_main_id']
        name = sendData_json['name']
        department = sendData_json['department']
        labor_contract = sendData_json['labor_contract']
        wx_join_organization_apply311 = models.wx_join_organization_apply.objects(__raw__ ={
            'd.organization_main_id':organization_main_id,
            'd.apply_person_main_id':my_token_login_request[1].d['main_id']
        }).first()
        import datetime
        from . import tool
        if wx_join_organization_apply311 == None:
            d = {
                'organization_main_id':organization_main_id,
                'apply_person_main_id':my_token_login_request[1].d['main_id'],
                'apply_person_name':name,
                'apply_for_department':department,
                'apply_for_labor_contract':labor_contract,
                'apply_time':tool.Time().now_time(),
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
            from . import tool
            d = wx_join_organization_apply311.d
            d['apply_person_name'] = name
            d['apply_for_department'] = department
            d['apply_for_labor_contract'] = labor_contract
            d['apply_time'] = tool.Time().now_time()
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

def wx_create_organization(request):
    import json
    import traceback
    import time
    from . import models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        my_token_login_request = my_token_login(request)
        sendData = request.GET['sendData']
        sendData_json = json.loads(sendData)
        organization_main_id = sendData_json['organization_main_id']
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
            from . import tool
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
                'create_time':tool.Time().now_time(),
                'create_person_main_id':my_token_login_request[1].d['main_id'],
            }
            models.wx_organization(d=d).save()
            wx_organization448 = models.wx_organization.objects(__raw__ = {
                'd.certificate_for_uniform_social_credit_code' : certificate_for_uniform_social_credit_code
            }).first()
            if wx_organization448 == None:
                code = 0
                data = {}
                msg = '系统异常'
                res = {'status': code, 'data': data, 'msg': msg}
                return myHttpResponse(res)
            else:
                organization_main_id = str(wx_organization448.id)
                d_wx_organization448 = wx_organization448.d
                d_wx_organization448['organization_main_id'] = organization_main_id
                wx_organization448.update(d = d_wx_organization448 )
                wx_organization_match_main_id405 = models.wx_organization_match_user.objects(__raw__ = {
                    'd.organization_main_id':organization_main_id,
                    'd.main_id':my_token_login_request[1].d['main_id'],
                }).first()
                if wx_organization_match_main_id405 == None:
                    d = {
                        'organization_main_id':organization_main_id,
                        'main_id':my_token_login_request[1].d['main_id'],
                        'role':['super_admin','nomarl_admin','user'],
                        'department':'管理员',
                        'labor_contract':'合同制',
                    }
                    models.wx_organization_match_user(d=d).save()
                d_wx_user = my_token_login_request[1].d
                d_wx_user['active_organization'] = organization_main_id #更新用户默认关联的组织
                my_token_login_request[1].update(d=d_wx_user)
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
        sendData = request.GET['sendData']
        print(sendData,'-----------------wx_get_organizationInfo_list')
        sendData_json = json.loads(sendData)
        searchVal = sendData_json['searchVal']
        main_id = my_token_login_request[1].d['main_id']
        if searchVal == '':
            wx_organization_match_main_id478 = models.wx_organization_match_user.objects(__raw__ = {
                'd.main_id' : main_id
            }).limit(10)
        else:
            wx_organization_match_main_id478 = models.wx_organization_match_user.objects(__raw__ = {
                {'d.main_id' : main_id},
                {
                    'd.organization_name':{
                        '$regex':".*"+searchVal+".*"
                    }
                },
                {
                    'd.organization_main_id':{
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
        sendData = request.GET['sendData']
        print(sendData,'-----------------wx_swicth_organization')
        sendData_json = json.loads(sendData)
        organizationInfo = sendData_json['organizationInfo']
        main_id = my_token_login_request[1].d['main_id']
        organization_main_id = organizationInfo['d']['organization_main_id']
        wx_organization_match_main_id537 = models.wx_organization_match_user.objects(__raw__ = {
            'd.organization_main_id' : organization_main_id,
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
            d['active_organization'] = organization_main_id
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
        sendData = request.GET['sendData']
        print(sendData,'-----------------wx_get_apply_for_join_organization')
        sendData_json = json.loads(sendData)
        main_id = my_token_login_request[1].d['main_id']
        active_organization = my_token_login_request[1].d['active_organization']
        if 'apply_status' in sendData_json:
            apply_status = sendData_json['apply_status']
            if apply_status == 'todo':
                wx_join_organization_apply_id584 = models.wx_join_organization_apply.objects(__raw__ = {
                    'd.organization_main_id' : active_organization,
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
        def update_wx_join_organization_apply(my_token_login_request,apply,param):
            organization_main_id = my_token_login_request[1].d['active_organization']
            apply_person_main_id = apply['d']['apply_person_main_id']
            wx_join_organization_apply662 = models.wx_join_organization_apply.objects(__raw__ = {
                'd.organization_main_id':organization_main_id,
                'd.apply_person_main_id':apply_person_main_id
            }).first()
            if wx_join_organization_apply662 == None:
                pass
            else:
                from . import tool
                d = wx_join_organization_apply662.d
                if param == 'yes':
                    d['is_accept'] = True
                    d['apply_status'] = 'accept'
                    d['approval_person_main_id'] = my_token_login_request[1].d['main_id']
                    d['approval_time'] = tool.Time().now_time()
                    wx_join_organization_apply662.update(d=d)
                elif param == 'no':
                    d['apply_status'] = 'deny'
                    d['approval_person_main_id'] = my_token_login_request[1].d['main_id']
                    d['approval_time'] = tool.Time().now_time()
                    wx_join_organization_apply662.update(d=d)
                else:
                    pass
        sendData = request.GET['sendData']
        print(sendData,'-----------------wx_appral_apply_for_join_organization')
        sendDataJson =  json.loads(sendData)
        apply = sendDataJson['apply']
        apply_person_main_id = apply['d']['apply_person_main_id']
        param = sendDataJson['param']
        if not (my_token_login_request[2]['super_admin'] or my_token_login_request[2]['nomarl_admin']): #权限验证
            code = 4
            data = {}
            msg = '没有权限'
            res = {'status': code, 'data': data, 'msg': msg}
            return myHttpResponse(res)
        if param == 'yes':
            wx_organization_match_main_id666 = models.wx_organization_match_user.objects(__raw__ = {
                'd.organization_main_id':apply['d']['organization_main_id'],
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
                    'organization_main_id': apply['d']['organization_main_id'],
                    'main_id': apply_person_main_id,
                    'role': ['user'],
                    'department': apply['d']['apply_department']['name'],
                    'labor_contract': apply['d']['apply_for_labor_contract']['name'],
                }
                wx_organization_match_user(d=d).save()
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

def wx_create_supplier(request):
    import json
    import traceback
    import time
    from . import models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        my_token_login_request = my_token_login(request)
        sendData = request.GET['sendData']
        sendData_json = json.loads(sendData)
        supplier_main_id = sendData_json['supplier_main_id']
        certificate_for_uniform_social_credit_code = sendData_json['certificate_for_uniform_social_credit_code']
        supplier_name = sendData_json['supplier_name']
        supplier_address = sendData_json['supplier_address']
        legal_person_name = sendData_json['legal_person_name']
        legal_person_mobile = sendData_json['legal_person_mobile']
        manage_person_name = sendData_json['manage_person_name']
        manage_person_mobile = sendData_json['manage_person_mobile']
        wx_supplier373 = models.wx_supplier_info.objects(__raw__ ={
            'd.certificate_for_uniform_social_credit_code':certificate_for_uniform_social_credit_code
        }).first()
        import datetime
        if wx_supplier373 == None:
            from . import tool
            d = {
                'certificate_for_uniform_social_credit_code':certificate_for_uniform_social_credit_code,
                'supplier_name':supplier_name,
                'supplier_address':supplier_address,
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
                'supplier_department_id_list':[],
                'labor_contract':[
                    {'name':'合同制'},{'name':'派遣制'},{'name':'第三方'},{'name':'实习生'},{'name':'其它'}
                ],
                'create_time':tool.Time().now_time(),
                'create_person_main_id':my_token_login_request[1].d['main_id'],
            }
            models.wx_supplier_info(d=d).save()
            wx_supplier448 = models.wx_supplier_info.objects(__raw__ = {
                'd.certificate_for_uniform_social_credit_code' : certificate_for_uniform_social_credit_code
            }).first()
            if wx_supplier448 == None:
                code = 0
                data = {}
                msg = '系统异常'
                res = {'status': code, 'data': data, 'msg': msg}
                return myHttpResponse(res)
            else:
                supplier_main_id = str(wx_supplier448.id)
                d_wx_supplier448 = wx_supplier448.d
                d_wx_supplier448['supplier_main_id'] = supplier_main_id
                wx_supplier448.update(d = d_wx_supplier448 )
                wx_supplier_match_main_id405 = models.wx_supplier_match_user.objects(__raw__ = {
                    'd.supplier_main_id':supplier_main_id,
                    'd.main_id':my_token_login_request[1].d['main_id'],
                }).first()
                if wx_supplier_match_main_id405 == None:
                    d = {
                        'supplier_main_id':supplier_main_id,
                        'main_id':my_token_login_request[1].d['main_id'],
                        'role':['super_admin','nomarl_admin','user'],
                        'department':'管理员',
                        'labor_contract':'合同制',
                    }
                    models.wx_supplier_match_user(d=d).save()
                d_wx_user = my_token_login_request[1].d
                d_wx_user['active_supplier'] = supplier_main_id #更新用户默认关联的组织
                my_token_login_request[1].update(d=d_wx_user)
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

def wx_create_supplier_department(request):
    import json
    import traceback
    import time
    from . import models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        my_token_login_request = my_token_login(request)
        if not (my_token_login_request[3]['super_admin'] or my_token_login_request[3]['nomarl_admin']): #供应商权限验证
            code = 4
            data = {}
            msg = '没有权限'
            res = {'status': code, 'data': data, 'msg': msg}
            return myHttpResponse(res)
        sendData = request.GET['sendData']
        sendData_json = json.loads(sendData)
        supplier_main_id = sendData_json['supplier_main_id']
        supplier_department_name = sendData_json['supplier_department_name']
        supplier_department_address = sendData_json['supplier_department_address']
        supplier_department_manage_person_name = sendData_json['supplier_department_manage_person_name']
        supplier_department_manage_person_mobile = sendData_json['supplier_department_manage_person_mobile']
        wx_supplier373 = models.wx_supplier_department_info.objects(__raw__ ={
            'd.supplier_department_name':supplier_department_name
        }).first()
        import datetime
        if wx_supplier373 == None:
            q983 = models.wx_supplier_info.objects(__raw__ = { 'd.supplier_main_id':supplier_main_id }).first()
            if q983 == None:
                code = 5
                data = {}
                msg = '没有供应商信息'
                res = {'status': code, 'data': data, 'msg': msg}
                return myHttpResponse(res)
            
            from . import tool
            supplier_department_id = my_token_login_request[1].d['token']
            d = {
                'supplier_department_id': supplier_department_id,
                'supplier_department_name':supplier_department_name,
                'supplier_department_address':supplier_department_address,
                'super_admin_person':{
                    'main_id':my_token_login_request[1].d['main_id'],
                    'name':'',
                    'moile':'',
                },
                'manage_person':{
                    'name':supplier_department_manage_person_name,
                    'mobile':supplier_department_manage_person_mobile
                },
                'labor_contract':[
                    {'name':'合同制'},{'name':'派遣制'},{'name':'第三方'},{'name':'实习生'},{'name':'其它'}
                ],
                'create_time':tool.Time().now_time(),
                'create_person_main_id':my_token_login_request[1].d['main_id'],
            }
            models.wx_supplier_department_info(d=d).save()
            d1013 = q983.d
            d1013['supplier_department_id_list'].append( supplier_department_id )
            q983.update(d= d1013)
            code = 1
            data = {}
            msg = '创建成功'
            res = {'status': code, 'data': data, 'msg': msg}
            return myHttpResponse(res)
        else:
            code = 2
            data = {}
            msg = '已存在！'
            res = {'status': code, 'data': data, 'msg': msg}
            return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        code = 0
        data = {}
        msg = '系统异常'
        res = {'status': code, 'data': data, 'msg': msg}
        return myHttpResponse(res)

def wx_get_supplierInfo_list(request):
    import json
    import traceback
    import time
    from . import models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        my_token_login_request = my_token_login(request)
        sendData = request.GET['sendData']
        print(sendData,'-----------------wx_get_supplierInfo_list')
        sendData_json = json.loads(sendData)
        searchVal = sendData_json['searchVal']
        main_id = my_token_login_request[1].d['main_id']
        if searchVal == '':
            wx_supplier_match_main_id478 = models.wx_supplier_match_user.objects(__raw__ = {
                'd.main_id' : main_id
            }).limit(10)
        else:
            wx_supplier_match_main_id478 = models.wx_supplier_match_user.objects(__raw__ = {
                {'d.main_id' : main_id},
                {
                    'd.supplier_name':{
                        '$regex':".*"+searchVal+".*"
                    }
                },
                {
                    'd.supplier_main_id':{
                            '$regex':".*"+searchVal+".*"
                        # '$regex':'/^([0-9A-HJ-NPQRTUWXY]{2}\d{6}[0-9A-HJ-NPQRTUWXY]{10}|[1-9]\d{14})$/'
                    }
                }
            })
        wx_supplier_match_main_id478_len = len(list(wx_supplier_match_main_id478))
        if(wx_supplier_match_main_id478_len == 0):
            code = 2
            data = {}
            msg = '无关联组织'
            res = {'status': code, 'data': data, 'msg': msg}
            return myHttpResponse(res)
        else:
            supplier_list = wx_supplier_match_main_id478.to_json().encode('utf-8').decode('unicode_escape')
            supplier_list = json.loads(supplier_list)
            code = 1
            data = {'supplier_list':supplier_list}
            msg = '查询到'+str(wx_supplier_match_main_id478_len)+'个！'
            res = {'status': code, 'data': data, 'msg': msg}
            return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        code = 0
        data = {}
        msg = '系统异常'
        res = {'status': code, 'data': data, 'msg': msg}
        return myHttpResponse(res)

def wx_swicth_supplier(request):
    import json
    import traceback
    import time
    from . import models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        my_token_login_request = my_token_login(request)
        sendData = request.GET['sendData']
        print(sendData,'-----------------wx_swicth_supplier')
        sendData_json = json.loads(sendData)
        supplierInfo = sendData_json['supplierInfo']
        main_id = my_token_login_request[1].d['main_id']
        supplier_main_id = supplierInfo['d']['supplier_main_id']
        wx_supplier_match_main_id537 = models.wx_supplier_match_user.objects(__raw__ = {
            'd.supplier_main_id' : supplier_main_id,
            'd.main_id' : main_id
        }).first()
        if wx_supplier_match_main_id537 == None:
            code = 3
            data = {}
            msg = '你不属于该组织'
            res = {'status': code, 'data': data, 'msg': msg}
            return myHttpResponse(res)
        else:
            d = my_token_login_request[1].d
            d['active_supplier'] = supplier_main_id
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

def wx_get_my_wx_supplier_department_info_list(request):
    import json
    import traceback
    import time
    from . import models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        my_token_login_request = my_token_login(request)
        sendData = request.GET['sendData']
        print(sendData,'-----------------wx_get_my_wx_supplier_department_info_list')
        sendData_json = json.loads(sendData)
        supplier_info = sendData_json['supplier_info']
        main_id = my_token_login_request[1].d['main_id']
        supplier_department_id_list = supplier_info['d']['supplier_department_id_list']
        supplier_department_info_list = []
        for o in supplier_department_id_list:
            q1143 = models.wx_supplier_department_info.objects(__raw__ = {'d.supplier_department_id':o}).first()
            t1144 = q1143.to_json().encode('utf-8').decode('unicode_escape')
            supplier_department_info_list.append(json.loads(t1144))
        if supplier_department_info_list == []:
            code = 2
            data = {'supplier_department_info_list':[]}
            msg = '没有数据'
            res = {'status': code, 'data': data, 'msg': msg}
            return myHttpResponse(res)
        else:
            code = 1
            data = {'supplier_department_info_list':[]}
            msg = '成功'
            res = {'status': code, 'data': data, 'msg': msg}
            return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        code = 0
        data = {}
        msg = '系统异常'
        res = {'status': code, 'data': data, 'msg': msg}
        return myHttpResponse(res)
























































