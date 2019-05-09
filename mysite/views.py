import datetime
import json
import traceback
import uuid

import pandas
import pytz
import requests
import time
from django.http import HttpResponse
from django.shortcuts import render_to_response

from myConfig import appid, secret, grant_type, sign_name, template_code, django_root_path
import sys

from mysite.yi_cha_mongo import 易查试卷模版表


class Logger(object):
    def __init__(self, fileN="Default.log"):
        self.terminal = sys.stdout
        self.log = open(fileN, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
sys.stdout = Logger(django_root_path + '/' + 'out.txt')  # 保存到D盘



def index(request):
    try:
        print(request)
        return render_to_response("login.html")
    except:
        print(traceback.format_exc())
        return HttpResponse('500')

def 检查经纬度(request):
    return render_to_response("form_file_upload.html")

def 给定经纬度计算两点之间距离(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）
    from math import radians, cos, sin, asin, sqrt
    # 将十进制度数转化为弧度
    # math.degrees(x):为弧度转换为角度
    # math.radians(x):为角度转换为弧度
    if lon1 == None or lat1 == None:
        return 20000
    else:
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine公式
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin( dlat /2 ) **2 + cos(lat1) * cos(lat2) * sin( dlon /2 ) **2
        c = 2 * asin(sqrt(a))
        r = 6371 # 地球平均半径，单位为公里
        return c * r*1000

if __name__ == '__main__':
    df_main = pandas.read_excel(r'LTE扇区导出_20190118_090201_80991.xlsx')
    excel_list = []
    for index_main, row_main in df_main.iterrows():
        物理站点名称 = row_main['物理站点名称']
        经度 = float(row_main['经度'])
        纬度 = float(row_main['纬度'])
        excel_list.append({'物理站点名称':物理站点名称,'经度':经度,'纬度':纬度})
    # print(excel_list)
    site_1 = []
    site_2 = []
    ju_li_list = []
    for one_dict in excel_list:
        # di_gui_bi_jiao(one,excel_list)
        for my_list_one in excel_list:
            if one_dict['物理站点名称'] != my_list_one['物理站点名称']:
                ju_li = 给定经纬度计算两点之间距离(one_dict['经度'], one_dict['纬度'], my_list_one['经度'], my_list_one['纬度'])
                if ju_li < 10:
                    print(one_dict['物理站点名称'], my_list_one['物理站点名称'], ju_li)
                    site_1.append(one_dict['物理站点名称'])
                    site_2.append(my_list_one['物理站点名称'])
                    ju_li_list.append(ju_li)

    jie_guo_df = pandas.DataFrame({'物理站点名称':site_1,'物理站点名称2':site_2,'距离(米)':ju_li_list})
    jie_guo_df.to_excel('ju_li.xls')


