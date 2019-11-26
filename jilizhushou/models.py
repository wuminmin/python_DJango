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

import datetime
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

def save_image(id,path):
    outfile = open(path, 'rb')
    qset = qyrd_image_col.objects(col_id=id).first()
    if qset == None:
        qyrd_image_col(
            col_id = id,
            col_image = outfile
        ).save()
    else:
        qset.delete()
        qyrd_image_col(
            col_id = id,
            col_image = outfile
        ).save()


if __name__ == "__main__":
    # qset1 = qyrd_article_col.objects(type='通知公告').count()
    # print(qset1)
    save_image('修身福地灵秀青阳','./qyrd/banner.jpg')