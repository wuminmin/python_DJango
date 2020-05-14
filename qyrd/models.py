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

qyrd_usertoken = 'LhPAxsEJm3LihsU0siCH5Q=='

ban_kuai_lan_mu_dict = {
    '首页':['网站首页'],
    '首页图片':['图片新闻'],
    '首页滚动':['滚动图片'],
    '走进部门':['通知公告'],
    '今日石台':['领导活动','热点新闻','挂职动态','"疫"线党红旗'],
    '本部动态':['工作动态','组工简报','专题活动','权限组工系统主题教育'],
    '党建工作':['农村社区党建','机关国企学校党建','非公党建'],
    '干部人才':['教育培训','工作动态','政策法规'],
    '基层动态':['乡镇传真','部门传真','抓党建促脱贫','扫黑除恶'],
    '选派选聘':['选派动态','选聘动态','交流园地'],
    '远教电教':['基层动态','双创双争','视频课件','抗洪救灾'],
    '网上党校':['视频课件','党的知识','理论学习','学习贯彻党的十八届五中全会精神','抗洪救灾','学习贯彻党的十八届六中全会精神','学习贯彻党的十九大精神','不忘初心牢记使命'],
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