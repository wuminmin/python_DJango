

from . import models,db,tool,wmm
import myConfig
import json
import traceback
import time
from django.http import HttpResponse, FileResponse

def deprecated_async(f): # 异步函数
    def wrapper(*args, **kwargs):
        from threading import Thread
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

def myHttpResponse(res):  # 合并跨域配置
    response = HttpResponse(json.dumps(res))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def my_token_login(request):
    import requests
    token = request.GET['token']
    wx_user25 = models.wx_user.objects(__raw__ = {
            'd.token':token
    }).first()
    if wx_user25 == None:
        return myHttpResponse( {'status': 2, 'data': {}, 'msg': '已超时，请重新登录'} )
    else:
        return {'wx_user_d':wx_user25.d}

def wx_login_get_openid(request): #解析openid
    import requests
    try:
        sendData = json.loads(request.GET['sendData'])
        code = sendData['code']
        app_id = sendData['app_id']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': app_id, 'secret': myConfig.appid_secret_dict[app_id], 'js_code': code,
                    'grant_type': 'authorization_code'}
        r = requests.get(url=url, params=payload)
        myConfig.debug_print(r.text,'------------wx_login_get_openid')
        r_json = json.loads(r.text)
        openid = r_json['openid']
        session_key = r_json['session_key']
        return {'openid':openid,'session_key':session_key,'app_id':app_id}
    except:
        myConfig.debug_print(traceback.format_exc())
        return {'openid':'','session_key':'','app_id':''}

def wx_login(request):  # 微信小程序登录
    try:
        d_wx_login_get_openid = wx_login_get_openid(request)
        openid = d_wx_login_get_openid['openid']
        app_id = d_wx_login_get_openid['app_id']
        session_key = d_wx_login_get_openid['session_key']
        q1 = db.query_wx_openid_first2('openid',openid,'app_id',app_id)
        if not q1 == None:
            mobile = q1.d['mobile']
            q2 = db.query_wx_user_first('mobile',mobile)
            if not q2 == None:
                user_info = q2.d
                q3 = db.query_wx_organization_match_user_first2(
                    'user_main_id',q2.d['main_id'],
                    'is_default_organization',True
                )
                if not q3 == None:
                    organization_department_info = {'has':True,'name':q3.d['department']}
                    organization_department_info_list = db.query_wx_organization_match_user_list2(
                        'user_main_id',q2.d['main_id'],
                        'is_default_organization',True
                    )
                    q4 = db.query_wx_organization_first('main_id',q3.d['organization_main_id'])
                    if q4 == None:
                        organization_info = {'has':False}
                    else:
                        organization_info = q4.d
                else:
                    organization_info = {'has':False}
                    organization_department_info =  {'has':False}
                    organization_department_info_list =  []

                q3 = db.query_wx_supplier_match_user_first2(
                    'user_main_id',q2.d['main_id'],
                    'is_default_supplier',True
                )
                if not q3 == None:
                    supplier_department_info = {'has':True,'name':q3.d['department']}
                    supplier_department_info_list = db.query_wx_supplier_match_user_list2(
                        'user_main_id',q2.d['main_id'],
                        'is_default_supplier',True
                    )
                    q4 = db.query_wx_supplier_first('main_id',q3.d['supplier_main_id'])
                    if q4 == None:
                        supplier_info = {'has':False}
                    else:
                        supplier_info = q4.d
                else:
                    supplier_info = {'has':False}
                    supplier_department_info =  {'has':False}
                    supplier_department_info_list =  []

                data = {
                    'user_info':user_info,
                    'organization_info':organization_info,
                    'organization_department_info':organization_department_info,
                    'organization_department_info_list':organization_department_info_list,
                    'supplier_info':supplier_info,
                    'supplier_department_info':supplier_department_info,
                    'supplier_department_info_list':supplier_department_info_list,
                }
                return myHttpResponse( {'status': 1, 'data': data, 'msg': '登录成功'} )
            else:
                return myHttpResponse({'status': 2, 'data': {}, 'msg': '用户未注册'})
        else:
            return myHttpResponse( {'status': 3, 'data': {}, 'msg': '未绑定微信'} )
    except:
        myConfig.debug_print(traceback.format_exc())
        res = {'code': 500, 'data': {}, 'msg': '系统故障'}
        return myHttpResponse(res)

def wx_register(request):  #wx注册
    try:
        d_wx_login_get_openid = wx_login_get_openid(request)
        openid = d_wx_login_get_openid['openid']
        app_id = d_wx_login_get_openid['app_id']
        session_key = d_wx_login_get_openid['session_key']
        sendData_json = json.loads(request.GET['sendData'])
        nickname = sendData_json['nickname']
        mobile = sendData_json['mobile']
        password = sendData_json['password']
        q1 = db.query_wx_sms_first2('mobile',mobile,'password',password)
        if q1 == None:
            return myHttpResponse( {'status': 2, 'data': {}, 'msg': '验证码不正确'} )
        else:
            q2 = db.create_wx_user_by_mobile(mobile,{'nickname':nickname})
            if not q2 == None:
                q3 = db.create_wx_openid_by_mobile(mobile,openid,app_id,session_key,{})
                if not q3 == None:
                    return myHttpResponse({'status': 1, 'data': {'user_info':q2.d}, 'msg': '注册成功'})
                else:
                    if db.update_wx_openid_by_mobile(mobile,openid,app_id,session_key,{}):
                        return myHttpResponse({'status': 1, 'data': {'user_info':q2.d}, 'msg': '注册成功'})
                    else:
                        return myHttpResponse({'status': 2, 'data': {}, 'msg': '更新微信关联信息失败'})
            else:
                return myHttpResponse({'status': 3, 'data': {}, 'msg': '创建用户信息失败'})
    except:
        myConfig.debug_print(traceback.format_exc())
        return myHttpResponse({'status': 0, 'data': {}, 'msg': '系统异常'})

def wx_send_sms(request): #wx发短信
    try:
        # d_wx_login_get_openid = wx_login_get_openid(request)
        # openid = d_wx_login_get_openid['openid']
        # app_id = d_wx_login_get_openid['app_id']
        # session_key = d_wx_login_get_openid['session_key']
        sendData_json = json.loads(request.GET['sendData'])
        mobile = sendData_json['mobile']
        if not tool.check_mobile(mobile):
            return myHttpResponse({'status':2,'data':{},'msg':'手机号有误'} )
        else:
            import random
            import uuid
            j = 6
            sms_code = ''.join(str(i) for i in random.sample(range(0, 9), j))  # sample(seq, n) 从序列seq中选择n个随机且独立的元素；
            __business_id = uuid.uuid1()
            params = "{\"code\":\"" + sms_code + "\"}"
            r = tool.send_sms(__business_id, mobile, myConfig.sign_name, myConfig.template_code, params)
            myConfig.debug_print(r,'---------------阿里云短信网关')
            r2 = json.loads(r)
            if r2['Code'] == 'OK':
                q1 = db.create_wx_sms_by_mobile(mobile,sms_code)
                if q1 ==None:
                    if db.update_wx_sms_by_mobile(mobile,sms_code):
                        return myHttpResponse({'status':1,'data':{},'msg':'短信发送成功'})
                    else:
                        return myHttpResponse({'status':2,'data':{},'msg':'验证码更新失败'})
                else:
                    return myHttpResponse({'status':1,'data':{},'msg':'短信发送成功'})
            else:
                return myHttpResponse({'status':1,'data':{},'msg':'短信发送失败'})
    except:
        myConfig.debug_print(traceback.format_exc())
        return myHttpResponse({'status': 0, 'data': {}, 'msg': '系统异常'})

def wx_sync_info(request):
    try:
        q2 = db.query_wx_user_first('token',request.GET['token'])
        if not q2 == None:
            user_info = q2.d
            q3 = db.query_wx_organization_match_user_first2(
                'user_main_id',q2.d['main_id'],
                'is_default_organization',True
            )
            if not q3 == None:
                organization_department_info = {'has':True,'name':q3.d['department']}
                q4 = db.query_wx_organization_first('main_id',q3.d['organization_main_id'])
                if q4 == None:
                    organization_info = {'has':False}
                else:
                    organization_info = q4.d
                l1 = db.query_wx_organization_match_user_list2(
                    'user_main_id',q2.d['main_id'],
                    'is_default_organization',True
                )
                organization_department_info_list = {'has':True,'info_list':l1}
            else:
                organization_info = {'has':False}
                organization_department_info =  {'has':False}
                organization_department_info_list =  []
            q3 = db.query_wx_supplier_match_user_first2(
                'user_main_id',q2.d['main_id'],
                'is_default_supplier',True
            )
            if not q3 == None:
                supplier_department_info = {'has':True,'name':q3.d['department']}
                q4 = db.query_wx_supplier_first('main_id',q3.d['supplier_main_id'])
                if q4 == None:
                    supplier_info = {'has':False}
                else:
                    supplier_info = q4.d
                l1 = db.query_wx_supplier_match_user_list2(
                    'user_main_id',q2.d['main_id'],
                    'is_default_supplier',True
                )
                supplier_department_info_list = {'has':True,'info_list':l1}
            else:
                supplier_info = {'has':False}
                supplier_department_info =  {'has':False}
                supplier_department_info_list =  []
            data = {
                'user_info':user_info,
                'organization_info':organization_info,
                'organization_department_info':organization_info,
                'organization_department_info_list':organization_department_info_list,
                'supplier_info':supplier_info,
                'supplier_department_info':supplier_department_info,
                'supplier_department_info_list':supplier_department_info_list,
            }
            return myHttpResponse( {'status': 1, 'data': data, 'msg': '同步成功'} )
        else:
            return myHttpResponse({'status': 2, 'data': {}, 'msg': '用户未注册'})
    except:
        myConfig.debug_print(traceback.format_exc())
        res = {'code': 500, 'data': {}, 'msg': '系统故障'}
        return myHttpResponse(res)

def wx_search_organization(request):
    try:
        sendData_json = json.loads(request.GET['sendData'])
        searchVal = sendData_json['searchVal']
        l1 = db.query_wx_organization_list_by_regex2(
            'organization_name',searchVal,
            'certificate_for_uniform_social_credit_code',searchVal
        )
        if l1 == []:
            return myHttpResponse( {'status': 2, 'data': {'organization_list':[]}, 'msg': '没有组织'} )
        else:
            code = 1
            data = {'organization_list':l1}
            msg = '成功'
            return myHttpResponse({'status':1,'data':{'organization_list':l1},'msg':'成功'})
    except:
        myConfig.debug_print(traceback.format_exc())
        return myHttpResponse({'status':0,'data':{},'msg':'系统异常'})

def wx_commit_apply_for_organization(request):
    try:
        q1 = db.query_wx_user_first('token',request.GET['token'])
        if not q1 == None:
            sendData_json = json.loads(request.GET['sendData'])
            cfuscc = sendData_json['certificate_for_uniform_social_credit_code']
            name = sendData_json['name']
            department = sendData_json['department']
            labor_contract = sendData_json['labor_contract']
            q2 = db.query_wx_organization_first('certificate_for_uniform_social_credit_code',cfuscc)
            if not q2 == None:
                q3 = db.query_wx_organization_match_user_first2(
                    'user_main_id',q1.d['main_id'],
                    'organization_main_id',q2.d['main_id']
                )
                if not q3 == None:
                    if db.update_wx_organization_match_user(
                        q2.d['main_id'],q1.d['main_id'],
                        {

                        }
                    ):
                        return myHttpResponse({'status':1,'data':{},'msg':'已收到申请'})
                    else:
                        return myHttpResponse({'status':1,'data':{},'msg':'更新申请失败'})
                else:
                    return myHttpResponse({'status':1,'data':{},'msg':'更新申请失败'})
            else:
                return myHttpResponse({'status':1,'data':{},'msg':'更新申请失败'})
        else:
            return myHttpResponse({'status':1,'data':{},'msg':'更新申请失败'})
    except:
        myConfig.debug_print(traceback.format_exc())
        return myHttpResponse({'status': 0, 'data': {}, 'msg': '系统异常'})

def wx_joinDepartment(request):
    try:
        my_token_login_request = db.query_wx_user_first('token',request.GET['token'])

        sendData = request.GET['sendData']
        sendData_json = json.loads(sendData)
        organization_main_id = sendData_json['organization_main_id']
        name = sendData_json['name']
        department = sendData_json['department']
        labor_contract = sendData_json['labor_contract']
        wx_join_organization_apply311 = models.wx_join_organization_apply.objects(__raw__ ={
            'd.organization_main_id':organization_main_id,
            'd.apply_person_main_id':my_token_login_request['main_id']
        }).first()
        if wx_join_organization_apply311 == None:
            d426 = {
                'organization_main_id':organization_main_id,
                'apply_person_main_id':my_token_login_request['main_id'],
                'apply_person_name':name,
                'apply_for_department':department,
                'apply_for_labor_contract':labor_contract,
                'apply_time':tool.Time().now_time(),
                'apply_status':'todo',
                'is_accept':False,
                'approval_person_main_id':'',
                'approval_time':'',
            }
            models.wx_join_organization_apply(d=d426).save()
            code = 1
            data = {}
            msg = '已收到申请'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
        else:
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
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
    except:
        myConfig.debug_print(traceback.format_exc())
        return myHttpResponse({'status': 0, 'data': {}, 'msg': '系统异常'})

def wx_create_organization(request):
    try:
        q1 = db.query_wx_user_first('token',request.GET['token'])
        if q1 == None:
            return myHttpResponse({'status': 999, 'data': {}, 'msg': '已超时'})
        myConfig.debug_print(q1)
        sendData_json = json.loads(request.GET['sendData'])
        cfuscc = sendData_json['certificate_for_uniform_social_credit_code']
        organization_name = sendData_json['organization_name']
        organization_address = sendData_json['organization_address']
        q2 = db.create_wx_organization_by_cfuscc(
            cfuscc,{
                'name':organization_name,'address':organization_address
        })
        if not q2 == None: 
            q3 = db.create_wx_organization_match_user(
                q2.d['main_id'],
                q1.d['main_id'],
                {
                    'role':'超级管理员',
                    'labor_attribute':'合同制',
                    'department':'其它部门',
                }
            )
            if not q3 == None:
                return myHttpResponse({'status': 1, 'data': {'organization_info':q2.d},'msg':'创建成功'} )
            else:
                return myHttpResponse({'status': 1, 'data': {'organization_info':q2.d},'msg':'个人与组织已存在关联'} )
        else:
            return myHttpResponse({'status': 3, 'data': {}, 'msg': '失败！统一代码重复'})
    except:
        myConfig.debug_print(traceback.format_exc())
        return myHttpResponse({'status': 0, 'data': {}, 'msg': '系统异常'})

def wx_get_organizationInfo_list(request):
    try:
        my_token_login_request = db.query_wx_user_first('token',request.GET['token'])
        sendData = request.GET['sendData']
        myConfig.debug_print(sendData,'-----------------wx_get_organizationInfo_list')
        sendData_json = json.loads(sendData)
        searchVal = sendData_json['searchVal']
        main_id = my_token_login_request['main_id']
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
        if list(wx_organization_match_main_id478) == []:
            code = 2
            data = {}
            msg = '无关联组织'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
        else:
            organization_list = []
            for o in wx_organization_match_main_id478:
                q569 = models.wx_organization.objects(__raw__={'d.organization_main_id':o.d['organization_main_id']}).first()
                if q569 == None:
                    continue
                else:
                    organization_list.append(tool.wmm_to_json(q569))
            code = 1
            data = {'organization_list':organization_list}
            msg = '成功'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
    except:
        myConfig.debug_print(traceback.format_exc())
        return myHttpResponse({'status': 0, 'data': {}, 'msg': '系统异常'})

def wx_swicth_organization(request):
    try:
        my_token_login_request = db.query_wx_user_first('token',request.GET['token'])
        sendData = request.GET['sendData']
        myConfig.debug_print(sendData,'-----------------wx_swicth_organization')
        sendData_json = json.loads(sendData)
        organizationInfo = sendData_json['organizationInfo']
        main_id = my_token_login_request['main_id']
        organization_main_id = organizationInfo['d']['organization_main_id']
        q592 = models.wx_organization_match_user.objects(__raw__ = {
            'd.organization_main_id' : organization_main_id,
            'd.main_id' : main_id
        }).first()
        if q592 == None:
            code = 3
            data = {}
            msg = '你不属于该组织'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
        else:
            q607 = models.wx_organization.objects(__raw__={'d.organization_main_id':q592.d['organization_main_id']}).first()
            if q607 == None:
                return myHttpResponse({'status': 2, 'data': {}, 'msg': '没有组织'})
            #更新默认组织信息
            d609 = my_token_login_request
            d609['active_organization'] = q592.d['organization_main_id']
            my_token_login_request[1].update(d=d609)
            #-----
            l582 = wmm.query_organization_department_info_list_for_vuex(q592.d['organization_main_id'])
            code = 1
            data = {'organization_info':q607.d,'organization_department_info_list':l582}
            msg = '切换成功'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
    except:
        myConfig.debug_print(traceback.format_exc())
        return myHttpResponse({'status': 0, 'data': {}, 'msg': '系统异常'})

def wx_get_apply_for_join_organization(request):
    try:
        my_token_login_request = db.query_wx_user_first('token',request.GET['token'])
        sendData = request.GET['sendData']
        myConfig.debug_print(sendData,'-----------------wx_get_apply_for_join_organization')
        sendData_json = json.loads(sendData)
        main_id = my_token_login_request['main_id']
        active_organization = my_token_login_request['active_organization']
        apply_status = sendData_json['apply_status']
        if apply_status == 'todo':
            wx_join_organization_apply_id584 = models.wx_join_organization_apply.objects(__raw__ = {
                'd.organization_main_id' : active_organization,
                'd.apply_status':apply_status
            })
        else:
            code = 4
            data = {}
            msg = '参数错误'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
        wx_join_organization_apply_id584_len = len(list(wx_join_organization_apply_id584))
        if wx_join_organization_apply_id584_len == 0:
            code = 3
            data = {}
            msg = '暂无申请'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
        else:
            organization_apply_list = wx_join_organization_apply_id584.to_json().encode('utf-8').decode('unicode_escape')
            organization_apply_list = json.loads(organization_apply_list)
            code = 1
            data = {'organization_apply_list':organization_apply_list}
            msg = '查询成功'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
    except:
        myConfig.debug_print(traceback.format_exc())
        return myHttpResponse({'status': 0, 'data': {}, 'msg': '系统异常'})

def wx_appral_apply_for_join_organization(request):
    try:
        my_token_login_request = db.query_wx_user_first('token',request.GET['token'])
        def update_wx_join_organization_apply(my_token_login_request,apply,param):
            organization_main_id = my_token_login_request['active_organization']
            apply_person_main_id = apply['d']['apply_person_main_id']
            wx_join_organization_apply662 = models.wx_join_organization_apply.objects(__raw__ = {
                'd.organization_main_id':organization_main_id,
                'd.apply_person_main_id':apply_person_main_id
            }).first()
            if wx_join_organization_apply662 == None:
                pass
            else:
                d = wx_join_organization_apply662.d
                if param == 'yes':
                    d['is_accept'] = True
                    d['apply_status'] = 'accept'
                    d['approval_person_main_id'] = my_token_login_request['main_id']
                    d['approval_time'] = tool.Time().now_time()
                    wx_join_organization_apply662.update(d=d)
                elif param == 'no':
                    d['apply_status'] = 'deny'
                    d['approval_person_main_id'] = my_token_login_request['main_id']
                    d['approval_time'] = tool.Time().now_time()
                    wx_join_organization_apply662.update(d=d)
                else:
                    pass
        sendData = request.GET['sendData']
        myConfig.debug_print(sendData,'-----------------wx_appral_apply_for_join_organization')
        sendDataJson =  json.loads(sendData)
        apply = sendDataJson['apply']
        apply_person_main_id = apply['d']['apply_person_main_id']
        param = sendDataJson['param']
        if not (my_token_login_request[2]['super_admin'] or my_token_login_request[2]['nomarl_admin']): #权限验证
            code = 4
            data = {}
            msg = '没有权限'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
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
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
        else:
            pass
        code = 0
        data = {}
        msg = '参数异常'
        res = {'status': code, 'data': data, 'msg': msg}
        return myHttpResponse(res)
    except:
        myConfig.debug_print(traceback.format_exc())
        return myHttpResponse({'status': 0, 'data': {}, 'msg': '系统异常'})

def wx_create_supplier(request):
    try:
        my_token_login_request = db.query_wx_user_first('token',request.GET['token'])
        sendData = request.GET['sendData']
        sendData_json = json.loads(sendData)
        supplier_main_id = sendData_json['supplier_main_id']
        cfuscc = sendData_json['certificate_for_uniform_social_credit_code']
        supplier_name = sendData_json['supplier_name']
        supplier_address = sendData_json['supplier_address']
        legal_person_name = sendData_json['legal_person_name']
        legal_person_mobile = sendData_json['legal_person_mobile']
        manage_person_name = sendData_json['manage_person_name']
        manage_person_mobile = sendData_json['manage_person_mobile']
        wx_supplier373 = models.wx_supplier_info.objects(__raw__ ={
            'd.certificate_for_uniform_social_credit_code':cfuscc
        }).first()
        import datetime
        if wx_supplier373 == None:
            supplier_main_id = tool.wmm_create_main_id()
            d799 = {
                'supplier_main_id':supplier_main_id,
                'certificate_for_uniform_social_credit_code':cfuscc,
                'supplier_name':supplier_name,
                'supplier_address':supplier_address,
                'super_admin_person':{
                    'main_id':my_token_login_request['main_id'],
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
                'create_person_main_id':my_token_login_request['main_id'],
            }
            models.wx_supplier_info(d=d799).save()
            q838 = models.wx_supplier_match_user.objects(__raw__ = {
                'd.supplier_main_id':supplier_main_id,
                'd.main_id':my_token_login_request['main_id'],
            }).first()
            if q838 == None:
                d = {
                    'supplier_main_id':supplier_main_id,
                    'main_id':my_token_login_request['main_id'],
                    'role':['super_admin','nomarl_admin','user'],
                    'department':'管理员',
                    'labor_contract':'合同制',
                }
                models.wx_supplier_match_user(d=d).save()
            d_wx_user = my_token_login_request
            d_wx_user['active_supplier'] = supplier_main_id #更新用户默认关联的组织
            my_token_login_request[1].update(d=d_wx_user)
            code = 1
            data = {'supplier_info':d799}
            msg = '创建成功'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
        else:
            code = 2
            data = {}
            msg = '组织已存在！'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
    except:
        myConfig.debug_print(traceback.format_exc())
        return myHttpResponse({'status': 0, 'data': {}, 'msg': '系统异常'})

def wx_create_supplier_department(request):
    try:
        my_token_login_request = db.query_wx_user_first('token',request.GET['token'])
        if not (my_token_login_request[3]['super_admin'] or my_token_login_request[3]['nomarl_admin']): #供应商权限验证
            code = 4
            data = {}
            msg = '没有权限'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
        sendData = request.GET['sendData']
        sendData_json = json.loads(sendData)
        supplier_main_id = sendData_json['supplier_main_id']
        supplier_department_name = sendData_json['supplier_department_name']
        supplier_department_address = sendData_json['supplier_department_address']
        supplier_department_manage_person_name = sendData_json['supplier_department_manage_person_name']
        supplier_department_manage_person_mobile = sendData_json['supplier_department_manage_person_mobile']
        wx_supplier373 = models.wx_supplier_department_info.objects(__raw__ ={
            'd.supplier_department_name':supplier_department_name,
            'd.supplier_main_id':supplier_main_id
        }).first()
        if wx_supplier373 == None:
            q983 = models.wx_supplier_info.objects(__raw__ = { 'd.supplier_main_id':supplier_main_id }).first()
            if q983 == None:
                code = 5
                data = {}
                msg = '没有供应商信息'
                res = {'status': code, 'data': data, 'msg': msg}
                return myHttpResponse(res)
            supplier_department_id = tool.wmm_create_main_id()
            d = {
                'supplier_main_id':supplier_main_id,
                'supplier_department_id': supplier_department_id,
                'supplier_department_name':supplier_department_name,
                'supplier_department_address':supplier_department_address,
                'super_admin_person':{
                    'main_id':my_token_login_request['main_id'],
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
                'create_person_main_id':my_token_login_request['main_id'],
            }
            models.wx_supplier_department_info(d=d).save()
            q1033 = models.wx_supplier_department_info.objects(__raw__ = {'d.supplier_main_id':supplier_main_id})
            code = 1
            data = {'supplier_department_info_list':tool.wmm_to_json(q1033) }
            msg = '创建成功'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
        else:
            code = 2
            data = {}
            msg = '已存在！'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
    except:
        myConfig.debug_print(traceback.format_exc())
        return myHttpResponse({'status': 0, 'data': {}, 'msg': '系统异常'})

def wx_get_supplierInfo_list(request):
    try:
        my_token_login_request = db.query_wx_user_first('token',request.GET['token'])
        sendData = request.GET['sendData']
        myConfig.debug_print(sendData,'-----------------wx_get_supplierInfo_list')
        sendData_json = json.loads(sendData)
        searchVal = sendData_json['searchVal']
        main_id = my_token_login_request['main_id']
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
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
        else:
            supplier_list = []
            for o in wx_supplier_match_main_id478:
                supplier_main_id = o.d['supplier_main_id']
                q_wx_supplier_info1070 = models.wx_supplier_info.objects(__raw__ = {'d.supplier_main_id':supplier_main_id}).first()
                if q_wx_supplier_info1070 == None:
                    continue
                else:
                    supplier_list.append( { 'd':q_wx_supplier_info1070.d } )
            # supplier_list = wx_supplier_match_main_id478.to_json().encode('utf-8').decode('unicode_escape')
            # supplier_list = json.loads(supplier_list)
            code = 1
            data = {'supplier_list':supplier_list}
            msg = '查询到'+str(wx_supplier_match_main_id478_len)+'个！'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
    except:
        myConfig.debug_print(traceback.format_exc())
        return myHttpResponse({'status': 0, 'data': {}, 'msg': '系统异常'})

def wx_swicth_supplier(request):
    try:
        my_token_login_request = db.query_wx_user_first('token',request.GET['token'])
        sendData = request.GET['sendData']
        myConfig.debug_print(sendData,'-----------------wx_swicth_supplier')
        sendData_json = json.loads(sendData)
        supplierInfo = sendData_json['supplierInfo']
        main_id = my_token_login_request['main_id']
        supplier_main_id = supplierInfo['d']['supplier_main_id']
        wx_supplier_match_main_id537 = models.wx_supplier_match_user.objects(__raw__ = {
            'd.supplier_main_id' : supplier_main_id,
            'd.main_id' : main_id
        }).first()
        if wx_supplier_match_main_id537 == None:
            code = 3
            data = {}
            msg = '你不属于该组织'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
        else:
            d = my_token_login_request
            d['active_supplier'] = supplier_main_id
            my_token_login_request[1].update(d=d)
            #查询供应商部门列表
            supplier_department_id_list = supplierInfo['d']['supplier_department_id_list']
            q1143 = models.wx_supplier_department_info.objects(__raw__ = {'d.supplier_main_id':supplier_main_id})
            #------------
            code = 1
            data = {'userInfo':d,'supplier_info':supplierInfo['d'],'supplier_department_info_list':tool.wmm_to_json(q1143)}
            msg = '切换成功'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
    except:
        myConfig.debug_print(traceback.format_exc())
        return myHttpResponse({'status': 0, 'data': {}, 'msg': '系统异常'})

def wx_get_my_wx_supplier_department_info_list(request):
    try:
        my_token_login_request = db.query_wx_user_first('token',request.GET['token'])
        sendData = request.GET['sendData']
        myConfig.debug_print(sendData,'-----------------wx_get_my_wx_supplier_department_info_list')
        sendData_json = json.loads(sendData)
        supplier_info = sendData_json['supplier_info']
        main_id = my_token_login_request['main_id']
        supplier_department_id_list = supplier_info['supplier_department_id_list']
        supplier_department_info_list = []
        for o in supplier_department_id_list:
            q1143 = models.wx_supplier_department_info.objects(__raw__ = {'d.supplier_department_id':o}).first()
            t1144 = q1143.to_json().encode('utf-8').decode('unicode_escape')
            supplier_department_info_list.append(json.loads(t1144))
        if supplier_department_info_list == []:
            code = 2
            data = {'supplier_department_info_list':[]}
            msg = '没有数据'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
        else:
            code = 1
            data = {'supplier_department_info_list':[]}
            msg = '成功'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
    except:
        myConfig.debug_print(traceback.format_exc())
        return myHttpResponse({'status': 0, 'data': {}, 'msg': '系统异常'})

def wx_organization_department_info_list(request):
    try:
        my_token_login_request = db.query_wx_user_first('token',request.GET['token'])
        sendData = request.GET['sendData']
        myConfig.debug_print(sendData,'-----------------wx_organization_department_info_list')
        sendData_json = json.loads(sendData)
        d973 = sendData_json['organization_info']
        main_id = my_token_login_request['main_id']
        supplier_department_id_list = d973['supplier_department_id_list']
        supplier_department_info_list = []
        for o in supplier_department_id_list:
            q1143 = models.wx_supplier_department_info.objects(__raw__ = {'d.supplier_department_id':o}).first()
            t1144 = q1143.to_json().encode('utf-8').decode('unicode_escape')
            supplier_department_info_list.append(json.loads(t1144))
        if supplier_department_info_list == []:
            code = 2
            data = {'supplier_department_info_list':[]}
            msg = '没有数据'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
        else:
            code = 1
            data = {'supplier_department_info_list':[]}
            msg = '成功'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
    except:
        myConfig.debug_print(traceback.format_exc())
        return myHttpResponse({'status': 0, 'data': {}, 'msg': '系统异常'})

def wx_create_organization_department(request):
    try:
        my_token_login_request = db.query_wx_user_first('token',request.GET['token'])
        if not (my_token_login_request[2]['super_admin'] or my_token_login_request[2]['nomarl_admin']): #组织权限验证
            code = 4
            data = {}
            msg = '没有权限'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
        sendData = request.GET['sendData']
        sendData_json = json.loads(sendData)
        organization_main_id = sendData_json['organization_main_id']
        organization_department_name = sendData_json['organization_department_name']
        organization_department_address = sendData_json['organization_department_address']
        organization_department_manage_person_name = sendData_json['organization_department_manage_person_name']
        organization_department_manage_person_mobile = sendData_json['organization_department_manage_person_mobile']
        wx_organization373 = models.wx_organization_department_info.objects(__raw__ ={
            'd.organization_department_name':organization_department_name,
            'd.organization_main_id':organization_main_id
        }).first()
        if wx_organization373 == None:
            q983 = models.wx_organization.objects(__raw__ = { 'd.organization_main_id':organization_main_id }).first()
            if q983 == None:
                code = 5
                data = {}
                msg = '没有供应商信息'
                res = {'status': code, 'data': data, 'msg': msg}
                return myHttpResponse(res)
            organization_department_id = tool.wmm_create_main_id()
            d = {
                'organization_main_id':organization_main_id,
                'organization_department_id': organization_department_id,
                'organization_department_name':organization_department_name,
                'organization_department_address':organization_department_address,
                'super_admin_person':{
                    'main_id':my_token_login_request['main_id'],
                    'name':'',
                    'moile':'',
                },
                'manage_person':{
                    'name':organization_department_manage_person_name,
                    'mobile':organization_department_manage_person_mobile
                },
                'labor_contract':[
                    {'name':'合同制'},{'name':'派遣制'},{'name':'第三方'},{'name':'实习生'},{'name':'其它'}
                ],
                'create_time':tool.Time().now_time(),
                'create_person_main_id':my_token_login_request['main_id'],
            }
            models.wx_organization_department_info(d=d).save()
            q1033 = models.wx_organization_department_info.objects(__raw__ = {'d.organization_main_id':organization_main_id})
            code = 1
            data = {'organization_department_info_list':tool.wmm_to_json(q1033) }
            msg = '创建成功'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
        else:
            code = 2
            data = {}
            msg = '已存在！'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
    except:
        myConfig.debug_print(traceback.format_exc())
        return myHttpResponse({'status': 0, 'data': {}, 'msg': '系统异常'})

def wx_search_supplier(request):
    try:
        # my_token_login_request = db.query_wx_user_first('token',request.GET['token'])
        sendData = request.GET['sendData']
        sendData_json = json.loads(sendData)
        searchVal = sendData_json['searchVal']
        wx_supplier249 = models.wx_supplier_info.objects(__raw__ = {'$or':[
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
            ]
        })
        if list(wx_supplier249) == []:
            code = 2
            data = {'supplier_list':[]}
            msg = '没有组织'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
        else:
            code = 1
            data = { 'supplier_list':tool.wmm_to_json(wx_supplier249) }
            msg = '成功'
            return myHttpResponse( {'status': code, 'data': data, 'msg': msg} )
    except:
        myConfig.debug_print(traceback.format_exc())
        return myHttpResponse({'status': 0, 'data': {}, 'msg': '系统异常'})




















































