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

class  微信预约办事申请表(Document):
    openid = StringField(default='')
    部门编号 = StringField(default='')
    部门名称 = StringField(default='')
    办事内容 = StringField(default='')
    办事日期 = StringField(default='')
    办事区间 = StringField(default='')
    其它 = DictField(default={})

class 微信预约办事内容表(Document):
    部门编号 = StringField(default='')
    部门名称 = StringField(default='')
    value = StringField(default='')
    label = StringField(default='')
    info = DictField(default={})

class  微信预约验证码表(Document):
    验证码 = StringField()
    手机号 = StringField()

class 微信预约部门表(Document):
    部门图标 = ImageField(default=open(myConfig.django_root_path+'/mysite/'+'404','rb'))
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

def 保存微信预约办事列表(部门编号,部门名称,value,label,info={}):
    qset0 = 微信预约办事内容表.objects(
        部门编号 = 部门编号,
        部门名称 = 部门名称,
        value = value,
        label = label
    ).first()
    if qset0 == None:
        微信预约办事内容表(
            部门编号 = 部门编号,
            部门名称 = 部门名称,
            value = value,
            label = label,
            info = info
        ).save()
    else:
        qset0.update(
            部门编号 = 部门编号,
            部门名称 = 部门名称,
            value = value,
            label = label,
            info = info
        )

def 导入微信预约部门表和微信预约办事内容表(path):
    微信预约部门表.objects.delete()
    微信预约办事内容表.objects.delete()
    import pandas as pd
    df = pd.read_excel(path)
    for index_main, row_main in df.iterrows():
        部门编号 = str(row_main['部门编号'])
        部门图标文件 = str(row_main['部门图标文件'])
        outfile = open(myConfig.django_root_path+'/dzzwzx/'+部门图标文件, 'rb')
        部门名称 = str(row_main['部门名称'])
        办事编号 = str(row_main['办事编号'])
        办事内容 = str(row_main['办事内容'])
        备注 = str(row_main['备注'])
        qset = 微信预约部门表.objects(部门编号=部门编号).first()
        if qset == None:
            微信预约部门表(
                部门图标 = outfile,
                部门名称 = 部门名称,
                部门编号 = 部门编号,
                部门信息 = {}
            ).save()
        else:
            qset.delete()
            微信预约部门表(
                部门图标 = outfile,
                部门名称 = 部门名称,
                部门编号 = 部门编号,
                部门信息 = {}
            ).save()
        qset0 = 微信预约办事内容表.objects(
            部门编号 = 部门编号,
            value = 办事编号
        ).first()
        if qset0 == None:
            微信预约办事内容表(
                部门编号 = 部门编号,
                部门名称 = 部门名称,
                value = 办事编号,
                label = 办事内容,
                info = {'txt':备注}
            ).save()
        else:
            qset0.update(
                部门编号 = 部门编号,
                部门名称 = 部门名称,
                value = 办事编号,
                label = 办事内容,
                info = {'txt':备注}
            )

def 设置某手机号为管理员(path):
    import pandas as pd
    df = pd.read_excel(path)
    for index_main, row_main in df.iterrows():
        手机号 = str(row_main['手机号'])
        qset0 = 微信预约用户表.objects(手机号=手机号).first()
        if qset0 == None:
            pass
        else:
            qset0.其它['权限'] = '管理员'
            qset0.update(其它= qset0.其它)
   
if __name__ == '__main__':
    设置某手机号为管理员(myConfig.django_root_path+'/dzzwzx/'+'微信预约管理员.xlsx')
    导入微信预约部门表和微信预约办事内容表(myConfig.django_root_path+'/dzzwzx/'+'微信预约部门和办事表20190929.xlsx')


