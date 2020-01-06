from django.db import models
from mongoengine import *

# 数据库连接
import sys, os
root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_path)
import myConfig

connect(db=myConfig.db, host=myConfig.host, port=myConfig.port, username=myConfig.username, password=myConfig.password)

react_url = 'https://oa.wuminmin.top/'

class  铁塔用户表(Document):
    openid = StringField(default='')
    access_token = StringField(default='')
    refresh_token = StringField(default='')
    手机号 = StringField(default='')
    其它 = DictField(default={})

class  铁塔验证码表(Document):
    验证码 = StringField()
    手机号 = StringField()

class 铁塔资料表(Document):
    上传时间 = DateTimeField(default=None)
    openid = StringField(default='')
    手机号 = StringField(default='')
    资料 = DictField(default={})

# class  微信投票用户表(Document):
#     openid = StringField(default='')
#     access_token = StringField(default='')
#     refresh_token = StringField(default='')
#     手机号 = StringField(default='')
#     其它 = DictField(default={})

# class tou_piao_image_col(Document):
#     wxyl_id = StringField()
#     wxyl_image = ImageField()

# def save_image(id,path):
#     outfile = open(path, 'rb')
#     qset = tou_piao_image_col.objects(wxyl_id=id).first()
#     if qset == None:
#         tou_piao_image_col(
#             wxyl_id = id,
#             wxyl_image = outfile
#         ).save()
#     else:
#         qset.delete()
#         tou_piao_image_col(
#             wxyl_id = id,
#             wxyl_image = outfile
#         ).save()

if __name__ == '__main__':
    pass
