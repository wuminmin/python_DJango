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

wx_wx_info_d = {
    'openid':'',
    'app_id':'',
    'session_key':'',
    'mobile':'',
    "main_id":''
}
class wx_openid(Document): #微信信息表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})
    o = DictField(default={})

wx_user_d = {
    'has':True,
    'main_id':'',
    'token':'',
    'mobile':'',
    'nickname':'',
    'portrait':'http://img1.imgtn.bdimg.com/it/u=1266808576,2151703311&fm=26&gp=0.jpg',
}
class wx_user(Document):#用户信息表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})
    o = DictField(default={})

class wx_sms(Document): #短信验证码表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})
    o = DictField(default={})

class wx_organization(Document): #组织表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})
    o = DictField(default={})

# class wx_organization_department_info(Document): #组织部门表
#     meta = {"db_alias": canteen_alliance}
#     d = DictField(default={})

# class wx_join_organization_apply(Document): #加入组织申请表
#     meta = {"db_alias": canteen_alliance}
#     d = DictField(default={})


wx_organization_match_user_d = {
    'organization_main_id':'',
    'user_main_id':'',
    'role':['超级管理员','普通管理员','普通用户'],
    'labor_attribute':['合同制','派遣制','第三方','其它'],
    'department':['生产部门','销售部门','其它部门']
}
class wx_organization_match_user(Document): #组织和个人关系表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})
    o = DictField(default={})



class wx_supplier(Document): #供应商信息
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})
    o = DictField(default={})

wx_supplier_match_user_d = {
    'main_id':'',
    'supplier_main_id':'',
   'role':['超级管理员','普通管理员','普通用户'],
   'shop':['餐厅1','餐厅2'],
    'labor_attribute':['合同制','派遣制','第三方','其它'],
}
class wx_supplier_match_user(Document): #供应商和个人关系表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})
    o = DictField(default={})

# class wx_organization_match_supplier(Document): #组织和供应商关联
#     meta = {"db_alias": canteen_alliance}
#     d = DictField(default={})

# class wx_supplier_department_info(Document): #供应商部门表
#     meta = {"db_alias": canteen_alliance}
#     d = DictField(default={})

# class wx_goods_info(Document): #供应商某部门货物信息
#     meta = {"db_alias": canteen_alliance}
#     d = DictField(default={})





