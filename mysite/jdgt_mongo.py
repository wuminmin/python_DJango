from mongoengine import *

# 数据库连接
import myConfig

connect(db=myConfig.db, host=myConfig.host, port=myConfig.port, username=myConfig.username, password=myConfig.password)

部门主任存草稿 = '部门主任存草稿'
客户经理未核实 = '客户经理未核实'
客户经理已核实 = '客户经理已核实'
客户经理不通过 = '客户经理不通过'
政企校园完成打分 = '政企校园完成打分'
党群部审核通过 = '党群部审核通过'
党群部审核不通过 = '党群部审核不通过'
path = myConfig.django_root_path + '/' + 'mysite' + '/' + '404.png'
outfile = open(path, 'rb')
巡检机房 = '巡检机房'
拜访客户 = '拜访客户'
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

class 结对共拓用户表(Document):
    openid = StringField()
    手机号 = StringField()

class 结对共拓登录状态表(Document):
    session_key = StringField()
    openid = StringField()

class 结对共拓验证码表(Document):
    验证码 = StringField()
    手机号 = StringField()

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
    部门主任手机号 = StringField(default='')
    客户经理手机号 = StringField(default='')
    客户编码 = StringField(default='')
    状态 = StringField(default=部门主任存草稿)
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
