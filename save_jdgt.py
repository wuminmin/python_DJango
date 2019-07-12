import pandas
import time

from myConfig import django_root_path
from mysite.jdgt_mongo import 结对共拓主界面表, 结对共拓部门主任客户经理对应表, 结对共拓客户经理上传单位信息


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

def 导入结对共拓客户经理上传单位信息(文件名):
    df_main = pandas.read_excel(django_root_path + '/' + 文件名)
    for index_main, row in df_main.iterrows():
        单位名称 = str(row['单位名称'])
        客户编码 = str(row['客户编码'])
        客户经理 = str(row['客户经理'])
        客户经理手机号 = str(row['手机号码']).replace('.0','')
        tmp_first1 = 结对共拓客户经理上传单位信息.objects(客户编码 = 客户编码).first()
        if tmp_first1 == None:
            结对共拓客户经理上传单位信息(单位名称=单位名称, 手机号码=客户经理手机号,客户编码=客户编码,客户经理=客户经理
            ).save()
        else:
            tmp_first1.update(单位名称=单位名称, 手机号码=客户经理手机号, 客户编码=客户编码, 客户经理=客户经理
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

if __name__ == '__main__':

    # 导入主页数据('结对共拓人员表.xls')
    # 导入主页数据('结对共拓吴敏民.xls')
    # 导入结对共拓部门主任客户经理对应表('结对共拓部门主任和客户经理对应表.xls')
    导入结对共拓客户经理上传单位信息('结对共拓客户经理上传单位信息.xls')



# http://tmp/wxca4779d41f122b0a.o6zAJs0D5dGn7wRzf8MdA1si3laY.DkSuq9Os57Dg3458ca8be422d381c457abcb14699ed6.jpg
# http://tmp/wxca4779d41f122b0a.o6zAJs0D5dGn7wRzf8MdA1si3laY.eBIG6nLyQDjka2d53c65a8fb2a0666ac36cd0965f99a.jpg

# http://tmp/wxca4779d41f122b0a.o6zAJs0D5dGn7wRzf8MdA1si3laY.DkSuq9Os57Dg3458ca8be422d381c457abcb14699ed6.jpg
# http://tmp/wxca4779d41f122b0a.o6zAJs0D5dGn7wRzf8MdA1si3laY.eBIG6nLyQDjka2d53c65a8fb2a0666ac36cd0965f99a.jpg