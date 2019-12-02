import sys, os
root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_path)

import myConfig
from django.db import models

# Create your models here.
from mongoengine import *

# 数据库连接
import sys
import os
root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_path)

connect(db=myConfig.db, host=myConfig.host, port=myConfig.port,username=myConfig.username, password=myConfig.password)

react_url = 'https://oa.wuminmin.top/'

ban_kuai_lan_mu_dict = {
    '营销活动':['已发布','兑现中','已归档'],
    '新闻中心':['人大要闻','通知公告','工作动态'],
    '依法履职':['立法工作','决定决议','任职任免','监督工作'],
    '代表工作':['代表信息','代表风采','代表信箱','议案建议']
}

ban_kuai1_lan_mu1 = '已发布'
ban_kuai1_lan_mu2 = '兑现中'
ban_kuai1_lan_mu3 = '已归档'
import datetime
class ji_li_zhu_shou_article(Document):
    article = StringField(default='')
    lan_mu = StringField(default='')
    tittle = StringField(default='')
    my_time = StringField(default='')
    my_date = DateTimeField(default = datetime.datetime.now() )
    my_month = StringField(default= '')
    author = StringField(default='')
    other = DictField(default={})
    usernamelist = ListField(default=[])
    lan_mu1list =  ListField(default=[])
    lan_mu2list =  ListField(default=[])
    lan_mu3list =  ListField(default=[])
    userrolelist = ListField(default=[])

mystate1 = '待确认'
mystate2 = '已确认'
mystate3 = '已超时'
mystate4 = '已归档'
class ji_li_zhu_shou_dui_xian_qing_dan(Document):
    mainid = StringField(default='')
    tittle = StringField(default='')
    sellid = StringField(default='')
    money = FloatField(default=0)
    mydate = StringField(default='')
    nowdate = DateTimeField(default= datetime.datetime.now())
    bankid = StringField(default='')
    mystate = StringField(default=mystate1)

userrole1 = '销售员'
userrole2 = '管理员'
userrole3 = '公司领导'
userrole4 = '县区主任'
userrole5 = '营业部主任'
userrole6 = '系统管理员'
class ji_li_zhu_shou_userinfo(Document):
    my_date = DateTimeField(default = datetime.datetime.now() )
    username = StringField(default='')
    userpwd = StringField(default='')
    userphone = StringField(default='')
    userrole = StringField(default='')
    usertoken = StringField(default='')
    mainid = StringField(default='')
    lan_mu1 = StringField(default='')
    lan_mu2 = StringField(default='')
    lan_mu3 = StringField(default='')

class ji_li_zhu_shou_image(Document):
    col_id = StringField()
    col_image = ImageField()

def save_image(id,path):
    outfile = open(path, 'rb')
    qset = ji_li_zhu_shou_image.objects(col_id=id).first()
    if qset == None:
        ji_li_zhu_shou_image(
            col_id = id,
            col_image = outfile
        ).save()
    else:
        qset.delete()
        ji_li_zhu_shou_image(
            col_id = id,
            col_image = outfile
        ).save()


if __name__ == "__main__":
    # qset1 = qyrd_article_col.objects(lan_mu='通知公告').count()
    # print(qset1)
    # save_image('修身福地灵秀青阳','./qyrd/banner.jpg')

    ji_li_zhu_shou_userinfo(
        username = '吴敏民',
        userphone = '13355661100',
        userrole = '营销活动管理员',
    ).save()