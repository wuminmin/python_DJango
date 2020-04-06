from mongoengine import *

# 数据库连接
import myConfig
# disconnect(alias='default')
connect(alias='canteen_alias',db=myConfig.canteen_db, host=myConfig.canteen_host, port=myConfig.canteen_port, username=myConfig.canteen_username, password=myConfig.canteen_password)

class 订餐导入时间戳表(Document):
    flag = StringField(default='')
    isOk = BooleanField(default=None)
    eLog = DictField(default={'log':''})


池州电信分公司 = '池州市分公司'
青阳电信分公司 = '青阳分公司'
池州烟草公司 = '池州烟草公司'
#食堂订餐123--------------------------------------
class 订餐主界面表(Document):
    meta = {"db_alias": "canteen_alias"}
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
    meta = {"db_alias": "canteen_alias"}
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

产品名称列表 = ['包子','早餐','中餐','晚餐']
产品列表 = [
    # {
    #     '名称':'包子',
    #     '预定数量条件':['无', '预定1份','预定2份','预定3份','预定4份','预定5份'],
    #     '取消提前秒':7200,
    #     '价格':100,
    #     '就餐时间':'18:00:00'
    # },
    {
        '名称':'早餐',
        '预定数量条件':['无', '预定1份','预定2份','预定3份','预定4份','预定5份'],
        '取消提前秒':7200,
        '价格':1200,
        '就餐时间':'18:00:00'
    },
    {
        '名称':'中餐',
        '预定数量条件':['无', '预定1份','预定2份','预定3份','预定4份','预定5份'],
        '取消提前秒':7200,
        '价格':1200,
        '就餐时间':'18:00:00'
    },
    {
        '名称':'晚餐',
        '预定数量条件':['无', '预定1份','预定2份','预定3份','预定4份','预定5份'],
        '取消提前秒':7200,
        '价格':1200,
        '就餐时间':'18:00:00'
    }
]

管理员手机号清单 = ['13355661100','18956600118']
产品名称列表字典 = {
    'wx10547371f9547456':['包子','早餐','中餐','晚餐'],
    'wx32c0a3c1a3bfa81d':['肉包子','菜包子','馒头','早餐','中餐','晚餐'],
}
产品全局字典 = {
    'wx10547371f9547456':{
        '取消次数上限':3,
    },
    'wx32c0a3c1a3bfa81d':{
        '取消次数上限':3,
    },
}
产品列表字典 = {
    'wx10547371f9547456':[
        {
            '名称':'早餐',
            '预定数量条件':['无', '预定1份','预定2份','预定3份','预定4份','预定5份'],
            '取消提前秒':5400,
            '价格':1200,
            '就餐时间':'08:00:00'
        },
        {
            '名称':'中餐',
            '预定数量条件':['无', '预定1份','预定2份','预定3份','预定4份','预定5份'],
            '取消提前秒':5400,
            '价格':1200,
            '就餐时间':'12:00:00'
        },
        {
            '名称':'晚餐',
            '预定数量条件':['无', '预定1份','预定2份','预定3份','预定4份','预定5份'],
            '取消提前秒':5400,
            '价格':1200,
            '就餐时间':'18:00:00'
        }
    ],
    'wx32c0a3c1a3bfa81d':[
        {
            '名称':'肉包子',
            '预定数量条件':['无', '预定1份','预定2份','预定3份','预定4份','预定5份','预定6份','预定7份','预定8份','预定9份','预定10份','预定11份','预定12份'],
            '取消提前秒':7200,
            '价格':100,
            '就餐时间':'18:00:00'
        },
        {
            '名称':'菜包子',
            '预定数量条件':['无', '预定1份','预定2份','预定3份','预定4份','预定5份','预定6份','预定7份','预定8份','预定9份','预定10份','预定11份','预定12份'],
            '取消提前秒':7200,
            '价格':100,
            '就餐时间':'18:00:00'
        },
        {
            '名称':'馒头',
            '预定数量条件':['无', '预定1份','预定2份','预定3份','预定4份','预定5份','预定6份','预定7份','预定8份','预定9份','预定10份','预定11份','预定12份'],
            '取消提前秒':7200,
            '价格':100,
            '就餐时间':'18:00:00'
        },
        {
            '名称':'早餐',
            '预定数量条件':['无', '预定1份'],
            '取消提前秒':7200,
            '价格':400,
            '就餐时间':'08:00:00'
        },
        {
            '名称':'中餐',
            '预定数量条件':['无', '预定1份'],
            '取消提前秒':7200,
            '价格':800,
            '就餐时间':'12:00:00'
        },
        {
            '名称':'晚餐',
            '预定数量条件':['无', '预定1份'],
            '取消提前秒':72000,
            '价格':700,
            '就餐时间':'18:00:00'
        }
    ],
}



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
    meta = {"db_alias": "canteen_alias"}
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
    产品 = DictField(default={})
    

class 订餐结果临时表(Document):
    meta = {"db_alias": "canteen_alias"}
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
    产品 = DictField(default={})


class 订餐种类表(Document):
    meta = {"db_alias": "canteen_alias"}
    名称 = StringField(default='')
    订餐时间 = StringField(default='')
    取消时间 = StringField(default='')
    签到状态 = StringField(default='没吃')


class ding_can_chinaums_pay_order_res_col(Document):
    meta = {"db_alias": "canteen_alias"}
    json_res = DictField(default={})
    openid = StringField(default='')

class 订餐钱包表(Document):
    meta = {"db_alias": "canteen_alias"}
    openid = StringField(default='')
    已充值 = IntField(default=0)
    已消费 = IntField(default=0)
    预消费 = IntField(default=0)

class 订餐钱包充值表(Document):
    meta = {"db_alias": "canteen_alias"}
    手机号 = StringField(default='')
    充值金额 = IntField(default=0)
    充值时间 = StringField(default='')
    充值成功标识 = BooleanField(default=False)
    备注 = StringField(default='')

class 订餐用户表(Document):
    meta = {"db_alias": "canteen_alias"}
    openid = StringField()
    手机号 = StringField()
    钱包金额 = FloatField(default=0)
    

class 订餐登录状态表(Document):
    meta = {"db_alias": "canteen_alias"}
    session_key = StringField()
    openid = StringField()

class 订餐验证码表(Document):
    meta = {"db_alias": "canteen_alias"}
    验证码 = StringField()
    手机号 = StringField()

class 订餐核销码表(Document):
    meta = {"db_alias": "canteen_alias"}
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
    meta = {"db_alias": "canteen_alias"}
    二级部门 = StringField(default='')
    三级部门列表 = ListField(default=[])

class 订餐统计结果(Document):
    meta = {"db_alias": "canteen_alias"}
    日期 = StringField()
    子菜单page_name = StringField()
    子菜单page_desc = StringField()
    订餐结果 = DictField()

class 订餐提醒短信锁(Document):
    meta = {"db_alias": "canteen_alias"}
    日期 = StringField()
    短信锁 = BooleanField(default=False)

菜单分隔符 = '_'
无评价 = 'placeholder_grey'
差评 = 'placeholder_red'
中评 = 'placeholder_blue'
好评 = 'placeholder_green'
订餐菜单分页 = 10
class 订餐菜单表(Document):
    meta = {"db_alias": "canteen_alias"}
    # 订餐日期 = StringField()
    # 订餐类型 = StringField()
    食堂名称 = StringField()
    菜单列表 = ListField()

class 订餐菜单模版表(Document):
    meta = {"db_alias": "canteen_alias"}
    订餐日期 = StringField()
    食堂名称 = StringField()
    订餐类型 = StringField()
    菜谱名称 = StringField()
    菜谱备注 = DictField(default={})
    手机号 = StringField()
    上传时间 = StringField()

class 订餐菜单评价表(Document):
    meta = {"db_alias": "canteen_alias"}
    订餐日期 = StringField()
    食堂名称 = StringField()
    订餐类型 = StringField()
    手机号 = StringField()
    评价时间 = StringField()
    菜谱名称 = StringField()
    评价结果 = StringField()
    评价备注 = DictField(default={})

class 订餐评论表(Document):
    meta = {"db_alias": "canteen_alias"}
    手机号 = StringField()
    姓名 = StringField(default='')
    二级部门 = StringField(default='')
    三级部门 = StringField(default='')
    四级部门 = StringField(default='')
    创建时间 = StringField()
    评论内容 = StringField()
    评论图片 = ImageField()

class 订餐取消计数表(Document):
    meta = {"db_alias": "canteen_alias"}
    d = DictField(default={})

