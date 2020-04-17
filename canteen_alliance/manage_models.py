from mongoengine import *

# 数据库连接
import myConfig
# disconnect(alias='default')
connect(
    alias='canteen_alliance',
    db=myConfig.canteen_alliance_db, 
    host=myConfig.host, 
    port=myConfig.port, 
    username=myConfig.canteen_alliance_username, 
    password=myConfig.canteen_alliance_password
)

class my_user(Document):#用户表
    meta = {"db_alias": "canteen_alliance"}
    d = DictField(default={})
