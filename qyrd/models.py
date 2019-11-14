import myConfig
from django.db import models

# Create your models here.
from mongoengine import *

# 数据库连接
import sys
import os
root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_path)

connect(db=myConfig.db, host=myConfig.host, port=myConfig.port,
        username=myConfig.username, password=myConfig.password)

react_url = 'https://oa.wuminmin.top/'


class 青阳人大人大要闻(Document):
    日期 = StringField(default='')
    标题 = StringField(default='')
    文章 = StringField(default='')
    手机号 = StringField(default='')
    其它 = DictField(default={})


class 青阳人大通知公告(Document):
    日期 = StringField(default='')
    标题 = StringField(default='')
    文章 = StringField(default='')
    手机号 = StringField(default='')
    其它 = DictField(default={})


def 导入青阳人大人大要闻(path):
    青阳人大人大要闻.objects.delete()
    import pandas as pd
    df = pd.read_excel(path)
    for index_main, row_main in df.iterrows():
        标题 = str(row_main['标题'])
        日期 = str(row_main['日期'])
        文章 = str(row_main['文章'])
        手机号 = str(row_main['手机号'])
        其它 = {}
        qset = 青阳人大人大要闻.objects(标题=标题).first()
        if qset == None:
            青阳人大人大要闻(
                标题=标题,
                日期=日期,
                文章=文章,
                手机号=手机号,
                其它=其它
            ).save()
        else:
            qset.delete()
            青阳人大人大要闻(
                标题=标题,
                日期=日期,
                文章=文章,
                手机号=手机号,
                其它=其它
            ).save()

class qyrd_image_col(Document):
    col_id = StringField()
    col_image = ImageField()

def save_image(id,path):
    outfile = open(path, 'rb')
    qset = qyrd_image_col.objects(wxyl_id=id).first()
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
    导入青阳人大人大要闻(myConfig.django_root_path+'/qyrd/'+'导入青阳人大人大要闻.xlsx')
