import pandas
import pandas as pd
import time
import json
from pymongo import MongoClient

import myConfig
from myConfig import django_root_path


def 分析出局光缆(文件名1, 文件名2):
    df1 = pandas.read_excel(django_root_path + '/' + 文件名1, sheet_name=1)
    df2 = pandas.read_excel(django_root_path + '/' + 文件名2, sheet_name=1)
    df1_2 = df1.merge(df2, on='光缆段名称', how='outer')
    df1_2['纤芯容量差值'] = df1_2['纤芯容量_y'] - df1_2['纤芯容量_x']
    df1_2['封存芯数差值'] = df1_2['封存芯数_y'] - df1_2['封存芯数_x']
    df1_2['占用数差值'] = df1_2['占用数_y'] - df1_2['占用数_x']
    df1_2.rename(columns={
        '纤芯容量_x': '纤芯容量_' + 文件名1,
        '纤芯容量_y': '纤芯容量_' + 文件名2,
        '封存芯数_x': '封存芯数_' + 文件名1,
        '封存芯数_y': '封存芯数_' + 文件名2,
        '占用数_x': '占用数_' + 文件名1,
        '占用数_y': '占用数_' + 文件名2,
    }, inplace=True)

    indexNames = df1_2[df1_2['纤芯容量差值'] == 0].index
    df1_2.drop(indexNames, inplace=True)
    df1_2 = df1_2[[
        '纤芯容量_' + 文件名1,
        '封存芯数_' + 文件名1,
        '占用数_' + 文件名1,
        '纤芯容量_' + 文件名2,
        '封存芯数_' + 文件名2,
        '占用数_' + 文件名2,
        '纤芯容量差值',
        '封存芯数差值',
        '占用数差值',
        '光缆段名称',
    ]]

    now_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    file_name = '分析出局光缆' + now_time + '.xls'
    df1_2.to_excel(file_name, encoding='gbk')
    print(file_name)


def 分析出局主配(文件名1, 文件名2):
    df1 = pandas.read_excel(django_root_path + '/' + 文件名1, sheet_name=1)
    df2 = pandas.read_excel(django_root_path + '/' + 文件名2, sheet_name=1)
    df1_2 = df1.merge(df2, on='连接设备集团名称', how='outer')
    df1_2['主干纤芯总数差值'] = df1_2['主干纤芯总数_y'] - df1_2['主干纤芯总数_x']
    df1_2['主干纤芯占用数差值'] = df1_2['主干纤芯占用数_y'] - df1_2['主干纤芯占用数_x']
    df1_2['配线纤芯总数差值'] = df1_2['配线纤芯总数_y'] - df1_2['配线纤芯总数_x']
    df1_2['配线纤芯占用数差值'] = df1_2['配线纤芯占用数_y'] - df1_2['配线纤芯占用数_x']
    df1_2['配线纤芯封存数差值'] = df1_2['配线纤芯封存数_y'] - df1_2['配线纤芯封存数_x']
    df1_2.rename(
        columns={
            '主干纤芯总数_x': '主干纤芯总数_' + 文件名1,
            '主干纤芯总数_y': '主干纤芯总数_' + 文件名2,
            '主干纤芯占用数_x': '主干纤芯占用数_' + 文件名1,
            '主干纤芯占用数_y': '主干纤芯占用数_' + 文件名2,
            '配线纤芯总数_x': '配线纤芯总数_' + 文件名1,
            '配线纤芯总数_y': '配线纤芯总数_' + 文件名2,
            '配线纤芯占用数_x': '配线纤芯占用数_' + 文件名1,
            '配线纤芯占用数_y': '配线纤芯占用数_' + 文件名2,
            '配线纤芯封存数_x': '配线纤芯封存数_' + 文件名1,
            '配线纤芯封存数_y': '配线纤芯封存数_' + 文件名2,
        },
        inplace=True
    )

    indexNames = df1_2[
        (df1_2['主干纤芯总数差值'] == 0) &
        (df1_2['主干纤芯占用数差值'] == 0) &
        (df1_2['配线纤芯总数差值'] == 0) &
        (df1_2['配线纤芯占用数差值'] == 0) &
        (df1_2['配线纤芯封存数差值'] == 0)
        ].index
    df1_2.drop(indexNames, inplace=True)
    df1_2 = df1_2[[
        '主干纤芯总数_' + 文件名1,
        '主干纤芯占用数_' + 文件名1,
        '配线纤芯总数_' + 文件名1,
        '配线纤芯占用数_' + 文件名1,
        '配线纤芯封存数_' + 文件名1,
        '主干纤芯总数_' + 文件名2,
        '主干纤芯占用数_' + 文件名2,
        '配线纤芯总数_' + 文件名2,
        '配线纤芯占用数_' + 文件名2,
        '配线纤芯封存数_' + 文件名2,
        '主干纤芯总数差值',
        '主干纤芯占用数差值',
        '配线纤芯总数差值',
        '配线纤芯占用数差值',
        '配线纤芯封存数差值',
        '连接设备集团名称',
    ]]

    now_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    file_name = '分析出局主配' + now_time + '.xls'
    df1_2.to_excel(file_name, encoding='gbk')
    print(file_name)


if __name__ == '__main__':
    分析出局光缆(
        'fang_jun/ODN-2019-03-18/318/7.24.2-OLT局站出局光缆能力调查表.csv',
        'fang_jun/ODN-2019-0304/ODN-2019-03-04/7.24.2-OLT局站出局光缆能力调查表.csv'
    )
    分析出局主配(
        'fang_jun/ODN-2019-03-18/318/7.24.3（含直配）光交主配纤芯情况统计表.csv',
        'fang_jun/ODN-2019-0304/ODN-2019-03-04/7.24.3-OLT出局主干（含直配）光交主配纤芯情况统计表.csv'
    )
    # 分析出局光缆(
    #     'fang_jun/OLT局站出局光缆能力调查表3月.csv',
    #     'fang_jun/OLT局站出局光缆能力调查表4月.csv'
    # )
    # 分析出局主配(
    #     'fang_jun/光交主配纤芯情况统计表3月.csv',
    #     'fang_jun/光交主配纤芯情况统计表4月.csv'
    # )
