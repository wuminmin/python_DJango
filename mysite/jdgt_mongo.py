from mongoengine import *

# 数据库连接
import myConfig

connect(db=myConfig.db, host=myConfig.host, port=myConfig.port, username=myConfig.username, password=myConfig.password)


# 食堂订餐123--------------------------------------
class 结对共拓主界面表(Document):
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


class 结对共拓食堂模版表(Document):
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
中餐统计 = '中餐统计'
晚餐统计 = '晚餐统计'


class 结对共拓结果表(Document):
    手机号 = StringField()
    主菜单name = StringField()
    子菜单page_name = StringField()
    子菜单page_desc = StringField()
    用餐日期 = StringField()
    早餐食堂就餐预订数 = IntField()
    早餐食堂就餐签到 = StringField(default='')
    早餐订餐时间 = StringField()
    早餐取消时间 = StringField()
    早餐食堂外带预订数 = IntField(default=0)
    中餐食堂就餐预订数 = IntField()
    中餐食堂就餐签到 = StringField(default='')
    中餐订餐时间 = StringField()
    中餐取消时间 = StringField(default='')
    中餐食堂外带预订数 = IntField(default=0)
    晚餐食堂就餐预订数 = IntField()
    晚餐食堂就餐签到 = StringField(default='')
    晚餐订餐时间 = StringField()
    晚餐取消时间 = StringField(default='')
    晚餐食堂外带预订数 = IntField(default=0)


class 结对共拓用户表(Document):
    openid = StringField()
    手机号 = StringField()


class 结对共拓登录状态表(Document):
    session_key = StringField()
    openid = StringField()


class 结对共拓验证码表(Document):
    验证码 = StringField()
    手机号 = StringField()


class 结对共拓核销码表(Document):
    主菜单name = StringField()
    子菜单page_name = StringField()
    子菜单page_desc = StringField()
    核销码 = StringField(default='123456')
    姓名 = StringField(default='')
    手机号 = StringField(default='')
    二级部门 = StringField(default='')
    三级部门 = StringField(default='')
    四级部门 = StringField(default='')


class 结对共拓部门表(Document):
    二级部门 = StringField(default='')
    三级部门列表 = ListField(default=[])




class 结对共拓提醒短信锁(Document):
    日期 = StringField()
    短信锁 = BooleanField(default=False)


class 结对共拓菜单评价表(Document):
    订餐日期 = StringField()
    食堂名称 = StringField()
    订餐类型 = StringField()
    手机号 = StringField()
    评价时间 = StringField()
    菜谱名称 = StringField()
    评价结果 = StringField()
    评价备注 = DictField(default={})


class 结对共拓客户经理表(Document):
    客户经理工号 = StringField()
    姓名 = StringField()
    手机号 = StringField()
    部门 = StringField()


class 结对共拓单位名称(Document):
    名称 = StringField()
    客户编码 = StringField()
    客户经理 = StringField()
    客户经理工号 = StringField()


class 结对共拓客户经理上传单位信息(Document):
    单位名称 = StringField()
    客户编码 = StringField()
    客户经理 = StringField()
    手机号码 = StringField()


class 结对共拓部门主任客户经理对应表(Document):
    客户经理手机号码 = StringField()
    部门主任手机号码 = StringField()


客户经理未核实 = '客户经理未核实'
客户经理已核实 = '客户经理已核实'
客户经理不通过 = '客户经理不通过'
政企校园完成打分 = '政企校园完成打分'
党群部审核通过 = '党群部审核通过'
党群部审核不通过 = '党群部审核不通过'
path = myConfig.django_root_path + '/' + 'mysite' + '/' + '404.png'
outfile = open(path, 'rb')
class 结对共拓部门主任走访客户结果表(Document):
    走访日期 = StringField(default='')
    部门主任姓名 = StringField(default='')
    客户经理姓名 = StringField(default='')
    单位名称 = StringField(default='')
    走访主题 = StringField(default='')
    走访对象 = DictField(default={'走访对象': ''})
    商机信息 = DictField(default={'商机信息': ''})
    竞争信息 = DictField(default={'竞争信息': ''})
    服务问题 = DictField(default={'服务问题': ''})
    是否有服务问题 = BooleanField(default=True)
    是否提交云方案 = BooleanField(default=True)
    状态 = StringField(default=客户经理未核实)
    得分 = DictField(default={'积分': '0'})
    大门照片 = ImageField(default=outfile)

class 结对共拓部门主任机房巡检结果表(Document):
    走访日期 = StringField(default='')
    部门主任姓名 = StringField(default='')
    客户经理姓名 = StringField(default='')
    单位名称 = StringField(default='')
    状态 = StringField(default=客户经理未核实)
    得分 = DictField(default={'积分': '0'})
    main_list = ListField(default=[])

class 结对共拓部门主任机房巡检图片表(Document):
    file_url = StringField(default='')
    file_image = ImageField(default=outfile)

if __name__ == '__main__':
    # 结对共拓客户经理表(
    # 客户经理工号='测试1',
    # 姓名 = 'fjg',
    # 手机号 = '18956662004',
    # 部门 = '也管'
    # ).save()

    # 结对共拓部门主任客户经理对应表(
    #     客户经理手机号码='13355661100',
    #     部门主任手机号码='15305668602'
    # ).save()

    结对共拓客户经理上传单位信息(
        单位名称='池州电信',
        客户编码 = '客户编码',
        客户经理 = '吴敏民',
        手机号码 = '13355661100'
    ).save()
