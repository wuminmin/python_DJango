from . import models, tool
import myConfig
import json
import traceback
import time

#wx_user
def query_wx_user_first(key,value):
    try:
        q = models.wx_user.objects(__raw__={'d.'+key:value}).first()
        return q
    except:
        print(traceback.format_exc())
        return None

def create_wx_user_by_mobile(mobile,d):
    tool.debug_print(mobile,d)
    portrait = 'http://img1.imgtn.bdimg.com/it/u=1266808576,2151703311&fm=26&gp=0.jpg'
    if 'nickname' in d:
        nickname = d['nickname']
    if 'portrait' in d:
        portrait = d['portrait']
    if query_wx_user_first('mobile',mobile) == None:
        d2 = {
            'has':True,
            'main_id':tool.wmm_create_main_id(),
            'token':tool.wmm_create_token(),
            'mobile':mobile,
            'nickname':nickname,
            'portrait':portrait,
            # 'portrait':'http://img1.imgtn.bdimg.com/it/u=1266808576,2151703311&fm=26&gp=0.jpg',
        }
        models.wx_user(d=d2).save()
        return query_wx_user_first('mobile',mobile)
    else:
        return None

def update_wx_user_by_mobile(mobile,d):
    nickname = None
    portrait = None
    if 'nickname' in d:
        nickname = d['nickname']
    if 'portrait' in d:
        portrait = d['portrait']
    q = query_wx_user_first('mobile',mobile)
    if not q == None:
        d = q.d 
        if not nickname == None:
            d['nickname'] = nickname
        if not portrait == None:
            d['portrait'] = portrait
        q.update(d=d)
        return True
    else:
        return False

def delete_wx_user_first(key,value):
    q = query_wx_user_first(key,value)
    if not q == None:
        q.delete()
        return True
    else:
        return False

#wx_sms
def query_wx_sms_first(key,value):
    try:
        q = models.wx_sms.objects(__raw__={'d.'+key:value}).first()
        return q
    except:
        print(traceback.format_exc())
        return None

def query_wx_sms_first2(k1,v1,k2,v2):
    try:
        q = models.wx_sms.objects(__raw__={'d.'+k1:v1,'d.'+k2:v2}).first()
        return q
    except:
        print(traceback.format_exc())
        return None

def create_wx_sms_by_mobile(mobile,password):
    if query_wx_sms_first('mobile',mobile) == None:
        d = {
            'mobile':mobile,
            'password':password,
        }
        models.wx_sms(d=d).save()
        return query_wx_sms_first('mobile',mobile)
    else:
        return None

def update_wx_sms_by_mobile(mobile,password):
    q = query_wx_sms_first('mobile',mobile)
    if not q == None:
        d = q.d 
        if not password == None:
            d['password'] = password
        q.update(d=d)
        return True
    else:
        return False

def delete_wx_sms_first(key,value):
    q = query_wx_sms_first(key,value)
    if not q == None:
        q.delete()
        return True
    else:
        return False

#wx_openid
def query_wx_openid_first(key,value):
    try:
        q = models.wx_openid.objects(__raw__={'d.'+key:value}).first()
        return q
    except:
        print(traceback.format_exc())
        return None

def query_wx_openid_first2(key,value,key1,value1):
    try:
        q = models.wx_openid.objects(__raw__={'d.'+key:value,'d.'+key1:value1}).first()
        return q
    except:
        print(traceback.format_exc())
        return None

def create_wx_openid_by_mobile(mobile,openid,app_id,session_key,d):
    if query_wx_openid_first('mobile',mobile) == None:
        d = {
            'main_id':tool.wmm_create_main_id(),
            'mobile':mobile,
            'openid':openid,
            'app_id':app_id,
            'session_key':session_key,
        }
        models.wx_openid(d=d).save()
        return query_wx_openid_first('mobile',mobile)
    else:
        return None

def update_wx_openid_by_mobile(mobile,openid,app_id,session_key,d):
    q = query_wx_openid_first('mobile',mobile)
    if not q == None:
        d = q.d 
        if not openid == None:
            d['openid'] = openid
        if not openid == None:
            d['app_id'] = app_id
        if not openid == None:
            d['session_key'] = session_key
        q.update(d=d)
        return True
    else:
        return False

def delete_wx_openid_first(key,value):
    q = query_wx_openid_first(key,value)
    if not q == None:
        q.delete()
        return True
    else:
        return False

#wx_organization
def query_wx_organization_first(key,value):
    try:
        q = models.wx_organization.objects(__raw__={'d.'+key:value}).first()
        return q
    except:
        print(traceback.format_exc())
        return None

def create_wx_organization_by_cfuscc(cfuscc,d):
    name = None
    address = None
    department = ['销售部门','生产部门','管理部门']
    labor_attribute = ['合同制','派遣制','第三方','其它']
    create_person_main_id = None
    if 'name' in d:
        name = d['name']
    if 'address' in d:
        address = d['address']
    if 'create_person_main_id' in d:
        create_person_main_id = d['create_person_main_id']
    if query_wx_organization_first('certificate_for_uniform_social_credit_code',cfuscc) == None:
        d2 = {
            'has':True,
            'main_id':tool.wmm_create_main_id(),
            'certificate_for_uniform_social_credit_code':cfuscc,
            'name':name,
            'address':address,
            'department':department,
            'labor_attribute':labor_attribute,
            'create_time':tool.wmm_get_now_time,
            'create_person_main_id':create_person_main_id,
            # 'portrait':'http://img1.imgtn.bdimg.com/it/u=1266808576,2151703311&fm=26&gp=0.jpg',
        }
        models.wx_organization(d=d2).save()
        return query_wx_organization_first('mobile',mobile)
    else:
        return None

def update_wx_organization_by_mobile(cfuscc,d):
    name = None
    address = None
    department = []
    labor_attribute = []
    if 'name' in d:
        name = d['name']
    if 'address' in d:
        address = d['address']
    if 'department' in d:
        department = d['department']
    if 'labor_attribute' in d:
        labor_attribute = d['labor_attribute']
    q = query_wx_organization_first('certificate_for_uniform_social_credit_code',cfuscc)
    if not q == None:
        d2 = q.d 
        if not name == None:
            d2['name'] = name
        if not address == None:
            d2['address'] = address
        if not department == None:
            d2['department'] = department
        if not labor_attribute == None:
            d2['labor_attribute'] = labor_attribute
        q.update(d=d2)
        return True
    else:
        return False

def delete_wx_organization_first(key,value):
    q = query_wx_organization_first(key,value)
    if not q == None:
        q.delete()
        return True
    else:
        return False



#wx_organization_match_user
def query_wx_organization_match_user_first(key,value):
    try:
        q = models.wx_organization.objects(__raw__={'d.'+key:value}).first()
        return q
    except:
        print(traceback.format_exc())
        return None

def query_wx_organization_match_user_first2(key,value,key1,value1):
    try:
        q = models.wx_organization.objects(__raw__={'d.'+key:value,'d.'+key1:value1}).first()
        return q
    except:
        print(traceback.format_exc())
        return None

def query_wx_organization_match_user_list2(k1,v1,k2,v2):
    try:
        q = models.wx_organization_match_user.objects(__raw__={'d.'+k1:v1,'d.'+k2:v2})
        if list(q) == []:
            return []
        else:
            return tool.qset_to_json(q)
    except:
        print(traceback.format_exc())
        return []

def query_wx_organization_match_user_first3(k1,v1,k2,v2,k3,v3):
    try:
        q = models.wx_organization_match_user.objects(__raw__={
            'd.'+k1:v1,'d.'+k2:v2,'d.'+k3:v3
        }).first()
        return q
    except:
        print(traceback.format_exc())
        return None

def create_wx_organization_match_user(
    organization_main_id,
    user_main_id,
    d
):
    role = None
    labor_attribute = None
    department = None
    if 'role' in d:
        role = d['role']
    if 'labor_attribute' in d:
        labor_attribute = d['labor_attribute']
    if 'department' in d:
        department = d['department']
    if query_wx_organization_match_user_first2(
        'organization_main_id',organization_main_id,
        'user_main_id',user_main_id
    ) == None:
        d2 = {
            'main_id':tool.wmm_create_main_id(),
            'organization_main_id':organization_main_id,
            'user_main_id':user_main_id,
            'role':role,
            'labor_attribute':labor_attribute,
            'department':department,
            'is_default_organization':False,
        }
        models.wx_organization_match_user(d=d2).save()
        q = query_wx_organization_match_user_first2(
            'organization_main_id',organization_main_id,
            'user_main_id',user_main_id
        )
        return q
    else:
        return None

def update_wx_organization_match_user(organization_main_id,user_main_id,d):
    role = None
    department = None
    labor_attribute = None
    is_default_organization = None
    if 'role' in d:
        role = d['role']
    if 'department' in d:
        department = d['department']
    if 'labor_attribute' in d:
        labor_attribute = d['labor_attribute']
    if 'is_default_organization' in d:
        is_default_organization = d['is_default_organization']
    q = query_wx_organization_match_user_first2(
        'organization_main_id',organization_main_id,
        'user_main_id',user_main_id
    )
    if not q == None:
        d2 = q.d 
        if not role == None:
            d2['role'] = role
        if not department == None:
            d2['department'] = department
        if not labor_attribute == None:
            d2['labor_attribute'] = labor_attribute
        if not is_default_organization == None:
            d2['is_default_organization'] = is_default_organization
        q.update(d=d)
        return True
    else:
        return False

def delete_wx_organization_match_user_first2(
   key,value,key1,value1
):
    q = query_wx_organization_match_user_first2(key,value,key1,value1)
    if not q == None:
        q.delete()
        return True
    else:
        return False



#wx_supplier
def query_wx_supplier_first(key,value):
    try:
        q = models.wx_supplier.objects(__raw__={'d.'+key:value}).first()
        return q
    except:
        print(traceback.format_exc())
        return None

def create_wx_supplier_by_cfuscc(cfuscc,d):
    name = None
    address = None
    department = ['销售部门','生产部门','管理部门']
    labor_attribute = ['合同制','派遣制','第三方','其它']
    create_person_main_id = None
    if 'name' in d:
        name = d['name']
    if 'address' in d:
        address = d['address']
    if 'create_person_main_id' in d:
        create_person_main_id = d['create_person_main_id']
    if query_wx_supplier_first('certificate_for_uniform_social_credit_code',cfuscc) == None:
        d2 = {
            'has':True,
            'main_id':tool.wmm_create_main_id(),
            'certificate_for_uniform_social_credit_code':cfuscc,
            'name':name,
            'address':address,
            'department':department,
            'labor_attribute':labor_attribute,
            'create_time':tool.wmm_get_now_time,
            'create_person_main_id':create_person_main_id,
            # 'portrait':'http://img1.imgtn.bdimg.com/it/u=1266808576,2151703311&fm=26&gp=0.jpg',
        }
        models.wx_supplier(d=d2).save()
        return query_wx_supplier_first('mobile',mobile)
    else:
        return None

def update_wx_supplier_by_mobile(cfuscc,d):
    name = None
    address = None
    department = []
    labor_attribute = []
    if 'name' in d:
        name = d['name']
    if 'address' in d:
        address = d['address']
    if 'department' in d:
        department = d['department']
    if 'labor_attribute' in d:
        labor_attribute = d['labor_attribute']
    q = query_wx_supplier_first('certificate_for_uniform_social_credit_code',cfuscc)
    if not q == None:
        d2 = q.d 
        if not name == None:
            d2['name'] = name
        if not address == None:
            d2['address'] = address
        if not department == None:
            d2['department'] = department
        if not labor_attribute == None:
            d2['labor_attribute'] = labor_attribute
        q.update(d=d2)
        return True
    else:
        return False

def delete_wx_supplier_first(key,value):
    q = query_wx_supplier_first(key,value)
    if not q == None:
        q.delete()
        return True
    else:
        return False



#wx_supplier_match_user
def query_wx_supplier_match_user_first(key,value):
    try:
        q = models.wx_supplier_match_user.objects(__raw__={'d.'+key:value}).first()
        return q
    except:
        print(traceback.format_exc())
        return None

def query_wx_supplier_match_user_first2(key,value,key1,value1):
    try:
        q = models.wx_supplier_match_user.objects(__raw__={'d.'+key:value,'d.'+key1:value1}).first()
        return q
    except:
        print(traceback.format_exc())
        return None

def query_wx_supplier_match_user_list2(k1,v1,k2,v2):
    try:
        q = models.wx_supplier_match_user.objects(__raw__={'d.'+k1:v1,'d.'+k2:v2})
        if list(q) == []:
            return []
        else:
            return tool.qset_to_json(q)
    except:
        print(traceback.format_exc())
        return []

def query_wx_supplier_match_user_first3(k1,v1,k2,v2,k3,v3):
    try:
        q = models.wx_supplier_match_user.objects(__raw__={
            'd.'+k1:v1,'d.'+k2:v2,'d.'+k3:v3
        }).first()
        return q
    except:
        print(traceback.format_exc())
        return None

def create_wx_supplier_match_user(
    organization_main_id,
    user_main_id,
    d
):
    role = None
    labor_attribute = None
    department = None
    if 'role' in d:
        role = d['role']
    if 'labor_attribute' in d:
        labor_attribute = d['labor_attribute']
    if 'department' in d:
        department = d['department']
    if query_wx_supplier_match_user_first2(
        'organization_main_id',organization_main_id,
        'user_main_id',user_main_id
    ) == None:
        d2 = {
            'main_id':tool.wmm_create_main_id(),
            'organization_main_id':organization_main_id,
            'user_main_id':user_main_id,
            'role':role,
            'labor_attribute':labor_attribute,
            'department':department,
            'is_default_organization':False,
        }
        models.wx_supplier_match_user(d=d2).save()
        q = query_wx_supplier_match_user_first2(
            'organization_main_id',organization_main_id,
            'user_main_id',user_main_id
        )
        return q
    else:
        return None

def update_wx_supplier_match_user(organization_main_id,user_main_id,d):
    role = None
    department = None
    labor_attribute = None
    is_default_organization = None
    if 'role' in d:
        role = d['role']
    if 'department' in d:
        department = d['department']
    if 'labor_attribute' in d:
        labor_attribute = d['labor_attribute']
    if 'is_default_organization' in d:
        is_default_organization = d['is_default_organization']
    q = query_wx_supplier_match_user_first2(
        'organization_main_id',organization_main_id,
        'user_main_id',user_main_id
    )
    if not q == None:
        d2 = q.d 
        if not role == None:
            d2['role'] = role
        if not department == None:
            d2['department'] = department
        if not labor_attribute == None:
            d2['labor_attribute'] = labor_attribute
        if not is_default_organization == None:
            d2['is_default_organization'] = is_default_organization
        q.update(d=d)
        return True
    else:
        return False

def delete_wx_supplier_match_user_first2(
   key,value,key1,value1
):
    q = query_wx_supplier_match_user_first2(key,value,key1,value1)
    if not q == None:
        q.delete()
        return True
    else:
        return False




