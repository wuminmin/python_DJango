from mongoengine import *

# 数据库连接
import myConfig

connect(db=myConfig.db, host=myConfig.host, port=myConfig.port, username=myConfig.username, password=myConfig.password)

class 销售主界面表(Document):
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

class 销售用户表(Document):
    openid = StringField()
    手机号 = StringField()
    formId_dict = DictField(default={})

class 销售登录状态表(Document):
    session_key = StringField()
    openid = StringField()

class 销售验证码表(Document):
    验证码 = StringField()
    手机号 = StringField()

class 销售开关(Document):
    开关 = BooleanField()

可出售 = 'placeholder_red'
已登记 = 'placeholder_blue'
已出售 = 'placeholder_green'
门牌号分隔符 = '_'
class 销售楼宇表(Document):
    手机号列表 = ListField()
    小区名称 = StringField()
    小区编号 = StringField()
    楼宇名称 = StringField()
    楼宇编号 = StringField()
    楼宇详情列表 = ListField()

class 销售房屋信息表(Document):
    门牌编号 = StringField()
    创建时间 = StringField()
    房屋信息 = DictField()
    销售状态 = StringField()
    图片路径 = StringField(default='')
