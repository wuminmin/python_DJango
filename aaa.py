import traceback
from math import nan

import numpy
import pandas
import time

from haversine import haversine

from cell_analyse.cell_analyse_mongo import 分析扇区同方向表, 分析扇区同方向结果表
from myConfig import django_root_path
from mysite.views import 给定经纬度计算两点之间距离

def deprecated_async(f):
    def wrapper(*args, **kwargs):
        from threading import Thread
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

def 分析室分连线图(LTE扇区导出,室分基础导出):
    LTE扇区导出_df = pandas.read_excel(django_root_path + '/cell_analyse' + '/' + LTE扇区导出)
    室分基础导出_df = pandas.read_excel(django_root_path + '/cell_analyse' + '/' + 室分基础导出)
    print(LTE扇区导出_df.columns.tolist())
    print(室分基础导出_df.columns.tolist())
    name = []
    val = []
    lat = []
    lon = []
    for index_main, row_main in 室分基础导出_df.iterrows():
        经度 = float(row_main['经度'])
        纬度 = float(row_main['纬度'])
        LTE施主基站eNodeBID = float(row_main['LTE施主基站eNodeBID'])
        LTE施主扇区CellID = float(row_main['LTE施主扇区CellID'])
        LTE同PCI小区编号 = str(row_main['LTE同PCI小区编号'])
        功分扇区编号 = float(row_main['功分扇区编号'])
        室分系统名称 = str(row_main['室分系统名称'])
        for index_lte, row_lte in LTE扇区导出_df.iterrows():
            扇区经度 = float(row_lte['扇区经度'])
            扇区纬度 = float(row_lte['扇区纬度'])
            扇区中文名 = str(row_lte['扇区中文名'])
            扇区LTE施主基站eNodeBID = float(row_lte['基站标识eNodeBID'])
            扇区LTE施主扇区CellID = float(row_lte['小区标识CellID'])
            扇区LTE同PCI小区编号 = str(row_lte['同PCI小区编号'])
            扇区功分扇区编号 = float(row_lte['功分扇区编号'])
            if LTE施主基站eNodeBID==扇区LTE施主基站eNodeBID and LTE施主扇区CellID==扇区LTE施主扇区CellID  and LTE同PCI小区编号==扇区LTE同PCI小区编号 and 功分扇区编号 == 扇区功分扇区编号 :
                ju_li = 给定经纬度计算两点之间距离(经度,纬度,扇区经度,扇区纬度)
                print(室分系统名称, 扇区中文名, ju_li)
                if ju_li > 1500 :
                    print(室分系统名称,扇区中文名,ju_li)
                    name.append(室分系统名称)
                    val.append(ju_li)
                    lat.append(纬度)
                    lon.append(经度)
    jie_guo_df = pandas.DataFrame({'name': name, 'val': val, 'lat': lat,'lon':lon})
    创建时间 = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    jie_guo_df.to_csv('分析室分连线图' + 创建时间 + '.csv')

def 分析字段空白项(LTE扇区导出):
    name = []
    val = []
    lat = []
    lon = []
    LTE扇区导出_df = pandas.read_excel(django_root_path + '/cell_analyse' + '/' + LTE扇区导出)
    print(LTE扇区导出_df.columns.tolist())
    LTE扇区导出_columns_name_lsit = LTE扇区导出_df.columns.tolist()
    for index_main, row_main in LTE扇区导出_df.iterrows():
        for LTE扇区导出_name in LTE扇区导出_columns_name_lsit:
            LTE扇区导出_value = row_main[LTE扇区导出_name]
            # print(LTE扇区导出_value,type(LTE扇区导出_value))
            if LTE扇区导出_value is numpy.nan or LTE扇区导出_value == 'NaN' or LTE扇区导出_value == None:
                print(LTE扇区导出_value,LTE扇区导出_name,row_main['扇区中文名'])
                name.append(row_main['扇区中文名'])
                val.append(LTE扇区导出_name)
                lat.append(LTE扇区导出_value)
            else:
                # print('非空值',row_main)
                pass
    jie_guo_df = pandas.DataFrame({'name': name, 'val': val, 'lat': lat})
    创建时间 = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    jie_guo_df.to_csv('字段空白项分析'+创建时间+'.csv')

def 分析小区cellid命名(LTE扇区导出):
    主用号段 = ['69','6a','6b','6c','6d','dd','de','df']
    复用号段 = ['25','26','27','28','2b']
    cellid_主用号段_1800 = [50,63]
    cellid_主用号段_2100 = [0, 15]
    cellid_主用号段_2600 = [100, 111]
    cellid_主用号段_800_lte = [20, 31]
    cellid_主用号段_800_nb = [80, 95]
    cellid_复用号段_1800 = [176,191]
    cellid_复用号段_2100 = [128, 143]
    cellid_复用号段_2600 = [230, 239]
    cellid_复用号段_800_lte = [144, 159]
    cellid_复用号段_800_nb = [210, 223]
    主用号段频点 = {'3':cellid_主用号段_1800,'1':cellid_主用号段_2100,'41':cellid_主用号段_2600,'5':cellid_主用号段_800_lte,
              '11':cellid_主用号段_800_nb}
    复用号段频点 = {'3': cellid_复用号段_1800, '1': cellid_复用号段_2100, '41': cellid_复用号段_2600, '5': cellid_复用号段_800_lte,
              '11': cellid_复用号段_800_nb}
    name = []
    val = []
    lat = []
    lon = []
    LTE扇区导出_df = pandas.read_excel(django_root_path + '/cell_analyse' + '/' + LTE扇区导出)
    for index_main, row_main in LTE扇区导出_df.iterrows():
        try:
            MEID = row_main['MEID']
            cellLocalId = row_main['cellLocalId']
            # print(cellLocalId, type(cellLocalId))
            freqBandInd = row_main['freqBandInd']
            # print(freqBandInd, type(freqBandInd))
            # print(MEID,type(MEID))
            MEID_hex = hex(int(MEID))
            # print(MEID_hex,type(MEID_hex))
            MEID_hex_2_4 = MEID_hex[2:4]
            # print(MEID_hex_2_4)
            if MEID_hex_2_4 in 主用号段:
                if int(cellLocalId) >= 主用号段频点[freqBandInd][0] and int(cellLocalId) <= 主用号段频点[freqBandInd][1]:
                    pass
                else:
                    name.append(MEID)
                    val.append(cellLocalId)
                    lat.append(freqBandInd)
                    print('MEID',MEID,'cellLocalId',cellLocalId,'freqBandInd',freqBandInd)
            elif MEID_hex_2_4 in 复用号段:
                if int(cellLocalId) >= 复用号段频点[freqBandInd][0] and int(cellLocalId) <= 复用号段频点[freqBandInd][1]:
                    pass
                else:
                    name.append(MEID)
                    val.append(cellLocalId)
                    lat.append(freqBandInd)
                    print('MEID', MEID, 'cellLocalId', cellLocalId, 'freqBandInd', freqBandInd)
        except:
            print(traceback.format_exc())
            pass
    jie_guo_df = pandas.DataFrame({'MEID': name, 'cellLocalId': val, 'freqBandInd': lat})
    创建时间 = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    jie_guo_df.to_csv('分析小区cellid命名'+创建时间+'.csv')

def 列表全部空值(列表):
    flag = True
    for 元素 in 列表:
        if type(元素) is float:
            if numpy.math.isnan(元素):
                pass
            else:
                flag = False
    return flag

def 列表存在空值(列表):
    flag = False
    for 元素 in 列表:
        if type(元素) is float:
            if numpy.math.isnan(元素):
                flag = True
                return flag
    return flag

def 分析室分系统合路方式逻辑性(LTE扇区导出):
    col1 = []
    col2 = []
    col3 = []
    col4 = []
    col5 = []
    LTE扇区导出_df = pandas.read_excel(django_root_path + '/cell_analyse' + '/' + LTE扇区导出)
    LTE扇区导出_columns_name_lsit = LTE扇区导出_df.columns.tolist()
    print(LTE扇区导出_columns_name_lsit)
    for index_main, row_main in LTE扇区导出_df.iterrows():
        室分系统编号 = row_main['室分系统编号']
        室分系统合路方式 = row_main['室分系统合路方式']

        C网室分工程站号 =  row_main['C网室分工程站号']
        C网室分系统接入端信源类型 = row_main['C网室分系统接入端信源类型']
        C网所属BSC标识 = row_main['C网所属BSC标识']
        C网施主基站BTSID = row_main['C网施主基站BTSID']
        C网施主基站中文名 = row_main['C网施主基站中文名']
        C网施主扇区CellID = row_main['C网施主扇区CellID']
        C网施主扇区号 = row_main['C网施主扇区号']
        C网施主扇区名= row_main['C网施主扇区名']
        C网施主扇区PN = row_main['C网施主扇区PN']
        C网施主扇区LAC = row_main['C网施主扇区LAC']
        C网室分系统工作频点 = row_main['C网室分系统工作频点']
        C网室分系统接入信源设备厂商 = row_main['C网室分系统接入信源设备厂商']
        本扇区下C网直放站近端机数量 = row_main['本扇区下C网直放站近端机数量']
        本扇区下C网直放站远端机数量 = row_main['本扇区下C网直放站远端机数量']
        C网开通时间 = row_main['C网开通时间']
        C网室分系统运行状态 = row_main['C网室分系统运行状态']
        C网是否可监控 = row_main['C网是否可监控']
        与施主扇区距离 = row_main['与施主扇区距离（km）']
        光纤长度 = row_main['光纤长度（km）']
        C网室分参数list = []
        C网室分参数list.append(C网室分工程站号 )
        C网室分参数list.append(C网室分系统接入端信源类型)
        C网室分参数list.append(C网所属BSC标识)
        C网室分参数list.append(C网施主基站BTSID)
        C网室分参数list.append(C网施主基站中文名)
        C网室分参数list.append(C网施主扇区CellID)
        C网室分参数list.append(C网施主扇区号)
        C网室分参数list.append(C网施主扇区名)
        C网室分参数list.append(C网施主扇区PN)
        C网室分参数list.append(C网施主扇区LAC)
        C网室分参数list.append(C网室分系统工作频点)
        C网室分参数list.append(C网室分系统接入信源设备厂商)
        C网室分参数list.append(本扇区下C网直放站近端机数量)
        C网室分参数list.append(本扇区下C网直放站远端机数量)
        C网室分参数list.append(C网开通时间)
        C网室分参数list.append(C网室分系统运行状态)
        C网室分参数list.append(C网是否可监控)
        LTE室分系统接入端信源类型 = row_main['LTE室分系统接入端信源类型']
        LTE室分系统接入信源设备厂商 = row_main['LTE室分系统接入信源设备厂商']
        本扇区下L网直放站近端机数量 = row_main['本扇区下L网直放站近端机数量']
        本扇区下L网直放站远端机数量 = row_main['本扇区下L网直放站远端机数量']
        L网开通时间 = row_main['L网开通时间']
        L网室分系统运行状态 = row_main['L网室分系统运行状态']
        LTE施主基站设备商 = row_main['LTE施主基站设备商']
        LTE施主基站eNodeBID = row_main['LTE施主基站eNodeBID']
        LTE施主基站中文名 = row_main['LTE施主基站中文名(BBU)']
        LTE施主RRU产权 = row_main['LTE施主RRU产权']
        LTE施主RRU是否共享 = row_main['LTE施主RRU是否共享']
        LTE施主扇区CellID = row_main['LTE施主扇区CellID']
        索引关键值 = row_main['索引关键值（ECI）']
        LTE施主扇区号 = row_main['LTE施主扇区号']
        LTE同PCI小区编号 = row_main['LTE同PCI小区编号']
        功分扇区编号 = row_main['功分扇区编号']
        LTE扇区中文名 = row_main['LTE扇区中文名']
        LTE施主扇区PCI = row_main['LTE施主扇区PCI']
        LTERRU名称 = row_main['LTERRU名称']
        LTERRU是否级联 = row_main['LTERRU是否级联']
        级联RRU名称 = row_main['级联RRU名称']
        LTE是否同PCI = row_main['LTE是否同PCI']
        施主扇区TAC = row_main['施主扇区TAC']
        LTE室分list = []
        LTE室分list.append(LTE室分系统接入端信源类型  )
        LTE室分list.append(LTE室分系统接入信源设备厂商)
        LTE室分list.append(本扇区下L网直放站近端机数量)
        LTE室分list.append(本扇区下L网直放站远端机数量)
        LTE室分list.append(L网开通时间)
        LTE室分list.append(L网室分系统运行状态)
        LTE室分list.append(LTE施主基站设备商)
        LTE室分list.append(LTE施主基站eNodeBID)
        LTE室分list.append(LTE施主基站中文名)
        LTE室分list.append(LTE施主RRU产权)
        LTE室分list.append(LTE施主RRU是否共享)
        LTE室分list.append(LTE施主扇区CellID)
        LTE室分list.append(索引关键值)
        LTE室分list.append(LTE施主扇区号)
        LTE室分list.append(LTE同PCI小区编号)
        LTE室分list.append(功分扇区编号)
        LTE室分list.append(LTE扇区中文名)
        LTE室分list.append(LTE施主扇区PCI)
        LTE室分list.append(LTERRU名称)
        LTE室分list.append(LTERRU是否级联)
        LTE室分list.append(级联RRU名称)
        LTE室分list.append(LTE是否同PCI)
        LTE室分list.append(施主扇区TAC)
        # print('室分系统合路方式',室分系统合路方式,type(室分系统合路方式))
        # print('C网施主扇区名', C网施主扇区名, type(C网施主扇区名))
        # print('LTE扇区中文名', LTE扇区中文名, type(LTE扇区中文名))
        if 室分系统合路方式 == 'C+L共用':
            if C网室分系统运行状态 == '长期退服' and L网室分系统运行状态 == '长期退服' :
                pass
            elif  C网室分系统运行状态 == '长期退服' :
                if 列表存在空值(LTE室分list):
                    col1.append(室分系统编号)
                    col2.append(室分系统合路方式)
                    col3.append(C网施主扇区名)
                    col4.append(LTE扇区中文名)
                    col5.append('LTE扇区字段存在空值')
                    print('室分系统名称', 室分系统编号, '室分系统合路方式', 室分系统合路方式, 'C网施主扇区名', C网施主扇区名, 'LTE扇区中文名', LTE扇区中文名)
            elif L网室分系统运行状态 == '长期退服':
                if 列表存在空值(C网室分参数list):
                    col1.append(室分系统编号)
                    col2.append(室分系统合路方式)
                    col3.append(C网施主扇区名)
                    col4.append(LTE扇区中文名)
                    col5.append('C网室分字段存在空值')
                    print('室分系统名称', 室分系统编号, '室分系统合路方式', 室分系统合路方式, 'C网施主扇区名', C网施主扇区名, 'LTE扇区中文名', LTE扇区中文名)
            else:
                if 列表存在空值(C网室分参数list) or 列表存在空值(LTE室分list):
                    col1.append(室分系统编号)
                    col2.append(室分系统合路方式)
                    col3.append(C网施主扇区名)
                    col4.append(LTE扇区中文名)
                    col5.append('C网室分或L网室分字段存在空值')
                    print('室分系统名称', 室分系统编号, '室分系统合路方式', 室分系统合路方式, 'C网施主扇区名', C网施主扇区名, 'LTE扇区中文名', LTE扇区中文名)
        elif 室分系统合路方式 == 'L网专用':
            if 列表存在空值(LTE室分list):
                col1.append(室分系统编号)
                col2.append(室分系统合路方式)
                col3.append(C网施主扇区名)
                col4.append(LTE扇区中文名)
                col5.append('LTE扇区字段存在空值')
                print('室分系统名称', 室分系统编号, '室分系统合路方式', 室分系统合路方式, 'C网施主扇区名', C网施主扇区名, 'LTE扇区中文名', LTE扇区中文名)
            else:
                if 列表全部空值(C网室分参数list):
                    pass
                else:
                    col1.append(室分系统编号)
                    col2.append(室分系统合路方式)
                    col3.append(C网施主扇区名)
                    col4.append(LTE扇区中文名)
                    col5.append('C网扇区字段存在非空值')
                    print('室分系统名称', 室分系统编号, '室分系统合路方式', 室分系统合路方式, 'C网施主扇区名', C网施主扇区名, 'LTE扇区中文名', LTE扇区中文名)
        elif 室分系统合路方式 == 'C网专用':
            if 列表存在空值(C网室分参数list):
                col1.append(室分系统编号)
                col2.append(室分系统合路方式)
                col3.append(C网施主扇区名)
                col4.append(LTE扇区中文名)
                col5.append('C网室分字段存在空值')
                print('室分系统名称', 室分系统编号, '室分系统合路方式', 室分系统合路方式, 'C网施主扇区名', C网施主扇区名, 'LTE扇区中文名', LTE扇区中文名)
            else:
                if 列表全部空值(LTE室分list):
                    pass
                else:
                    col1.append(室分系统编号)
                    col2.append(室分系统合路方式)
                    col3.append(C网施主扇区名)
                    col4.append(LTE扇区中文名)
                    col5.append('LTE扇区字段存在非空值')
                    print('室分系统名称', 室分系统编号, '室分系统合路方式', 室分系统合路方式, 'C网施主扇区名', C网施主扇区名, 'LTE扇区中文名', LTE扇区中文名)
        else:
            col1.append(室分系统编号)
            col2.append(室分系统合路方式)
            col3.append(C网施主扇区名)
            col4.append(LTE扇区中文名)
            col5.append('室分系统合路方式字段异常')
            print('室分系统编号', 室分系统编号, '室分系统合路方式', 室分系统合路方式, 'C网施主扇区名', C网施主扇区名, 'LTE扇区中文名', LTE扇区中文名)
    jie_guo_df = pandas.DataFrame({'室分系统编号': col1, '室分系统合路方式': col2, 'C网施主扇区名': col3,'LTE扇区中文名':col4,'原因':col5})
    创建时间 = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    jie_guo_df.to_csv('分析室分系统合路方式逻辑性' + 创建时间 + '.csv',encoding='gbk')

def 分析扇区覆盖区域类型检查插花(LTE扇区导出):
    col1 = []
    col2 = []
    col3 = []
    col4 = []
    col5 = []
    LTE扇区导出_df = pandas.read_excel(django_root_path + '/cell_analyse' + '/' + LTE扇区导出)
    LTE扇区导出_columns_name_lsit = LTE扇区导出_df.columns.tolist()
    # for index_main, row_main in LTE扇区导出_df.iterrows():
    #     扇区经度 = row_main['扇区经度']
    #     扇区纬度 = row_main['扇区纬度']
    #     扇区覆盖区域类型 = row_main['扇区覆盖区域类型']

    from scipy import spatial
    import numpy as np
    A = np.random.random((10, 2)) * 100
    print(A)
    pt = [6, 30]  # <-- the point to find
    print( A[spatial.KDTree(A).query(pt)[1]] )  # <-- the nearest point
    distance, index = spatial.KDTree(A).query(pt)
    print(distance)  # <-- The distances to the nearest neighbors
    print(index)  # <-- The locations of the neighbors
    print(A[index])

def 计算经纬度距离(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）
    from math import radians, cos, sin, asin, sqrt
    # 将十进制度数转化为弧度
    # math.degrees(x):为弧度转换为角度
    # math.radians(x):为角度转换为弧度
    if lon1 == None or lat1 == None or lon2 == None or lat2 == None:
        return None
    else:
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine公式
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin( dlat /2 ) **2 + cos(lat1) * cos(lat2) * sin( dlon /2 ) **2
        c = 2 * asin(sqrt(a))
        r = 6371 # 地球平均半径，单位为公里
        return c * r*1000

@deprecated_async
def 异步计算是否同方向(LTE扇区导出_df_list, 营业部):
    for LTE扇区导出_df_one1 in LTE扇区导出_df_list:
        扇区中文名1 = LTE扇区导出_df_one1['扇区中文名']
        扇区经度1 = LTE扇区导出_df_one1['扇区经度']
        扇区纬度1 = LTE扇区导出_df_one1['扇区纬度']
        天线方位角1 = LTE扇区导出_df_one1['天线方位角']
        索引1 = LTE扇区导出_df_one1['索引']
        for LTE扇区导出_df_one2 in LTE扇区导出_df_list:
            扇区中文名2 = LTE扇区导出_df_one2['扇区中文名']
            扇区经度2 = LTE扇区导出_df_one2['扇区经度']
            扇区纬度2 = LTE扇区导出_df_one2['扇区纬度']
            天线方位角2 = LTE扇区导出_df_one2['天线方位角']
            索引2 = LTE扇区导出_df_one2['索引']
            if 索引1 == 索引2:
                pass
            else:
                距离12 = 计算经纬度距离(扇区经度1, 扇区纬度1, 扇区经度2, 扇区纬度2)
                if 距离12 < 50:
                    if abs(天线方位角1 - 天线方位角2) < 30:
                        print(扇区中文名1, 扇区中文名2, 天线方位角1, 天线方位角2)
                        LTE扇区同方向结果表first = 分析扇区同方向结果表.objects(
                            营业部=str(营业部),
                            扇区中文名1=str(扇区中文名1),
                            扇区中文名2=str(扇区中文名2),
                            天线方位角1=str(天线方位角1),
                            天线方位角2=str(天线方位角2)
                        ).first()
                        if LTE扇区同方向结果表first == None:
                            分析扇区同方向结果表(
                                营业部=str(营业部),
                                扇区中文名1=str(扇区中文名1),
                                扇区中文名2=str(扇区中文名2),
                                天线方位角1=str(天线方位角1),
                                天线方位角2=str(天线方位角2)
                            ).save()
                        else:
                            LTE扇区同方向结果表first.update(
                                营业部=str(营业部),
                                扇区中文名1=str(扇区中文名1),
                                扇区中文名2=str(扇区中文名2),
                                天线方位角1=str(天线方位角1),
                                天线方位角2=str(天线方位角2)
                            )

@deprecated_async
def 异步计算扇区分组(LTE扇区导出_df_营业部,网格编号,index):
    try:
        LTE扇区导出_df_list = []
        for index_main, row_main in LTE扇区导出_df_营业部.iterrows():
            扇区中文名 = row_main['扇区中文名']
            扇区经度 = float(row_main['扇区经度'])
            扇区纬度 = float(row_main['扇区纬度'])
            天线方位角 = float(row_main['天线方位角'])
            站点类型 = row_main['站点类型']
            if 站点类型 == '专用室分源':
                pass
            else:
                index = index +1
                LTE扇区导出_df_list.append({
                    '索引': index,
                    '扇区中文名': 扇区中文名,
                    '扇区经度': 扇区经度,
                    '扇区纬度': 扇区纬度,
                    '天线方位角': 天线方位角
                })
        if type(网格编号) is not str:
            print('type(网格编号) is not str',网格编号)
        else:
            分析扇区同方向表first = 分析扇区同方向表.objects(营业部=网格编号).first()
            if 分析扇区同方向表first == None:
                分析扇区同方向表(
                    营业部=网格编号,
                    扇区组=LTE扇区导出_df_list
                ).save()
            else:
                分析扇区同方向表first.update(
                    营业部=网格编号,
                    扇区组=LTE扇区导出_df_list
                )
            print(网格编号)
    except:
        print(traceback.format_exc())

def 分析扇区同方向计算分组(LTE扇区导出):
    分析扇区同方向表.objects().delete()
    分析扇区同方向结果表.objects().delete()
    LTE扇区导出_df = pandas.read_excel(django_root_path + '/cell_analyse' + '/' + LTE扇区导出)
    LTE扇区导出_columns_name_lsit = LTE扇区导出_df.columns.tolist()
    print(LTE扇区导出_columns_name_lsit)
    网格编号list = []
    index = 0
    for index_df, row_df in LTE扇区导出_df.iterrows():
        # 地市 = row_df['市/地区/州/盟']
        # 区县 = row_df['区/市/县/旗']
        网格编号 = row_df['网格编号']
        if 网格编号 in 网格编号list:
            pass
        else:
            网格编号list.append(网格编号)
    for 网格编号 in 网格编号list:
        LTE扇区导出_df_营业部 = LTE扇区导出_df.loc[
            (
                LTE扇区导出_df['网格编号'] == 网格编号
            )
        ]
        异步计算扇区分组(LTE扇区导出_df_营业部, 网格编号, index)
        index = index+100000

def 分析扇区同方向计算是否同方向():
    分析扇区同方向表objs = 分析扇区同方向表.objects
    for 分析扇区同方向表one in 分析扇区同方向表objs:
        异步计算是否同方向(分析扇区同方向表one.扇区组, 分析扇区同方向表one.营业部)

def 分析扇区同方向导出结果():
    分析扇区同方向结果表objs = 分析扇区同方向结果表.objects
    营业部list = []
    扇区中文名1list = []
    扇区中文名2list = []
    天线方位角1list = []
    天线方位角2list = []
    for 分析扇区同方向结果表one in 分析扇区同方向结果表objs:
        营业部 = 分析扇区同方向结果表one.营业部
        扇区中文名1 = 分析扇区同方向结果表one.扇区中文名1
        扇区中文名2 = 分析扇区同方向结果表one.扇区中文名2
        天线方位角1 = 分析扇区同方向结果表one.天线方位角1
        天线方位角2 = 分析扇区同方向结果表one.天线方位角2
        营业部list.append(营业部)
        扇区中文名1list.append(扇区中文名1)
        扇区中文名2list.append(扇区中文名2)
        天线方位角1list.append(天线方位角1)
        天线方位角2list.append(天线方位角2)
    jie_guo_df = pandas.DataFrame({
        '营业部': 营业部list,
        '扇区中文名1': 扇区中文名1list,
        '扇区中文名2': 扇区中文名2list,
        '天线方位角1': 天线方位角1list,
        '天线方位角2': 天线方位角2list
    })
    创建时间 = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    jie_guo_df.to_csv('分析扇区同方向导出结果' + 创建时间 + '.csv', encoding='gbk')

def 分析三频同方向扇区(文件名):
    df = pandas.read_excel(django_root_path + '/cell_analyse' + '/' + 文件名)
    # df_columns_name_lsit = df.columns.tolist()
    # print(df_columns_name_lsit)
    # df['扇区经度']
    # df['扇区纬度']
    # df['Eucl'] = [haversine( (df.扇区经度[i], df.扇区纬度[i]),(df.扇区经度[i], df.扇区纬度[i])) for i in range(len(df))]
    # cell_distance = haversine.distance()
    # print(df['Eucl'])
    grouped = [g[1] for g in df.groupby(['网格编号'])]
    for g in grouped:
        print(g['网格编号'])
        # g.apply(
        #     核查电子倾角, axis=1
        # )

def 分析扇区同PCI行数(文件名):
    df1 = pandas.read_excel(django_root_path + '/cell_analyse/' + 文件名, sheet_name=0)
    df1_是同PCI小区_室外站 = df1.loc[
        (df1['站点类型'] == '室外站') &
        (df1['是否同PCI小区'] == '是')
    ]
    df1_否同PCI小区_室外站 = df1.loc[
        (df1['站点类型'] == '室外站') &
        (df1['是否同PCI小区'] == '否')
    ]
    grouped_是同PCI小区_室外站 = [g[1] for g in df1_是同PCI小区_室外站.groupby(['物理站点名称'])]
    grouped_否同PCI小区_室外站 = [g[1] for g in df1_否同PCI小区_室外站.groupby(['物理站点名称'])]
    l1 = []
    l2 = []
    for grouped1 in grouped_是同PCI小区_室外站:
        # print(grouped1['物理站点名称'])
        if len(grouped1) == 1:
            print('异常情况----------',grouped1['物理站点名称'])
            l1.append('是同PCI小区行数等于1')
            l2.append(grouped1['物理站点名称'])
    for grouped2 in grouped_否同PCI小区_室外站:
        if len(grouped2) != 1:
            print('异常情况----------',grouped2['物理站点名称'])
            l1.append('否同PCI小区行数不等于1')
            l2.append(grouped2['物理站点名称'])
    jie_guo_df = pandas.DataFrame({
        '异常情况': l1,
        '物理站点名称':l2
    })
    创建时间 = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    jie_guo_df.to_excel('分析扇区同PCI行数' + 创建时间 + '.xls', encoding='gbk')

if __name__ == '__main__':
    # 分析室分连线图('LTE扇区导出_20190220_120220_02385.xlsx','室分基础导出 _20190220_120203_83105.xlsx')
    # 分析字段空白项('LTE扇区导出_20190220_120220_02385.xlsx')
    # 分析小区cellid命名('EUtranCellFDD_20190214_114628164.xlsx')
    # 分析室分系统合路方式逻辑性('室分基础导出 _20190215_114943_17578.xlsx')
    # 分析扇区覆盖区域类型检查插花('LTE扇区导出_20190220_120220_02385.xlsx')
    # 分析扇区同方向('LTE扇区导出_20190220_120220_02385.xlsx')

    # 分析扇区同方向计算分组('LTE扇区导出_20190506_152225_05858.xlsx')
    # 分析扇区同方向计算是否同方向()
    分析扇区同方向导出结果()

    # 分析三频同方向扇区('LTE扇区导出_20190220_120220_02385.xlsx')

    # 分析扇区同PCI行数('LTE扇区导出_20190220_120220_02385.xlsx')
