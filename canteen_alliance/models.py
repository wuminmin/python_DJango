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

class wx_user(Document):#用户表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

class wx_sms(Document): #短信验证码表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

class wx_organization(Document): #组织表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

# /** 
# * Paste one or more documents here
# */
# {
#     "d": {
#         "certificate_for_uniform_social_credit_code": "9111000071093019X7",
#         "apply_person_main_id": "5e91b5ad587861042b4df41c",
#         "apply_person_name": "吴敏民",
#         "apply_for_department": {
#             "name": "管理员"
#         },
#         "apply_for_labor_contract": {
#             "name": "合同制"
#         },
#         "apply_time": {
#             "$date": {
#                 "$numberLong": "1586694467101"
#             }
#         },
#           "apply_status":"todo",  #todo accept  deny
#         "is_accept": false,
#         "approval_person_main_id": "",
#         "approval_time": ""
#     }
# }
class wx_join_organization_apply(Document): #加入组织申请表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

# super_admin = False  超级管理员
# normal_admin = False 普通管理员
# user = False 普通用户
# /** 
# * Paste one or more documents here
# */
# {
#     "d": {
#         "certificate_for_uniform_social_credit_code": "9111000071093019X7",
#         "main_id": "5e91b5ad587861042b4df41c",
#         "role": ["super_admin"],
#         "department": "管理员",
#         "labor_contract": "合同制"
#     }
# }
class wx_organization_match_main_id(Document): #组织和个人关系表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

d_wx_supplier_info = {
    'certificate_for_uniform_social_credit_code':'9111000071093019X7',
    'supplier_department_name':'电信食堂',
    'supplier_department_id':'021RIb6j1Zxcwt0EoK2j1dYf6j1RIb6r',
    'supplier_address':'池州市长江路',
    'create_time':'',
    'create_person_main_id':'',
}
class wx_supplier_info(Document): #供应商信息
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

class wx_organization_match_supplier_(Document): #组织和供应商关联
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
class wx_goods_list(Document): #供应商某部门货物信息
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})





