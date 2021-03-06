from mongoengine import *

# 数据库连接
import myConfig

connect(db=myConfig.db, host=myConfig.host, port=myConfig.port, username=myConfig.username, password=myConfig.password)

class 订餐导入时间戳表(Document):
    flag = StringField(default='')
    isOk = BooleanField(default=None)
    eLog = DictField(default={'log':''})

池州电信分公司 = '池州市分公司'
青阳电信分公司 = '青阳分公司'
池州烟草公司 = '池州烟草公司'
#食堂订餐123--------------------------------------
class 订餐主界面表(Document):
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

青阳食堂 = '青阳食堂'
class 订餐食堂模版表(Document):
    主菜单name = StringField()
    主菜单id = StringField()
    子菜单page_name = StringField()
    子菜单page_desc = StringField()
    子菜单url = StringField()
    食堂地址 = StringField()
    早餐价格 = StringField()
    中餐价格 = StringField()
    晚餐价格 = StringField()
    早餐就餐时间 = StringField()
    中餐就餐时间 = StringField()
    晚餐就餐时间 = StringField()
    预定早餐提前秒 = IntField()
    预定中餐提前秒 = IntField()
    预定晚餐提前秒 = IntField()
    取消早餐提前秒 = IntField()
    取消中餐提前秒 = IntField()
    取消晚餐提前秒 = IntField()
    创建时间 = StringField()

没吃 = '没吃'
吃过 = '吃过'
取消 = '取消'
早餐统计 = '早餐统计'
中餐统计 = '中餐统计'
晚餐统计 = '晚餐统计'
早餐外带统计 = '早餐外带统计'
中餐外带统计 = '中餐外带统计'
晚餐外带统计 = '晚餐外带统计'
烟草公司每月外带上限次数 = 8
class 订餐结果表(Document):
    手机号 = StringField(default='')
    主菜单name = StringField(default='')
    子菜单page_name = StringField(default='')
    子菜单page_desc = StringField(default='')
    用餐日期 = StringField(default='')
    早餐食堂就餐预订数 = IntField(default=0)
    早餐食堂就餐签到 = StringField(default=没吃)
    早餐订餐时间 = StringField(default='')
    早餐取消时间 = StringField(default='')
    早餐食堂外带预订数 = IntField(default=0)
    中餐食堂就餐预订数 = IntField(default=0)
    中餐食堂就餐签到 = StringField(default=没吃)
    中餐订餐时间 = StringField(default='')
    中餐取消时间 = StringField(default='')
    中餐食堂外带预订数 = IntField(default=0)
    晚餐食堂就餐预订数 = IntField(default=0)
    晚餐食堂就餐签到 = StringField(default=没吃)
    晚餐订餐时间 = StringField(default='')
    晚餐取消时间 = StringField(default='')
    晚餐食堂外带预订数 = IntField(default=0)

class 订餐用户表(Document):
    openid = StringField()
    手机号 = StringField()

class 订餐登录状态表(Document):
    session_key = StringField()
    openid = StringField()

class 订餐验证码表(Document):
    验证码 = StringField()
    手机号 = StringField()

class 订餐核销码表(Document):
    主菜单name = StringField()
    子菜单page_name = StringField()
    子菜单page_desc = StringField()
    核销码 = StringField(default='123456')
    姓名 = StringField(default='')
    手机号 = StringField(default='')
    二级部门 = StringField(default='')
    三级部门 = StringField(default='')
    四级部门 = StringField(default='')

class 订餐部门表(Document):
    二级部门 = StringField(default='')
    三级部门列表 = ListField(default=[])

class 订餐统计结果(Document):
    日期 = StringField()
    子菜单page_name = StringField()
    子菜单page_desc = StringField()
    订餐结果 = DictField()

class 订餐提醒短信锁(Document):
    日期 = StringField()
    短信锁 = BooleanField(default=False)

菜单分隔符 = '_'
无评价 = 'placeholder_grey'
差评 = 'placeholder_red'
中评 = 'placeholder_blue'
好评 = 'placeholder_green'
订餐菜单分页 = 10
class 订餐菜单表(Document):
    # 订餐日期 = StringField()
    # 订餐类型 = StringField()
    食堂名称 = StringField()
    菜单列表 = ListField()

class 订餐菜单模版表(Document):
    订餐日期 = StringField()
    食堂名称 = StringField()
    订餐类型 = StringField()
    菜谱名称 = StringField()
    菜谱备注 = DictField(default={})
    手机号 = StringField()
    上传时间 = StringField()

class 订餐菜单评价表(Document):
    订餐日期 = StringField()
    食堂名称 = StringField()
    订餐类型 = StringField()
    手机号 = StringField()
    评价时间 = StringField()
    菜谱名称 = StringField()
    评价结果 = StringField()
    评价备注 = DictField(default={})

class 订餐评论表(Document):
    手机号 = StringField()
    姓名 = StringField(default='')
    二级部门 = StringField(default='')
    三级部门 = StringField(default='')
    四级部门 = StringField(default='')
    创建时间 = StringField()
    评论内容 = StringField()
    评论图片 = ImageField()