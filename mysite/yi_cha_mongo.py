from mongoengine import *

# 数据库连接
import myConfig

connect(db=myConfig.db, host=myConfig.host, port=myConfig.port, username=myConfig.username, password=myConfig.password)


#易查199----------------------
class 易查主界面表(Document):
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

class 易查套餐内容(Document):
    描述 = StringField(default='下载成功')
    page_name = StringField(default='')
    page_desc = StringField(default='')
    toast_data = StringField(default='')

class 易查政策宣传主界面(Document):
    # 手机号 = StringField()
    描述 = StringField(default='下载成功')
    创建时间 = StringField(default='')
    主页标题 = StringField(default='政策宣传')
    主页描述 = StringField(default='')
    验证码标题 = StringField(default='')
    验证码描述 = StringField(default='')
    # 二级部门 = StringField()
    # 三级部门 = StringField()
    # 四级部门 = StringField()
    # 姓名 = StringField()
    page_name = StringField(default='')
    page_desc = StringField(default='')
    主界内容 = ListField(default=[])

class 易查试卷结果表(Document):
    手机号 = StringField()
    正确题数 = IntField()
    考试大类 = StringField()
    考试小类 = StringField()
    交卷时间 = StringField()
    考试结果 = ListField()
    测试 = IntField()

class 易查试卷答案表(Document):
    考试大类 = StringField()
    考试小类 = StringField()
    创建时间 = StringField()
    考试答案 = ListField()

考试未开始 = '考试未开始'
考试进行中 = '考试进行中'
考试已交卷 = '考试已交卷'
考试已结束 = '考试已结束'
class 易查试卷模版表(Document):
    主菜单name = StringField()
    主菜单id = StringField()
    子菜单page_name = StringField()
    子菜单page_desc = StringField()
    子菜单url = StringField()
    考试开始时间 = StringField()
    考试结束时间 = StringField()
    考试时长 = IntField()
    创建时间 = StringField()
    考试状态 = StringField(default=考试未开始)
    试卷内容 = ListField()

class 易查用户表(Document):
    openid = StringField()
    手机号 = StringField()

class 易查登录状态表(Document):
    session_key = StringField()
    openid = StringField()

class 易查验证码表(Document):
    验证码 = StringField()
    手机号 = StringField()
