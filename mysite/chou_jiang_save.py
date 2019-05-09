import traceback

import pandas
import time
import json

from myConfig import django_root_path
from mysite.chou_jiang_mongo import 抽奖主界面表, 抽奖参与者, 采集分工表, 采集模版表, 建筑物主键分隔符, 可录入


def 导入主页数据(文件名):
    df_main = pandas.read_excel(django_root_path + '/' + 文件名)
    手机号_list = []
    主菜单id_list = []
    for index_main, row_main in df_main.iterrows():
        手机号 = row_main['手机号']
        主菜单id = row_main['主菜单id']
        if 手机号 in 手机号_list:
            pass
        else:
            手机号_list.append(手机号)
        if 主菜单id in 主菜单id_list:
            pass
        else:
            主菜单id_list.append(主菜单id)

    for 手机号 in 手机号_list:
        采集分工表.objects()
        主界内容 = []
        df_手机号 = df_main.loc[(df_main['手机号'] == 手机号)]
        for index, row in df_手机号.iterrows():
            创建时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            描述 = row['描述']
            主页标题 = row['主页标题']
            主页描述 = row['主页描述']
            验证码标题 = row['验证码标题']
            验证码描述 = row['验证码描述']
            二级部门 = row['二级部门']
            三级部门 = row['三级部门']
            四级部门 = row['四级部门']
            姓名 = row['姓名']
            主菜单name = row['主菜单name']
            主菜单id = row['主菜单id']
            df_手机号_主菜单name = df_main.loc[(df_main['手机号'] == 手机号) & (df_main['主菜单name'] == 主菜单name)]
            pages = []
            for index, row in df_手机号_主菜单name.iterrows():
                子菜单page_name = row['子菜单page_name']
                子菜单page_desc = row['子菜单page_desc']
                子菜单url = row['子菜单url']
                page = {}
                page['url'] = 子菜单url
                page['page_name'] = 子菜单page_name
                page['page_desc'] = 子菜单page_desc
                if page in pages:
                    pass
                else:
                    pages.append(page)
            主菜单id_dict = {
                'id': 主菜单id,
                'name': 主菜单name,
                'open': False,
                'pages': pages
            }
            if 主菜单id_dict in 主界内容:
                pass
            else:
                主界内容.append(主菜单id_dict)
            主界面表_one = 抽奖主界面表.objects(手机号=str(手机号)).first()
            if 主界面表_one == None:
                抽奖主界面表(手机号=str(手机号), 描述=str(描述), 创建时间=str(创建时间), 主页标题=str(主页标题), 主页描述=str(主页描述), 验证码标题=str(验证码标题)
                     , 验证码描述=str(验证码描述),二级部门=二级部门,三级部门=三级部门,四级部门=四级部门,姓名=姓名, 主界内容=主界内容).save()
            else:
                主界面表_one.update(手机号=str(手机号), 描述=str(描述), 创建时间=str(创建时间), 主页标题=str(主页标题), 主页描述=str(主页描述), 验证码标题=str(验证码标题)
                     , 验证码描述=str(验证码描述),二级部门=二级部门,三级部门=三级部门,四级部门=四级部门,姓名=姓名, 主界内容=主界内容)

def 导入分工表(文件名):
    df_main = pandas.read_excel(django_root_path + '/' + 文件名)
    for index_main, row_main in df_main.iterrows():
        try:
            区市县 = row_main['区/市/县']
            场所名称 = row_main['场所名称']
            建筑物ID = row_main['建筑物ID']
            建筑物名称 = row_main['建筑物名称']
            建筑物经度 = row_main['建筑物经度']
            建筑物纬度 = row_main['建筑物纬度']
            建筑物三高类型 = row_main['建筑物三高类型']
            责任人 = str(row_main['责任人'])
            分工 = {
                '区市县':区市县,
                '场所名称':场所名称,
                '建筑物ID':建筑物ID,
                '建筑物名称':建筑物名称,
                '建筑物经度':建筑物经度,
                '建筑物纬度':建筑物纬度,
                '建筑物三高类型':建筑物三高类型,
                '责任人':责任人
            }
            采集分工表first = 采集分工表.objects(
                建筑物编号=str(建筑物ID)
            ).first()
            if 采集分工表first == None:
                采集分工表(
                    手机号=责任人,
                    建筑物编号 = str(建筑物ID),
                    分工=分工
                ).save()
            else:
                采集分工表first.update(
                    手机号=责任人,
                    建筑物编号=str(建筑物ID),
                    分工=分工
                )
        except:
            print(traceback.format_exc())
            continue

def 修改采集模版表():
    采集模版表objs = 采集模版表.objects()
    for 采集模版表obj in 采集模版表objs:
        采集内容 = 采集模版表obj.采集内容
        print(采集内容)
        try:
            if 采集内容['shi_fou_you_di_xia_ting_cha_chang'] == 'true':
                采集内容['shi_fou_you_di_xia_ting_cha_chang'] = True
            else:
                采集内容['shi_fou_you_di_xia_ting_cha_chang'] = False
            if 采集内容['shi_fou_you_yi_wang_shi_feng'] == 'true':
                采集内容['shi_fou_you_yi_wang_shi_feng'] = True
            else:
                采集内容['shi_fou_you_yi_wang_shi_feng'] = False
            if 采集内容['shi_fou_you_yi_kan_cha'] == 'true':
                采集内容['shi_fou_you_yi_kan_cha'] = True
            else:
                采集内容['shi_fou_you_yi_kan_cha'] = False
            采集模版表obj.update(
                采集内容 =采集内容
            )
        except:
            continue

def 创建录入list(page_name):
    采集分工表objs = 采集分工表.objects(
        手机号=page_name
    )
    场所名称list = []
    for 采集分工表obj in 采集分工表objs:
        分工 = 采集分工表obj.分工
        场所名称 = 分工['场所名称']
        if 场所名称 in 场所名称list:
            pass
        else:
            场所名称list.append(场所名称)
    分工list = []
    for index, 场所名称one in enumerate(场所名称list):
        lou_ceng_list = []
        lou_ceng_index = 0
        ceng_list = []
        i = 4
        for 采集分工表obj in 采集分工表objs:

            分工 = 采集分工表obj.分工
            场所名称 = 分工['场所名称']
            if 场所名称one == 场所名称:
                建筑物ID = str(分工['建筑物ID'])
                建筑物名称 = str(分工['建筑物名称'])

                men_pai_dict = {
                    'men_pai_id': page_name+建筑物主键分隔符+场所名称+建筑物主键分隔符+建筑物ID+建筑物主键分隔符+建筑物名称,
                    'men_pai_hao': 建筑物名称,
                    'zhuang_tai': 可录入,
                }
                ceng_list.append(men_pai_dict)
                if i%3 == 0:
                    lou_ceng_dict = {
                        'lou_ceng_id': lou_ceng_index,
                        'ceng': ceng_list
                    }
                    ceng_list =[]
                    lou_ceng_list.append(lou_ceng_dict)
                    lou_ceng_index = lou_ceng_index +1
                i = i +1

        dan_yuan_list = {
            'dan_yuan_id': index,
            'dan_yuan_name': 场所名称one,
            'dan_yuan': lou_ceng_list
        }
        分工list.append(dan_yuan_list)

    print(json.dumps(分工list).encode('utf-8').decode('unicode_escape'))

if __name__ == '__main__':
    # 导入分工表('分工和楼宇信息收集记录模板.xlsx')


    # 主页文件名列表 = ['抽奖普通用户.xls','抽奖管理员.xls']
    主页文件名列表 = [ '采集普通用户.xls']
    for 文件名 in 主页文件名列表:
        导入主页数据(文件名)

        # 抽奖主界面表_obj = 抽奖主界面表.objects
        # for 抽奖主界面表_one in 抽奖主界面表_obj:
        #     抽奖参与者_first = 抽奖参与者.objects(手机号=抽奖主界面表_one.手机号).first()
        #     if 抽奖参与者_first == None:
        #         抽奖参与者(
        #             手机号=抽奖主界面表_one.手机号,
        #             姓名=抽奖主界面表_one.姓名,
        #             三级部门=抽奖主界面表_one.三级部门
        #         ).save()
        #     else:
        #         抽奖参与者_first.update(
        #             手机号=抽奖主界面表_one.手机号,
        #             姓名=抽奖主界面表_one.姓名,
        #             三级部门=抽奖主界面表_one.三级部门
        #         )

    # 修改采集模版表()
    # 创建录入list('网优班组')