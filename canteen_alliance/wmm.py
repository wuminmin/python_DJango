from . import models, tool, wmm
import myConfig
import json
import traceback
import time
from django.http import HttpResponse, FileResponse, JsonResponse

#wx_wx_info
def query_wx_wx_info_first_by_openid_and_app_id(
    openid,
    app_id
):
    return models.wx_wx_info.objects(__raw__={'d.openid':openid,'d.app_id':app_id}).first()

def create_wx_wx_info_by_openid_and_app_id(
    main_id,
    openid,
    app_id,
    session_key,
    mobile
):
    q245 = models.wx_wx_info.objects(__raw__={'d.openid':openid,'d.app_id':app_id}).first()
    if q245 == None:
        d = {
            'main_id':main_id,
            'openid':openid,
            'app_id':app_id,
            'session_key':session_key,
            'mobile':mobile,
        }
        models.wx_wx_info(d=d).save()
        return models.wx_wx_info.objects(__raw__={'d.openid':openid}).first()
    else:
        return None

def update_wx_wx_info_by_openid_and_app_id(
    main_id,
    openid,
    app_id,
    session_key,
    mobile
):
    q245 = models.wx_wx_info.objects(__raw__={'d.openid':openid,'d.app_id':app_id}).first()
    if q245 == None:
        return None
    else:
        d = q245.d
        if not main_id == None:
            d['main_id'] = main_id
        if not session_key == None:
            d['session_key'] = session_key
        if not mobile == None:
            d['mobile'] = mobile
        q245.update(d=d)
        return models.wx_wx_info.objects(__raw__={'d.openid':openid}).first()
#--------------

#wx_user
def query_wx_user_info_first_by_token(request):
    q9 = models.wx_user.objects(__raw__={'d.token':request.GET['token']}).first()
    if q9 == None:
        return None
    else:
        return q9.d

def query_wx_user_info_first_by_main_id(
    main_id
):
    return models.wx_user.objects(__raw__={'d.main_id':main_id}).first()
    
def create_wx_user_info_by_mobile(
    mobile,
    nickname,
    portrait,
    active_organization,
    active_supplier
):
    q14 = models.wx_user.objects(__raw__={'d.mobile': mobile}).first()
    if q14 == None:
        d16 = {
            'has':True,
            'main_id': tool.wmm_create_main_id(),
            'token': tool.wmm_create_token(),
            'mobile': mobile,
            'nickname': nickname,
            'portrait': portrait,
            'active_organization': active_organization,
            'active_supplier': active_supplier
        }
        models.wx_user(d=d16).save()
        return models.wx_user.objects(__raw__={'d.mobile': mobile}).first()
    else:
        return None

def update_wx_user_by_main_id(main_id, d_key, d_value):
    q46 = models.wx_user.objects(__raw__={'d.main_id': main_id}).first()
    if q46 == None:
        return None
    else:
        d50 = q46.d
        d50[d_key] = d_value
        q46.update(d=d50)
        return d50

def update_wx_user_info_by_mobile(
    mobile,
    token,
    nickname,
    portrait,
    active_organization,
    active_supplier
):
    q14 = models.wx_user.objects(__raw__={'d.mobile': mobile}).first()
    if q14 == None:
        return None
    else:
        d = q14.d
        if not token == None:
            d['token'] = token
        if not nickname == None:
            d['nickname'] = nickname
        if not portrait == None:
            d['portrait'] = portrait
        if not active_organization == None:
            d['active_organization'] = active_organization
        if not active_supplier == None:
            d['active_supplier'] = active_supplier
        q14.update(d=d)
        return models.wx_user.objects(__raw__={'d.mobile': mobile}).first()

def create_wx_user_info_by_mobile_and_main_id(
    main_id,
    mobile,
    nickname,
    active_organization,
    active_supplier
):
    q14 = models.wx_user.objects(__raw__={'d.mobile': mobile}).first()
    if q14 == None:
        d16 = {
            'has':True,
            'main_id': main_id,
            'token': tool.wmm_create_token(),
            'mobile': mobile,
            'nickname': nickname,
            'portrait': 'https://dss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=1676131907,2302520392&fm=111&gp=0.jpg',
            'active_organization': active_organization,
            'active_supplier': active_supplier
        }
        models.wx_user(d=d16).save()
        return models.wx_user.objects(__raw__={'d.mobile': mobile}).first()
    else:
        return None
#--------------

#organization_department_info
def query_organization_department_info_list_for_vuex(
    organization_main_id
):
    q10 = models.wx_organization_department_info.objects(
        __raw__={'d.organization_main_id': organization_main_id})
    return tool.wmm_to_json(q10)

def query_organization_department_info_list_by_organization_main_id(
    organization_main_id
):
    q193 = models.wx_organization_department_info.objects(__raw__={'d.organization_main_id':organization_main_id})
    if list(q193) == []:
        return []
    else:
        return tool.wmm_to_json(q193)
#-----------------

#wx_organization_match_user
def create_wx_organization_match_user_by_main_id_and_organization_main_id(
    main_id,
    organization_main_id,
    role,
    labor_attribute
):
    q29 = models.wx_organization_match_user.objects(__raw__={
        'd.main_id': main_id, 'd.organization_main_id': organization_main_id}).first()
    if q29 == None:
        d31 = {
            'main_id': main_id,
            'organization_main_id': organization_main_id,
            'role': models.wx_organization_match_user_d['role'][role],
            'labor_attribute': models.wx_organization_match_user_d['labor_attribute'][labor_attribute]
        }
        models.wx_organization_match_user(d=d31).save()
        return  models.wx_organization_match_user.objects(__raw__={
            'd.main_id': main_id, 'd.organization_main_id': organization_main_id}).first()
    else:
        return None
#-------------------

#wx_organization
def creater_wx_organization_by_certificate_for_uniform_social_credit_code(
    certificate_for_uniform_social_credit_code,
    organization_name,
    organization_address,
    create_person_main_id
):
    wx_organization373 = models.wx_organization.objects(__raw__={
        'd.certificate_for_uniform_social_credit_code': certificate_for_uniform_social_credit_code
    }).first()
    if wx_organization373 == None:
        d494 = {
            'has': True,
            'organization_main_id': tool.wmm_create_main_id(),
            'certificate_for_uniform_social_credit_code': certificate_for_uniform_social_credit_code,
            'organization_name': organization_name,
            'organization_address': organization_address,
            'create_time': tool.wmm_get_now_time(),
            'create_person_main_id': create_person_main_id
        }
        models.wx_organization(d=d494).save()
        return models.wx_organization.objects(__raw__={
            'd.certificate_for_uniform_social_credit_code': certificate_for_uniform_social_credit_code
        }).first()
    else:
        return None

def query_organization_info_first_by_organization_main_id(
    organization_main_id
):
    return models.wx_organization.objects(__raw__ = {'d.organization_main_id':organization_main_id}).first()
#--------------------

#wx_supplier_info
def query_wx_supplier_info_first_by_supplier_main_id(
    supplier_main_id
):
    return  models.wx_supplier_info.objects(__raw__ = {'d.supplier_main_id':supplier_main_id}).first()
#----------------