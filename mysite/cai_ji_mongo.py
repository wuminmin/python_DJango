from mongoengine import *

# 数据库连接
import myConfig

connect(db=myConfig.db, host=myConfig.host, port=myConfig.port, username=myConfig.username, password=myConfig.password)


class  采集主界面表(Document):
    手机号 = StringField()
    描述 = StringField()
    创建时间 = StringField()
    主页标题 = StringField()
    主页描述 = StringField()
    验证码标题 = StringField()
    验证码描述 = StringField()
    二级部门 = StringField()
    三级部门 = StringField()
    四级部门 = StringField()
    姓名 = StringField()
    主界内容 = ListField()

class  采集用户表(Document):
    openid = StringField()
    手机号 = StringField()
    formId_dict = DictField(default={})

class  采集登录状态表(Document):
    session_key = StringField()
    openid = StringField()

class  采集验证码表(Document):
    验证码 = StringField()
    手机号 = StringField()
