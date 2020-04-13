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

class wx_wx_info(Document): #微信信息表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

class wx_user(Document):#用户信息表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

class wx_sms(Document): #短信验证码表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

class wx_organization(Document): #组织表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

class wx_organization_department_info(Document): #组织部门表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

class wx_join_organization_apply(Document): #加入组织申请表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

class wx_organization_match_user(Document): #组织和个人关系表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

class wx_supplier_match_user(Document): #供应商和个人关系表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

class wx_supplier_info(Document): #供应商信息
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

class wx_organization_match_supplier(Document): #组织和供应商关联
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

class wx_supplier_department_info(Document): #供应商部门表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

class wx_goods_info(Document): #供应商某部门货物信息
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})





