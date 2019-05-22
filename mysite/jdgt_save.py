import pandas
import time

from myConfig import django_root_path
from mysite.jdgt_mongo import 结对共拓主界面表, 结对共拓食堂模版表, 结对共拓部门表, 结对共拓部门主任客户经理对应表


def 导入结对共拓部门主任客户经理对应表(文件名):
    df_main = pandas.read_excel(django_root_path + '/' + 文件名)
    for index_main, row in df_main.iterrows():
        部门主任手机号 = str(row['部门主任手机号'])
        客户经理手机号 = str(row['客户经理手机号'])
        tmp_first1 = 结对共拓部门主任客户经理对应表.objects(
            部门主任手机号码 = 部门主任手机号,
            客户经理手机号码 = 客户经理手机号,
        ).first()
        if tmp_first1 == None:
            结对共拓部门主任客户经理对应表(
                部门主任手机号码=部门主任手机号,
                客户经理手机号码=客户经理手机号,
            ).save()
        else:
            tmp_first1.update(
                部门主任手机号码=部门主任手机号,
                客户经理手机号码=客户经理手机号,
            )


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
            主界面表_one = 结对共拓主界面表.objects(手机号=str(手机号)).first()
            if 主界面表_one == None:
                结对共拓主界面表(手机号=str(手机号), 描述=str(描述), 创建时间=str(创建时间), 主页标题=str(主页标题), 主页描述=str(主页描述), 验证码标题=str(验证码标题)
                     , 验证码描述=str(验证码描述),二级部门=二级部门,三级部门=三级部门,四级部门=四级部门,姓名=姓名, 主界内容=主界内容).save()
            else:
                主界面表_one.update(手机号=str(手机号), 描述=str(描述), 创建时间=str(创建时间), 主页标题=str(主页标题), 主页描述=str(主页描述), 验证码标题=str(验证码标题)
                     , 验证码描述=str(验证码描述),二级部门=二级部门,三级部门=三级部门,四级部门=四级部门,姓名=姓名, 主界内容=主界内容)

def 保存订餐部门列表():
    结对共拓主界面表_all = 结对共拓主界面表.objects
    二级部门list = []
    for 结对共拓主界面表_one in 结对共拓主界面表_all:
        if 结对共拓主界面表_one.二级部门 in 二级部门list:
            pass
        else:
            二级部门list.append(结对共拓主界面表_one.二级部门)
    for 二级部门one in 二级部门list:
        结对共拓主界面表_二级部门 = 结对共拓主界面表.objects(二级部门=二级部门one)
        三级部门list = []
        for 结对共拓主界面表_二级部门one in 结对共拓主界面表_二级部门:
            if 结对共拓主界面表_二级部门one.三级部门 in 三级部门list:
                pass
            else:
                三级部门list.append(结对共拓主界面表_二级部门one.三级部门)
        结对共拓部门表_firtst = 结对共拓部门表.objects(二级部门=二级部门one).first()
        if 结对共拓部门表_firtst == None:
            结对共拓部门表(
                二级部门=二级部门one,
                三级部门列表=三级部门list
            ).save()
        else:
            结对共拓部门表_firtst.update(
                二级部门=二级部门one,
                三级部门列表=三级部门list
            )

def 导出订餐人员():
    col1 = []
    col2 = []
    col3 = []
    col4 = []
    col5 = []
    col6 = []
    col7 = []
    col8 = []
    col9 = []
    col10 = []
    结对共拓主界面表_objs = 结对共拓主界面表.objects()
    for 结对共拓主界面表_one in 结对共拓主界面表_objs:
        col1.append(结对共拓主界面表_one.手机号)
        col2.append(结对共拓主界面表_one.描述)
        col3.append(结对共拓主界面表_one.主页标题)
        col4.append(结对共拓主界面表_one.主页描述)
        col5.append(结对共拓主界面表_one.验证码标题)
        col6.append(结对共拓主界面表_one.验证码描述)
        col7.append(结对共拓主界面表_one.二级部门)
        col8.append(结对共拓主界面表_one.三级部门)
        col9.append(结对共拓主界面表_one.四级部门)
        col10.append(结对共拓主界面表_one.姓名)
    jie_guo_df = pandas.DataFrame({
        '手机号': col1,
        '描述': col2,
        '主页标题': col3,
        '主页描述': col4,
        '验证码标题': col5,
        '验证码描述': col6,
        '二级部门': col7,
        '三级部门': col8,
        '四级部门': col9,
        '姓名': col10,
    })
    创建时间 = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    jie_guo_df.to_excel('导出订餐人员' + 创建时间 + '.xls',encoding='gbk')

def 根据三级部门删除主界面表(三级部门):
    结对共拓主界面表objs = 结对共拓主界面表.objects(三级部门=三级部门)
    for one in 结对共拓主界面表objs:
        print(one.三级部门)
        one.delete()

if __name__ == '__main__':

    结对共拓主页文件名列表 = [ '结对共拓人员清单.xls']
    for 文件名 in 结对共拓主页文件名列表:
        导入主页数据(文件名)

    导入结对共拓部门主任客户经理对应表('结对共拓部门主任和客户经理对应表.xls')



