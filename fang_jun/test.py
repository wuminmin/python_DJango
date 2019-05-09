import pandas
import time
from pymongo import MongoClient

import myConfig
import json
from myConfig import django_root_path

def 测试(文件名1 , 文件名2):
    # client = MongoClient('mongodb://' + myConfig.username + ':' + myConfig.password + '@' + str(myConfig.host) + ':' + str(myConfig.port) + '/'+myConfig.db)
    # db = client['mydb']
    df1 = pandas.read_excel(django_root_path + '/' + 文件名1, sheet_name=1)
    df2 = pandas.read_excel(django_root_path + '/' + 文件名2, sheet_name=1)
    # records = json.loads(表1.T.to_json()).values()
    # print(type(records))
    # print(records)
    # db.方君分析出局光缆.insert(records)
    # print(table1)
    # print( table1['纤芯容量'] )
    # t3 = table1['纤芯容量']- table2['纤芯容量']
    # print(t3)
    df1_2 = df1.merge(df2,on='光缆段名称',how='left')
    df1_2['纤芯容量差值'] = df1_2['纤芯容量_x']-df1_2['纤芯容量_y']
    df1_2['封存芯数差值'] = df1_2['封存芯数_x'] - df1_2['封存芯数_y']
    df1_2['占用数差值'] = df1_2['占用数_x'] - df1_2['占用数_y']
    print(df1_2)
    创建时间 = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    df1_2.to_excel('分析出局光缆' + 创建时间 + '.xls', encoding='gbk')

if __name__ == '__main__':
    # 两高采集表每天发邮件()
    测试(
        'fang_jun/ODN-2019-03-18/318/7.24.2-OLT局站出局光缆能力调查表.csv',
        'fang_jun/ODN-2019-0304/ODN-2019-03-04/7.24.2-OLT局站出局光缆能力调查表.csv'
    )




