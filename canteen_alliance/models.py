from mongoengine import *

# 数据库连接
import myConfig
# disconnect(alias='default')
canteen_alliance = 'canteen_alliance'
connect(
    alias='canteen_alliance',
    db=myConfig.canteen_alliance_db, 
    host=myConfig.host, 
    port=myConfig.port, 
    username=myConfig.canteen_alliance_username, 
    password=myConfig.canteen_alliance_password
)

d_wx_wx_info = {
    "openid": "oixmv4qKdbfmgEy97swKuXLAXyf4",
    "app_id": "wx32c0a3c1a3bfa81d",
    "session_key": "XNwoP4v/d+kxevqQBUfr7Q==",
    "main_id": "5e92d90c2cafa21786033439"
}
class wx_wx_info(Document):
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

d_wx_user = {
    "main_id": "5e92d90c2cafa21786033439",
    "token": "7bde7729d7a0e8e4be66e482dfc057be",
    "mobile": "13355661100",
    "nickname": "吴敏民",
    "portrait": "https://dss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=1676131907,2302520392&fm=111&gp=0.jpg",
    "active_organization": "",
}
class wx_user(Document):#用户表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

class wx_sms(Document): #短信验证码表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

d_wx_organization =  {
    "organization_main_id":"5e926d8266063def8dfce70f",
    "certificate_for_uniform_social_credit_code": "9111000071093019X7",
    "organization_name": "中国电信股份有限公司池州分公司",
    "organization_address": "池州市长江路",
    "super_admin_person": {
        "main_id": "5e91b5ad587861042b4df41c",
        "name": "",
        "moile": ""
    },
    "legal_person": {
        "name": "测试",
        "mobile": "123456"
    },
    "manage_person": {
        "name": "吴敏民",
        "mobile": "13355661100"
    },
    "department": [{
        "name": "管理员"
    }, {
        "name": "管控部门"
    }, {
        "name": "销售部门"
    }, {
        "name": "生产部门"
    }],
    "labor_contract": [{
        "name": "合同制"
    }, {
        "name": "派遣制"
    }, {
        "name": "第三方"
    }, {
        "name": "实习生"
    }, {
        "name": "其它"
    }],
    "create_time": {
        "$date": {
            "$numberLong": "1586683394752"
        }
    },
    "create_person_main_id": "5e91b5ad587861042b4df41c"
}
class wx_organization(Document): #组织表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

d_wx_join_organization_apply =  {
    "certificate_for_uniform_social_credit_code": "9111000071093019X7",
    "apply_person_main_id": "5e91b5ad587861042b4df41c",
    "apply_person_name": "吴敏民",
    "apply_for_department": {
        "name": "管理员"
    },
    "apply_for_labor_contract": {
        "name": "合同制"
    },
    "apply_time": {
        "$date": {
            "$numberLong": "1586694467101"
        }
    },
        "apply_status":"todo",  #todo accept  deny
    "is_accept": False,
    "approval_person_main_id": "",
    "approval_time": ""
}
class wx_join_organization_apply(Document): #加入组织申请表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

d_wx_organization_match_user =  {
    "main_id": "5e91b5ad587861042b4df41c",
    "role": ["super_admin"], # super_admin 超级管理员 normal_admin 普通管理员 user 普通用户
    "department": "管理员",
    "labor_contract": "合同制"
}
class wx_organization_match_user(Document): #组织和个人关系表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

d_wx_supplier_match_user =  {
    "main_id": "5e91b5ad587861042b4df41c",
    "role": ["super_admin"], # super_admin 超级管理员 normal_admin 普通管理员 user 普通用户
    "department": "管理员",
    "labor_contract": "合同制"
}
class wx_supplier_match_user(Document): #供应商和个人关系表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

d_wx_supplier_info = {
    'supplier_main_id':'',
    'certificate_for_uniform_social_credit_code':'9111000071093019X7',
    'supplier_department_id_list':[],
    'supplier_address':'池州市长江路',
    'create_time':'',
    'create_person_main_id':'',
}
class wx_supplier_info(Document): #供应商信息
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

d_wx_organization_match_supplier = {
    'organization_main_id':'',
    'supplier_main_id':'',
    'supplier_department_id':''
}
class wx_organization_match_supplier(Document): #组织和供应商关联
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

d_wx_supplier_department_info = {
    'supplier_department_id':'021RIb6j1Zxcwt0EoK2j1dYf6j1RIb6r',
    'supplier_department_name':'',
    'supplier_department_address':''
}
class wx_supplier_department_info(Document): #供应商部门表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

d_wx_goods_list = {
    'supplier_department_id':'021RIb6j1Zxcwt0EoK2j1dYf6j1RIb6r',
    'goods_list':[
        {
            'image': "https://dss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=220119721,2872000268&fm=26&gp=0.jpg",
            'image2': "http://pic.rmb.bdstatic.com/819a044daa66718c2c40a48c1ba971e6.jpeg",
            'image3': "http://img001.hc360.cn/y5/M00/1B/45/wKhQUVYFE0uEZ7zVAAAAAMj3H1w418.jpg",
            'title': "肉包子",
            'price': 100,
            'sales': 0,
        }
    ]
}
class wx_goods_info(Document): #供应商某部门货物信息
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})





