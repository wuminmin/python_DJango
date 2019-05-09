from mongoengine import *

# 数据库连接
import myConfig

connect(db=myConfig.db, host=myConfig.host, port=myConfig.port, username=myConfig.username, password=myConfig.password)
全体奖 = '章总发红包'
一等奖 = '第一轮抽奖'
二等奖 = '第二轮抽奖'
三等奖 = '第三轮抽奖'
四等奖 = '第四轮抽奖'
没中奖 = '没中奖'
未开始 = '未开始'
抽奖开始 = '正在抽奖'
抽奖结束 = '抽奖结束'
中奖人数字典 = {全体奖:1000,一等奖:100,二等奖:100,三等奖:100,四等奖:100}
中奖金额字典 = {全体奖:10,一等奖:20,二等奖:20,三等奖:20,四等奖:40}


class 抽奖主界面表(Document):
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

class 抽奖用户表(Document):
    openid = StringField()
    手机号 = StringField()
    formId_dict = DictField(default={})

class 抽奖登录状态表(Document):
    session_key = StringField()
    openid = StringField()

class 抽奖验证码表(Document):
    验证码 = StringField()
    手机号 = StringField()

class 抽奖开关(Document):
    开关 = BooleanField()

class 抽奖按钮状态(Document):
    lei_xing = StringField()
    jie_guo = StringField()
    ti_shi = StringField()
    btn_list = ListField()

class 抽奖状态表(Document):
    lei_xing = StringField()
    flex_list = ListField()

class 抽奖全体奖状态表(Document):
    quan_ti_jiang = DictField(default={})

class 抽奖参与者(Document):
    手机号 = StringField()
    姓名 = StringField()
    三级部门 = StringField()
    中奖类型 = StringField(default=没中奖)

class 采集模版表(Document):
    手机号 = StringField()
    当前时间 = StringField()
    建筑物编号 = StringField()
    采集内容 = DictField()

class 采集分工表(Document):
    手机号 = StringField()
    修改记录 = DictField(default={})
    建筑物编号 = StringField()
    分工 = DictField()

建筑物主键分隔符 = '_'
可录入 = 'placeholder_red'
新录入 = 'placeholder_blue'
已录入 = 'placeholder_green'
分页 = 10
class 采集录入分工表(Document):
    责任人 = StringField()
    录入分工 = ListField()