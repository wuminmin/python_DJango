import json
import traceback
import uuid

import pandas
import schedule
import time

#异步函数
import myConfig
from myConfig import sign_name
from mysite.chou_jiang_mongo import 采集模版表, 抽奖主界面表, 采集分工表
from mysite.demo_sms_send import send_sms
from mysite.ding_can_mongo import 订餐结果表, 订餐主界面表, 订餐提醒短信锁

def deprecated_async(f):
    def wrapper(*args, **kwargs):
        from threading import Thread
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

def job():
    创建时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(创建时间,"订餐提醒任务正在执行")

def 订餐提醒任务():
    try:
        日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        订餐提醒短信锁_first = 订餐提醒短信锁.objects(日期=日期).first()
        if 订餐提醒短信锁_first == None:
            订餐提醒短信锁(日期=日期,短信锁=False).save()
            订餐提醒任务()
        else:
            if 订餐提醒短信锁_first.短信锁 :
                return False
            else:
                订餐提醒短信锁_first.update(短信锁=True)
                template_code_ding_can_ti_xing = 'SMS_157682401'
                日期 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400))
                订餐结果表_objs = 订餐结果表.objects(用餐日期=日期)
                手机号_list = []
                手机号_list.append('13305669898')#这个用户要求屏蔽短信提醒
                for 订餐结果表_obj in 订餐结果表_objs:
                    if 订餐结果表_obj.中餐食堂就餐预订数 == 1 or 订餐结果表_obj.晚餐食堂就餐预订数 == 1:
                        手机号_list.append(订餐结果表_obj.手机号)
                订餐主界面表_objs = 订餐主界面表.objects
                for 订餐主界面表_obj in 订餐主界面表_objs:
                    手机号 = 订餐主界面表_obj.手机号
                    if 手机号 in 手机号_list:
                        pass
                    else:
                        # 创建时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                        # print(创建时间, '发送订餐提醒短信给', 手机号)
                        __business_id = uuid.uuid1()
                        name = 订餐主界面表_obj.姓名
                        params = {'name': name,'time':日期}
                        params = json.dumps(params).encode('utf-8').decode('unicode_escape')
                        r = send_sms(__business_id, 手机号, sign_name, template_code_ding_can_ti_xing, params)
                        r2 = json.loads(r)
                        if r2['Code'] == 'OK':
                            创建时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                            print(创建时间, '发送订餐提醒短信给', 手机号)
                return True
    except:
        print(traceback.format_exc())
        return False

def 发邮件(邮箱, 文件名, 姓名, 附件):
    import smtplib
    from email.header import Header
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    mail_host = 'smtp.qq.com'
    # receivers = '15305513057@189.cn'
    receivers = 邮箱
    sender = myConfig.qq_mail_send
    passwd = myConfig.qq_mail_passwd
    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = Header("订餐123", 'utf-8')
    message['To'] = Header(姓名, 'utf-8')
    subject = '订餐123订餐结果'
    message['Subject'] = Header(subject, 'utf-8')
    # 邮件正文内容
    message.attach(
        MIMEText(
            '这是“订餐123”微信小程序自动发出的邮件，请不要回复。若附件后缀名不可用，请下载后自行修改为 .xls',
            'plain',
            'utf-8'
        )
    )
    # 文件名 = '13093452622常柯仁淮南市20190323123702.csv'
    文件路径 = myConfig.django_root_path + '/' + 文件名
    # 构造附件1，传送当前目录下的 test.txt 文件
    # att1 = MIMEText(open(文件路径, 'rb').read(), 'base64', 'utf-8')
    att1 = MIMEText(附件, 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="excel.xls"'
    message.attach(att1)
    try:
        server = smtplib.SMTP_SSL(mail_host)
        server.login(sender, passwd)
        server.sendmail(sender, receivers, message.as_string())
        print('发送成功')
        return True
    except smtplib.SMTPException:
        print('无法发送')
        return False

def 订餐没吃统计发邮件(mail_addr):
    try:

        dcjg = 订餐结果表.objects()
        l1 = []
        l2 = []
        l3 = []
        l4 = []
        l5 = []
        l6 = []
        l7 = []
        l8 = []
        市公司本部员工移动电话list = []
        df1 = pandas.read_excel(myConfig.django_root_path + '/' + '市公司本部员工0610.xlsx', sheet_name=0)
        for index_main, row_main in df1.iterrows():
            市公司本部员工移动电话list.append(str(row_main['移动电话']))
        for dcjg_1 in dcjg:
            手机号 = dcjg_1.手机号
            用餐日期 = dcjg_1.用餐日期
            中餐食堂就餐签到 = dcjg_1.中餐食堂就餐签到
            晚餐食堂就餐签到 = dcjg_1.晚餐食堂就餐签到
            dczjm = 订餐主界面表.objects(
                手机号=手机号
            ).first()
            if dczjm == None:
                continue
            二级部门 = dczjm.二级部门
            四级部门 = dczjm.四级部门
            姓名 = dczjm.姓名
            l1.append(手机号)
            l2.append(用餐日期)
            l3.append(中餐食堂就餐签到)
            l4.append(晚餐食堂就餐签到)
            l5.append(二级部门)
            l6.append(四级部门)
            l7.append(姓名)
            if 手机号 in 市公司本部员工移动电话list:
                l8.append('本部员工')
            else:
                l8.append('非本部员工')
        jie_guo_df = pandas.DataFrame({
             '手机号': l1,
            '用餐日期': l2,
            '中餐食堂就餐签到': l3,
            '晚餐食堂就餐签到': l4,
            '二级部门': l5,
            '四级部门': l6,
            '姓名': l7,
            '是否本部':l8
        })
        创建时间 = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        file_name = '订餐没吃统计发邮件' + 创建时间 + '.xls'
        邮箱 = mail_addr
        文件名 = file_name
        姓名 = '管理员'
        import io
        s_buf = io.StringIO()
        # jie_guo_df.to_excel(s_buf)
        jie_guo_df.to_excel(file_name, encoding='gbk')
        附件 =  open(file_name,'rb').read()
        发邮件(邮箱, 文件名, 姓名,附件)
    except:
        print(traceback.format_exc())

@deprecated_async
def 启动订餐提醒定时器():
    mail_addr = ['15305669601@189.cn','15305669706@189.cn','15305666002@189.cn','18905667300@189.cn']
    # mail_addr = ['buckwmm@qq.com']
    # schedule.every().monday.do(订餐没吃统计发邮件,mail_addr)
    # schedule.every().day.at("17:14").do(订餐没吃统计发邮件,mail_addr)

    # schedule.every(10).seconds.do(job)
    # schedule.every(10).minutes.do(job)
    # schedule.every().hour.do(job)
    # schedule.every().day.at("10:30").do(job)
    # schedule.every(5).to(10).days.do(job)
    # schedule.every().monday.do(job)
    # schedule.every().wednesday.at("13:15").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':


    # mail_addr = ['15305669601@189.cn', '15305669706@189.cn', '15305666002@189.cn']
    mail_addr = ['buckwmm@qq.com']
    订餐没吃统计发邮件(mail_addr)

