import pandas
import time

from myConfig import django_root_path
from mysite.yi_cha_mongo import 易查试卷答案表, 考试未开始, 易查试卷模版表, 易查主界面表


def 增加答案():
    df = pandas.read_excel(django_root_path + '/易查试卷答案.xls')
    当前时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    for index, row in df.iterrows():
        考试大类 = row['考试大类']
        考试小类 = row['考试小类']
        试卷答案表_queryset = 易查试卷答案表.objects(考试大类=考试大类, 考试小类=考试小类)
        if 试卷答案表_queryset != []:
            试卷答案表_queryset.delete()

    for index, row in df.iterrows():
        考试大类 = row['考试大类']
        考试小类 = row['考试小类']
        答案编号 = row['答案编号']
        试卷答案表_one = 易查试卷答案表.objects(考试大类=考试大类, 考试小类=考试小类).first()
        if 试卷答案表_one == None:
            考试答案 = []
            考试答案.append(答案编号)
            易查试卷答案表(考试大类=考试大类, 考试小类=考试小类, 创建时间=当前时间, 考试答案=考试答案).save()
        else:
            试卷答案表_one.update(push__考试答案=答案编号)

def 增加试卷模版():
    df_main = pandas.read_excel(django_root_path + '/易查试卷模版.xls')
    考试大类_list = []
    考试小类_list = []
    for index_main, row_main in df_main.iterrows():
        考试大类列名 = row_main['子菜单page_name']
        考试小类列名 = row_main['子菜单page_desc']
        if 考试大类列名 in 考试大类_list:
            pass
        else:
            考试大类_list.append(考试大类列名)

        if 考试小类列名 in 考试小类_list:
            pass
        else:
            考试小类_list.append(考试小类列名)

    for 考试大类_one in 考试大类_list:
        for 考试小类_one in 考试小类_list:
            df = df_main.loc[(df_main['子菜单page_name'] == 考试大类_one) & (df_main['子菜单page_desc'] == 考试小类_one)]
            list = []
            i = 1
            timu = {}
            radioItems = []
            danxuan = {}
            子菜单url = ''
            考试时长 = ''
            考试开始时间 = ''
            考试结束时间 = ''
            for index, row in df.iterrows():
                考试时长 = row["考试时长"]
                子菜单url = row["子菜单url"]
                考试开始时间 = row["考试开始时间"]
                考试结束时间 = row["考试结束时间"]
                k = row["k"]
                v = row["v"]
                if k == 'tittle':
                    timu[k] = v
                if k == 'id':
                    timu[k] = v
                if k == 'name':
                    danxuan[k] = v
                if k == 'value':
                    danxuan[k] = v
                    radioItems.append(danxuan)
                    danxuan = {}
                if i == 10:
                    timu['radioItems'] = radioItems
                    list.append(timu)
                    timu = {}
                    radioItems = []
                    danxuan = {}
                elif i > 10 and i % 10 == 0:
                    timu['radioItems'] = radioItems
                    list.append(timu)
                    timu = {}
                    radioItems = []
                    danxuan = {}
                else:
                    pass
                i = i + 1
            试卷内容 = list
            考试状态 = 考试未开始
            考试大类 = 考试大类_one
            考试小类 = 考试小类_one
            创建时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            试卷模版表_one = 易查试卷模版表.objects( 子菜单page_name=考试大类, 子菜单page_desc=考试小类).first()
            if 试卷模版表_one == None:
                易查试卷模版表( 考试状态=考试状态, 子菜单page_name=考试大类
                      , 子菜单page_desc=考试小类, 考试时长=考试时长,子菜单url=子菜单url
                      , 考试开始时间=str(考试开始时间), 考试结束时间=str(考试结束时间), 创建时间=创建时间
                      , 试卷内容=试卷内容).save()
            else:
                试卷模版表_one.update( 考试状态=考试状态, 子菜单page_name=考试大类, 子菜单page_desc=考试小类
                                      ,考试时长=考试时长, 考试开始时间=str(考试开始时间),子菜单url=子菜单url
                                      ,考试结束时间=str(考试结束时间), 创建时间=创建时间, 试卷内容=试卷内容)

def 增加主页数据():
    df_main = pandas.read_excel(django_root_path + '/易查主页数据.xls')
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
            主界面表_one = 易查主界面表.objects(手机号=str(手机号)).first()
            if 主界面表_one == None:
                易查主界面表(手机号=str(手机号), 描述=str(描述), 创建时间=str(创建时间), 主页标题=str(主页标题), 主页描述=str(主页描述), 验证码标题=str(验证码标题)
                       , 验证码描述=str(验证码描述), 二级部门=二级部门, 三级部门=三级部门, 四级部门=四级部门, 姓名=姓名, 主界内容=主界内容).save()

            else:
                主界面表_one.update(手机号=str(手机号), 描述=str(描述), 创建时间=str(创建时间), 主页标题=str(主页标题), 主页描述=str(主页描述),
                                验证码标题=str(验证码标题)
                                , 验证码描述=str(验证码描述), 二级部门=二级部门, 三级部门=三级部门, 四级部门=四级部门, 姓名=姓名, 主界内容=主界内容)

if __name__ == '__main__':
    # 增加答案()
    # 增加试卷模版()
    增加主页数据()

