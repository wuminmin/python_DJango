from mongoengine import *

# 数据库连接
import myConfig
# disconnect(alias='default')
connect(alias='canteen_alias',db=myConfig.canteen_db, host=myConfig.canteen_host, port=myConfig.canteen_port, username=myConfig.canteen_username, password=myConfig.canteen_password)

class MyUsers(Document):#用户表
    d = DictField(default={})
