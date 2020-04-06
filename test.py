import datetime
import json
import traceback
import uuid

import pandas
import schedule
import time

import sys, os
root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_path)

#异步函数
def deprecated_async(f):
    def wrapper(*args, **kwargs):
        from threading import Thread
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

def job():
    创建时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(创建时间,"订餐提醒任务正在执行")

def 自动核销():
    from canteen import models
    用餐日期 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    qset1 = models.订餐结果表.objects(用餐日期=用餐日期)
    for one in qset1:
        产品 = one.产品
        for one2 in models.产品名称列表字典['wx10547371f9547456']:
            if one2 in 产品:
                if 产品[one2]['签到'] == '没吃':
                    产品[one2]['签到'] = '吃过'
                    print(产品)
        one.update(产品=产品)


@deprecated_async
def 启动定时器():
    schedule.every().day.at("17:14").do(自动核销)
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

def a():
    from canteen import manage_models 
    from canteen import models
    # manage_models.my_user(
    #     d = {'username':'wmm','password':'123456'}
    # ).save()

    # q1 = models.订餐结果表.objects(手机号='13355661100').first()
    # print(q1)

    q1 = manage_models.my_user.objects(__raw__ = {'d.username':'wmm','d.password':'123456'}).first().to_json()
    print(q1)

def b():
    from canteen import models
    手机号 = '13355661100'
    当前月份 = '2020-04'
    订餐取消计数表1 = models.订餐取消计数表.objects(__raw__ = {'d.手机号':手机号,'d.月份':当前月份})
    print(订餐取消计数表1)                   
if __name__ == '__main__':
    # 自动核销()
    b()


