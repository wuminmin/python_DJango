import pandas
import time
import numpy
import myConfig

def 判断经纬度是否偏离归属营业部(文件名):
    df1 = pandas.read_excel(myConfig.django_root_path + '/cell_analyse/' + 文件名, sheet_name=0)
    print(list(df1.columns))
    grouped_网格编号 = [g[1] for g in df1.groupby(['网格编号'])]
    pass

def 判断某值是否在枚举值之内(文件名,文件名2):
    df1 = pandas.read_excel(myConfig.django_root_path + '/cell_analyse/' + 文件名, sheet_name=0)
    df2 = pandas.read_excel(myConfig.django_root_path + '/cell_analyse/' + 文件名2, sheet_name=0)
    print(list(df1.columns))
    扇区覆盖区域类型不合法 = '_0001'
    扇区覆盖道路类型不合法 = '_0002'
    扇区覆盖热点类型不合法 = '_0003'
    扇区类别不合法 = '_0004'
    扇区状态不合法 = '_0005'
    塔桅类型不合法 = '_0006'
    小区半径800M室分不合法 = '_0007'
    小区半径800M室外站县城市区密集市区不合法 = '_0008'
    小区半径800M室外站郊区不合法 = '_0009'
    小区半径800M室外站四种农村不合法 = '_0010'
    小区半径1800M室分不合法 = '_0011'
    小区半径1800M室外站县城市区密集市区不合法 = '_0012'
    小区半径1800M室外站郊区不合法 = '_0013'
    小区半径1800M室外站四种农村不合法 = '_0014'
    小区半径2100M室分不合法 = '_0015'
    小区半径2100M室外站县城市区密集市区不合法 = '_0016'
    小区半径2100M室外站郊区不合法 = '_0017'
    小区半径2100M室外站四种农村不合法 = '_0018'
    小区半径2600M室分不合法 = '_0019'
    小区半径2600M室外站县城市区密集市区不合法 = '_0020'
    小区半径2600M室外站郊区不合法 = '_0021'
    小区半径2600M室外站四种农村不合法 = '_0022'
    小区半径站点类型不合法 = '_0023'
    无法识别小区频段 = '_0024'
    预置电下倾角加可调电下倾角不等于电子倾角 = '_0025'
    预置电下倾角可调电下倾角电子倾角可能有异常值 = '_0026'
    电子倾角机械物理倾角不等于总下倾角 = '_0027'
    电子倾角机械物理倾角总下倾角可能有异常值 = '_0028'
    扇区机房共享情况不合法 = '_0029'
    扇区机房产权方不合法 = '_0030'
    塔桅共享情况不合法 = '_0031'
    塔桅产权方不合法 = '_0032'
    扇区经度偏离区县边界 = '_0033'
    扇区纬度偏离区县边界 = '_0034'
    扇区经度偏离区县边界异常 = '_0035'
    扇区纬度偏离区县边界异常 = '_0036'
    error_list = [
        扇区覆盖区域类型不合法,
        扇区覆盖道路类型不合法,
        扇区覆盖热点类型不合法,
        扇区类别不合法,
        扇区状态不合法,
        塔桅类型不合法,
        小区半径800M室分不合法,
        小区半径800M室外站县城市区密集市区不合法,
        小区半径800M室外站郊区不合法,
        小区半径800M室外站四种农村不合法,
        小区半径1800M室分不合法,
        小区半径1800M室外站县城市区密集市区不合法,
        小区半径1800M室外站郊区不合法,
        小区半径1800M室外站四种农村不合法,
        小区半径2100M室分不合法,
        小区半径2100M室外站县城市区密集市区不合法,
        小区半径2100M室外站郊区不合法,
        小区半径2100M室外站四种农村不合法,
        小区半径2600M室分不合法,
        小区半径2600M室外站县城市区密集市区不合法,
        小区半径2600M室外站郊区不合法,
        小区半径2600M室外站四种农村不合法,
        小区半径站点类型不合法,
        无法识别小区频段,
        预置电下倾角加可调电下倾角不等于电子倾角,
        预置电下倾角可调电下倾角电子倾角可能有异常值,
        电子倾角机械物理倾角不等于总下倾角,
        电子倾角机械物理倾角总下倾角可能有异常值,
        扇区机房共享情况不合法,
        扇区机房产权方不合法,
        塔桅共享情况不合法,
        塔桅产权方不合法,
        扇区经度偏离区县边界,
        扇区纬度偏离区县边界,
        扇区经度偏离区县边界异常,
        扇区纬度偏离区县边界异常,
    ]
    def is_in_list(row,my_col_name,my_list,error_code):
        if row[my_col_name] in my_list:
            return row[my_col_name]
        else:
            # return str('ERROR'+'_'+row[my_col_name]+'_not_in_'+str(my_list))
            return error_code
    扇区覆盖区域类型_list = [
        '密集市区',
        '市区',
        '县城',
        '郊区',
        '平原农村',
        '水域农村',
        '丘陵农村',
        '山区农村',
    ]
    扇区覆盖道路类型_list = [
        '市区',
        '县城',
        '高铁',
        '高速',
        '铁路',
        '航道',
        '国道',
        '省道',
        '县道',
        '乡道',
        '无'
    ]
    扇区覆盖热点类型_list = [
        '校园',
        '风景区',
        '交通集散地',
        '批发集贸市场',
        '会展中心',
        '体育场',
        '商业步行街',
        '大型企业',
        '大型医院',
        '港口',
        '写字楼',
        '宾馆酒店',
        '住宅小区',
        '隧道',
        '公墓',
        '无'
    ]
    扇区类别_list = [
        '室外宏基站扇区',
        '室分信源站扇区',
        '室内外混合扇区',
        '微基站扇区'
    ]
    扇区状态_list = [
        '正常',
        '故障长期退服',
        '搬迁中',
        '站点拆除'
    ]
    塔桅类型_list = [
        '无塔桅',
        '落地角钢塔',
        '落地景观塔',
        '落地拉线塔',
        '落地单管塔',
        '落地三管塔',
        '落地四管塔',
        '楼顶抱杆',
        '楼顶角钢塔',
        '楼顶美化天线',
        '楼顶拉线塔',
        '楼顶组合抱杆',
        '楼顶景观塔',
        'H杆',
        '水泥杆',
        '其他',
    ]
    扇区机房共享情况_list = [
        '电信独有',
        '电信移动',
        '电信联通',
        '电信移动联通',
        '无机房',
        '其他',
    ]
    扇区机房产权方_list = [
        '电信',
        '移动',
        '联通',
        '无机房',
        '其他',
        '铁塔',
    ]
    塔桅共享情况_ist = [
        '电信独有',
        '电信移动',
        '电信联通',
        '电信移动联通',
        '无塔桅',
        '其他',
    ]
    塔桅产权方_list = [
        '电信',
        '移动',
        '联通',
        '广电',
        '无塔桅',
        '其他',
        '铁塔',
    ]
    df1['扇区覆盖区域类型'] = df1.apply(
        is_in_list,args=('扇区覆盖区域类型',扇区覆盖区域类型_list,扇区覆盖区域类型不合法),axis=1)
    df1['扇区覆盖道路类型'] = df1.apply(
        is_in_list, args=('扇区覆盖道路类型', 扇区覆盖道路类型_list,扇区覆盖道路类型不合法), axis=1)
    df1['扇区覆盖热点类型'] = df1.apply(
        is_in_list, args=('扇区覆盖热点类型', 扇区覆盖热点类型_list,扇区覆盖热点类型不合法), axis=1)
    df1['扇区类别'] = df1.apply(
        is_in_list, args=('扇区类别', 扇区类别_list,扇区类别不合法), axis=1)
    df1['扇区状态'] = df1.apply(
        is_in_list, args=('扇区状态', 扇区状态_list,扇区状态不合法), axis=1)
    df1['塔桅类型'] = df1.apply(
        is_in_list, args=('塔桅类型', 塔桅类型_list,塔桅类型不合法), axis=1)
    df1['扇区机房共享情况'] = df1.apply(
        is_in_list, args=('扇区机房共享情况', 扇区机房共享情况_list,扇区机房共享情况不合法), axis=1)
    df1['扇区机房产权方'] = df1.apply(
        is_in_list, args=('扇区机房产权方', 扇区机房产权方_list,扇区机房产权方不合法), axis=1)
    df1['塔桅共享情况'] = df1.apply(
        is_in_list, args=('塔桅共享情况', 塔桅共享情况_ist,塔桅共享情况不合法), axis=1)
    df1['塔桅产权方'] = df1.apply(
        is_in_list, args=('塔桅产权方', 塔桅产权方_list,塔桅产权方不合法), axis=1)
    def 根据字段判断小区半径是否错误(row):
        cellid_主用号段_1800 = [50, 63]
        cellid_主用号段_2100 = [0, 15]
        cellid_主用号段_2600 = [100, 111]
        cellid_主用号段_800_lte = [20, 31]
        cellid_主用号段_800_nb = [80, 95]
        cellid_复用号段_1800 = [176, 191]
        cellid_复用号段_2100 = [128, 143]
        cellid_复用号段_2600 = [230, 239]
        cellid_复用号段_800_lte = [144, 159]
        cellid_复用号段_800_nb = [210, 223]
        小区标识CellID = int(row['小区标识CellID'])
        if 小区标识CellID >= cellid_主用号段_1800[0] and 小区标识CellID<= cellid_主用号段_1800[1]:
            频段指示 = '3.0'
        elif 小区标识CellID >= cellid_主用号段_2100[0] and 小区标识CellID<= cellid_主用号段_2100[1]:
            频段指示 = '1.0'
        elif 小区标识CellID >= cellid_主用号段_2600[0] and 小区标识CellID <= cellid_主用号段_2600[1]:
            频段指示 = '41.0'
        elif 小区标识CellID >= cellid_主用号段_800_lte[0] and 小区标识CellID <= cellid_主用号段_800_lte[1]:
            频段指示 = '5.0'
        elif 小区标识CellID >= cellid_主用号段_800_nb[0] and 小区标识CellID <= cellid_主用号段_800_nb[1]:
            频段指示 = '5.0'
        elif 小区标识CellID >= cellid_复用号段_1800[0] and 小区标识CellID <= cellid_复用号段_1800[1]:
            频段指示 = '3.0'
        elif 小区标识CellID >= cellid_复用号段_2100[0] and 小区标识CellID <= cellid_复用号段_2100[1]:
            频段指示 = '1.0'
        elif 小区标识CellID >= cellid_复用号段_2600[0] and 小区标识CellID <= cellid_复用号段_2600[1]:
            频段指示 = '41.0'
        elif 小区标识CellID >= cellid_复用号段_800_lte[0] and 小区标识CellID <= cellid_复用号段_800_lte[1]:
            频段指示 = '5.0'
        elif 小区标识CellID >= cellid_复用号段_800_nb[0] and 小区标识CellID <= cellid_复用号段_800_nb[1]:
            频段指示 = '5.0'
        else:
            return 无法识别小区频段
        扇区覆盖区域类型 = str(row['扇区覆盖区域类型'])
        小区半径 = str(row['小区半径（千米）'])
        站点类型 = row['站点类型']
        if 站点类型 == '专用室分源':
            if 频段指示 == '1.0':
                if 小区半径 == '0.04':
                    return row['小区半径（千米）']
                else:
                    return 小区半径2100M室分不合法
            elif 频段指示 == '3.0':
                if 小区半径 == '0.05':
                    return row['小区半径（千米）']
                else:
                    return 小区半径1800M室分不合法
            elif 频段指示 == '5.0':
                if 小区半径 == '0.06':
                    return row['小区半径（千米）']
                else:
                    return 小区半径800M室分不合法
            elif 频段指示 == '41.0':
                if 小区半径 == '0.04':
                    return row['小区半径（千米）']
                else:
                   return 小区半径2600M室分不合法
            else :
                return 无法识别小区频段
        elif 站点类型 == '室外站':
            if 频段指示 == '1.0':
                if 扇区覆盖区域类型 in ['县城', '市区', '密集市区']:
                    if 小区半径 == '0.1':
                        return row['小区半径（千米）']
                    else:
                        return 小区半径2100M室外站县城市区密集市区不合法
                if 扇区覆盖区域类型 in ['郊区']:
                    if 小区半径 == '0.17':
                        return row['小区半径（千米）']
                    else:
                        return 小区半径2100M室外站郊区不合法
                if 扇区覆盖区域类型 in ['平原农村', '丘陵农村', '山区农村', '水域农村']:
                    if 小区半径 == '0.35':
                        return row['小区半径（千米）']
                    else:
                        return 小区半径2100M室外站四种农村不合法
            elif 频段指示 == '3.0':
                if 扇区覆盖区域类型 in ['县城', '市区', '密集市区']:
                    if 小区半径 == '0.11':
                        return row['小区半径（千米）']
                    else:
                        return 小区半径1800M室外站县城市区密集市区不合法
                if 扇区覆盖区域类型 in ['郊区']:
                    if 小区半径 == '0.19':
                        return row['小区半径（千米）']
                    else:
                        return 小区半径1800M室外站郊区不合法
                if 扇区覆盖区域类型 in ['平原农村', '丘陵农村', '山区农村', '水域农村']:
                    if 小区半径 == '0.4':
                        return row['小区半径（千米）']
                    else:
                       return 小区半径1800M室外站四种农村不合法
            elif 频段指示 == '5.0':
                if 扇区覆盖区域类型 in ['县城', '市区', '密集市区']:
                    if 小区半径 == '0.12':
                        return row['小区半径（千米）']
                    else:
                        return 小区半径800M室外站县城市区密集市区不合法
                if 扇区覆盖区域类型 in ['郊区']:
                    if 小区半径 == '0.22':
                        return row['小区半径（千米）']
                    else:
                        return 小区半径800M室外站郊区不合法
                if 扇区覆盖区域类型 in ['平原农村', '丘陵农村', '山区农村', '水域农村']:
                    if 小区半径 == '0.45':
                        return row['小区半径（千米）']
                    else:
                        return 小区半径800M室外站四种农村不合法
            elif 频段指示 == '41.0':
                if 扇区覆盖区域类型 in ['县城', '市区', '密集市区']:
                    if 小区半径 == '0.09':
                        return row['小区半径（千米）']
                    else:
                        return  小区半径2600M室外站县城市区密集市区不合法
                if 扇区覆盖区域类型 in ['郊区']:
                    if 小区半径 == '0.15':
                        return row['小区半径（千米）']
                    else:
                        return 小区半径2600M室外站郊区不合法
                if 扇区覆盖区域类型 in ['平原农村', '丘陵农村', '山区农村', '水域农村']:
                    if 小区半径 == '0.3':
                        return row['小区半径（千米）']
                    else:
                       return 小区半径2600M室外站四种农村不合法
            else :
                return 无法识别小区频段
        else:
            return 小区半径站点类型不合法
    df1['小区半径（千米）'] = df1.apply(
        根据字段判断小区半径是否错误, axis=1
    )
    def 核查电子倾角(row):
        预置电下倾角 = row['预置电下倾角']
        可调电下倾角 = row['可调电下倾角']
        电子倾角 = row['电子倾角']
        try:
            if 预置电下倾角+可调电下倾角 == 电子倾角:
                return row['电子倾角']
            else:
                return 预置电下倾角加可调电下倾角不等于电子倾角
        except:
            return 预置电下倾角可调电下倾角电子倾角可能有异常值
    df1['电子倾角'] = df1.apply(
        核查电子倾角, axis=1
    )
    def 核查总下倾角(row):
        电子倾角 = row['电子倾角']
        机械物理倾角 = row['机械物理倾角']
        总下倾角 = row['总下倾角']
        try:
            if 电子倾角 + 机械物理倾角 == 总下倾角:
                return row['总下倾角']
            else:
                return 电子倾角机械物理倾角不等于总下倾角
        except:
            return 电子倾角机械物理倾角总下倾角可能有异常值
    df1['总下倾角'] = df1.apply(
        核查总下倾角, axis=1
    )
    def 核查经度偏离县区(row):
        try:
            xian_name = row['区/市/县/旗']
            df2_xian_name = df2.loc[
                df2['县'] == xian_name
            ]
            左下角经度 = df2_xian_name['左下角经度'][0]
            左下角纬度 = df2_xian_name['左下角纬度'][0]
            右上角经度 = df2_xian_name['右上角经度'][0]
            右上角纬度 = df2_xian_name['右上角纬度'][0]
            #and row['扇区纬度'] >= 左下角纬度 and row['扇区纬度'] <= 右上角纬度
            if row['扇区经度'] >= 左下角经度 and row['扇区经度'] <= 右上角经度 :
                return  row['扇区经度']
            else:
                return 扇区经度偏离区县边界
        except:
            return 扇区经度偏离区县边界异常
    def 核查纬度偏离县区(row):
        try:
            xian_name = row['区/市/县/旗']
            df2_xian_name = df2.loc[
                df2['县'] == xian_name
            ]
            左下角经度 = df2_xian_name['左下角经度'][0]
            左下角纬度 = df2_xian_name['左下角纬度'][0]
            右上角经度 = df2_xian_name['右上角经度'][0]
            右上角纬度 = df2_xian_name['右上角纬度'][0]
            #and row['扇区纬度'] >= 左下角纬度 and row['扇区纬度'] <= 右上角纬度
            if row['扇区纬度'] >= 左下角纬度 and row['扇区纬度'] <= 右上角纬度 :
                return  row['扇区纬度']
            else:
                return 扇区纬度偏离区县边界
        except:
            return 扇区纬度偏离区县边界异常

    # df1['扇区经度'] = df1.apply(
    #     核查经度偏离县区, axis=1
    # )
    # df1['扇区纬度'] = df1.apply(
    #     核查纬度偏离县区, axis=1
    # )
    r = df1.loc[
        df1['扇区覆盖区域类型'].isin(error_list) |
        df1['扇区覆盖道路类型'].isin(error_list) |
        df1['扇区覆盖热点类型'].isin(error_list) |
        df1['扇区类别'].isin(error_list) |
        df1['扇区状态'].isin(error_list) |
        df1['塔桅类型'].isin(error_list) |
        df1['小区半径（千米）'].isin(error_list) |
        df1['电子倾角'].isin(error_list)|
        df1['总下倾角'].isin(error_list)|
        df1['扇区机房共享情况'].isin(error_list)|
        df1['扇区机房产权方'].isin(error_list)|
        df1['塔桅共享情况'].isin(error_list)|
        df1['塔桅产权方'].isin(error_list) |
        df1['扇区经度'].isin(error_list) |
        df1['扇区纬度'].isin(error_list)
    ]
    r2 = r[[
        '扇区中文名',
        '扇区经度',
        '扇区纬度',
        '扇区覆盖区域类型',
        '扇区覆盖道路类型',
        '扇区覆盖热点类型',
        '扇区类别',
        '扇区状态',
        '塔桅类型',
        '小区半径（千米）',
        '电子倾角',
        '总下倾角',
        '扇区机房共享情况',
        '扇区机房产权方',
        '塔桅共享情况',
        '塔桅产权方',
    ]]
    创建时间 = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    r2.to_excel('判断某值是否在枚举值之内' + 创建时间 + '.xlsx', encoding='gbk')

def 根据网管eci和扇区库核查冗余数据和新增数据(文件名1,文件名2):
    df1 = pandas.read_excel(myConfig.django_root_path + '/cell_analyse/' + 文件名1, sheet_name=0)
    df2 = pandas.read_excel(myConfig.django_root_path + '/cell_analyse/' + 文件名2, sheet_name=0)
    df1['ECI'] = df1['基站标识eNodeBID'].apply(str)+'_'+df1['小区标识CellID'].apply(str)
    df1_2 = df1.merge(df2, on='ECI', how='outer')
    创建时间 = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    df1_2.to_excel('根据网管eci和扇区库核查冗余数据和新增数据' + 创建时间 + '.xlsx', encoding='gbk')

if __name__ == '__main__':
    判断某值是否在枚举值之内('LTE扇区导出_20190220_120220_02385.xlsx','县区经纬度边界.xlsx')
    # 判断某值是否在枚举值之内('LTE扇区导出_20190220_120220_02385.xlsx')
    # 根据网管eci和扇区库核查冗余数据和新增数据(
    #     'LTE扇区导出_20190408_092330_26520.xlsx',
    #     '临时-网管ECI.xlsx'
    # )