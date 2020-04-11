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

class wx_join_organization_apply(Document): #加入组织申请表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})

class wx_organization_match_main_id(Document): #组织和个人关系表
    meta = {"db_alias": canteen_alliance}
    d = DictField(default={})







