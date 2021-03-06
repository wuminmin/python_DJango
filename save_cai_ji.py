import pandas
import time

from myConfig import django_root_path
from mysite.chou_jiang_mongo import 抽奖主界面表, 抽奖参与者


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


if __name__ == '__main__':
    # 主页文件名列表 = ['抽奖普通用户.xls','抽奖管理员.xls']
    主页文件名列表 = [ '抽奖管理员.xls']
    for 文件名 in 主页文件名列表:
        导入主页数据(文件名)
        抽奖主界面表_obj = 抽奖主界面表.objects
        for 抽奖主界面表_one in 抽奖主界面表_obj:
            抽奖参与者_first = 抽奖参与者.objects(手机号=抽奖主界面表_one.手机号).first()
            if 抽奖参与者_first == None:
                抽奖参与者(
                    手机号=抽奖主界面表_one.手机号,
                    姓名=抽奖主界面表_one.姓名,
                    三级部门=抽奖主界面表_one.三级部门
                ).save()
            else:
                抽奖参与者_first.update(
                    手机号=抽奖主界面表_one.手机号,
                    姓名=抽奖主界面表_one.姓名,
                    三级部门=抽奖主界面表_one.三级部门
                )