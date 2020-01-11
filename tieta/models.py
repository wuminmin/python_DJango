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

def send_mail_tie_ta(mail_addr):
    qset1 = 铁塔资料表.objects
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    l5 = []
    l6 = []
    l7 = []
    l8 = []
    l9 = []
    l10 = []
    l11 = []
    l12 = []
    l13 = []
    l14 = []
    l15 = []
    l16 = []
    l17 = []
    l18 = []
    l19 = []
    l20 = []
    l21 = []
    l22 = []
    l23 = []
    l24 = []
    l25 = []
    l26 = []
    l27 = []
    l28 = []
    def get_value(one,key):
        if key in one.资料:
            return str( one.资料[key] )
        else:
            return ''
    for one in qset1:
        l1.append(get_value(one,'姓名'))
        l2.append(get_value(one,'手机号'))
        l3.append(get_value(one,'身份证号码'))
        l4.append(get_value(one,'铁塔站址编码'))
        l5.append(get_value(one,'站名'))
        l6.append(get_value(one,'经度'))
        l7.append(get_value(one,'纬度'))
        l8.append(get_value(one,'L1_8G挂高'))
        l9.append(get_value(one,'L1_8G天线数'))
        l10.append(get_value(one,'L1_8G机械下倾角'))
        l11.append(get_value(one,'L1_8G方位角'))
        l12.append(get_value(one,'L800M挂高'))
        l13.append(get_value(one,'L800M天线数'))
        l14.append(get_value(one,'L800M机械下倾角'))
        l15.append(get_value(one,'L800M方位角'))
        l16.append(get_value(one,'C网挂高'))
        l17.append(get_value(one,'C网天线数'))
        l18.append(get_value(one,'C网方位角'))
        l19.append(get_value(one,'C网机械下倾角'))
        l20.append(get_value(one,'塔型'))
        l21.append(get_value(one,'L1_8G天线平台'))
        l22.append(get_value(one,'L800M天线平台'))
        l23.append(get_value(one,'C网天线平台'))
        l24.append(get_value(one,'合路天线情况'))
        l25.append(get_value(one,'铁塔共享运营商'))
        l26.append(get_value(one,'配套共享运营商'))
        l27.append(get_value(one,'机房或机柜是否有BBU'))
        l28.append(get_value(one,'电流分割比'))
    import pandas
    jie_guo_df = pandas.DataFrame({
        '姓名': l1,
        '手机号': l2,
        '身份证号码': l3,
        '铁塔站址编码': l4,
        '站名': l5,
        '经度': l6,
        '纬度': l7,
        'L1_8G挂高': l8,
        'L1_8G天线数':l9,
        'L1_8G机械下倾角':l10,
        'L1_8G方位角':l11,
        'L800M挂高':l12,
        'L800M天线数':l13,
        'L800M机械下倾角':l14,
        'L800M方位角':l15,
        'C网挂高':l16,
        'C网天线数':l17,
        'C网方位角':l18,
        'C网机械下倾角':l19,
        '塔型':l20,
        'L1_8G天线平台':l21,
        'L800M天线平台':l22,
        'C网天线平台':l23,
        '合路天线情况':l24,
        '铁塔共享运营商':l25,
        '配套共享运营商':l26,
        '机房或机柜是否有BBU':l27,
        '电流分割比':l28
    })
    import time
    创建时间 = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    file_name = '铁塔资料' + 创建时间 + '.xls'
    邮箱 = mail_addr
    文件名 = file_name
    姓名 = '管理员'
    import io
    s_buf = io.StringIO()
    # jie_guo_df.to_excel(s_buf)
    jie_guo_df.to_excel(file_name, encoding='gbk')
    附件 =  open(file_name,'rb').read()
    from mysite.schedule_tool import 发邮件
    发邮件(邮箱, 文件名, 姓名,附件)
if __name__ == '__main__':
    send_mail_tie_ta('15305666012@189.cn')
    
