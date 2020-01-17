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
import datetime
root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_path)

# disconnenect()
connect(db=myConfig.db, host=myConfig.host, port=myConfig.port,username=myConfig.username, password=myConfig.password)
react_url = 'https://oa.wuminmin.top/'

ban_kuai_lan_mu_dict = {
    '首页':['首页'],
    '人大概况':['人大简介','组织机构','组成人员','委室职责','换届选举'],
    '新闻中心':['人大要闻','通知公告','工作动态'],
    '依法履职':['决定决议','任职任免','监督工作','法律法规'],
    '会议之窗':['人民代表大会会议','常委会会议','主任会议','代表联系群众','代表邮箱'],
    '一府一委两院':['人民政府','监察委员会','人民法院','人民检察院'],
    '乡镇人大':['蓉城镇','朱备镇','杨田镇','陵阳镇','新河镇','木镇镇','丁桥镇','乔木乡','酉华镇','庙前镇','杜村乡'],
    '代表工作':['代表信息','代表风采','议案建议']
}

class qyrd_article_col(Document):
    article = StringField(default='')
    type = StringField(default='')
    tittle = StringField(default='')
    my_time = StringField(default='')
    my_date = DateTimeField(default = datetime.datetime.now() )
    my_month = StringField(default= '')
    author = StringField(default='')
    other = DictField(default={})

class qyrd_image_col(Document):
    col_id = StringField()
    col_image = ImageField()

class qyrd_userinfo(Document):
    my_date = DateTimeField(default = datetime.datetime.now() )
    username = StringField(default='')
    userpwd = StringField(default='')
    userphone = StringField(default='')
    userrole = StringField(default='')
    usertoken = StringField(default='')
    mainid = StringField(default='')
    type1 = StringField(default='')
    type2 = StringField(default='')
    type3 = StringField(default='')


if __name__ == "__main__":
    qyrd_userinfo(
        username = '吴敏民',
        usertoken = '123456',
        userphone = '13355661100'
    ).save()