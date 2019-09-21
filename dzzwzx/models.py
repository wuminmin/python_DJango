from django.db import models

# Create your models here.

from mongoengine import *

# 数据库连接
import myConfig

connect(db=myConfig.db, host=myConfig.host, port=myConfig.port, username=myConfig.username, password=myConfig.password)

react_url = 'https://oa.wuminmin.top/'

class  微信预约用户表(Document):
    openid = StringField()
    手机号 = StringField()

class  微信预约验证码表(Document):
    验证码 = StringField()
    手机号 = StringField()
