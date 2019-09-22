from django.db import models

# Create your models here.

from mongoengine import *

# 数据库连接
import sys, os
root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_path)
import myConfig

connect(db=myConfig.db, host=myConfig.host, port=myConfig.port, username=myConfig.username, password=myConfig.password)

react_url = 'https://oa.wuminmin.top/'

class  微信预约用户表(Document):
    openid = StringField(default='')
    access_token = StringField(default='')
    refresh_token = StringField(default='')
    手机号 = StringField(default='')
    其它 = DictField(default={})

class  微信预约验证码表(Document):
    验证码 = StringField()
    手机号 = StringField()

class 微信预约部门表(Document):
    部门图标 = ImageField(default=open(myConfig.django_root_path+'/'+'mysite/'+'404.png','rb'))
    部门名称 = StringField(default='')
    部门编号 = StringField(default='')
    部门信息 = DictField(default={})

def 保存微信预约部门表(path,部门名称,部门编号,部门信息):
    outfile = open(path, 'rb')
    qset = 微信预约部门表.objects(部门编号=部门编号).first()
    if qset == None:
        微信预约部门表(
            部门图标 = outfile,
            部门名称=部门名称,
            部门编号 = 部门编号,
            部门信息=部门信息
        ).save()
    else:
        qset.delete()
        微信预约部门表(
            部门图标 = outfile,
            部门名称=部门名称,
            部门编号 = 部门编号,
            部门信息=部门信息
        ).save()

if __name__ == '__main__':
    保存微信预约部门表(myConfig.django_root_path+'/'+'dzzwzx/images/'+'公安盾牌.png','公安局','1',{})
    保存微信预约部门表(myConfig.django_root_path+'/'+'dzzwzx/images/'+'医疗.png','卫计委','2',{})
    保存微信预约部门表(myConfig.django_root_path+'/'+'dzzwzx/images/'+'司法公证.png','司法局','3',{})
    保存微信预约部门表(myConfig.django_root_path+'/'+'dzzwzx/images/'+'宜兴房产.png','房管局','4',{})
    保存微信预约部门表(myConfig.django_root_path+'/'+'dzzwzx/images/'+'教育.png','教育局','5',{})


