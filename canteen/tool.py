from . import db

def objectid_to_json(data): #转换ObjectId未'$oid'
    import json
    from bson import json_util, ObjectId
    res = json.loads(json_util.dumps(data))
    return res

# 异步函数
def deprecated_async(f):
    def wrapper(*args, **kwargs):
        from threading import Thread
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper
    
def 动态计算金额(数量,产品字典,折扣标签):
    if '价格' in 产品字典:
        if '折扣' in 产品字典:
            if 折扣标签 in 产品字典['折扣']:
                金额 = 数量*产品字典['价格']*产品字典['折扣'][折扣标签]
            else:
                金额 = 数量*产品字典['价格']
        else:
            金额 = 数量*产品字典['价格']
    else:
        金额 = 0
    print('动态计算金额-----------------',金额,数量,产品字典,折扣标签)
    return 金额

def 动态计算价格(产品字典,折扣标签):
    if '价格' in 产品字典:
        if '折扣' in 产品字典:
            if 折扣标签 in 产品字典['折扣']:
                价格 = 产品字典['价格']*产品字典['折扣'][折扣标签]
            else:
                价格 = 产品字典['价格']
        else:
            价格 = 产品字典['价格']
    else:
        价格 = 0
    print('动态计算价格-----------------',价格,产品字典,折扣标签)
    return 价格

def my_httpResponse(code,data,msg):
    from django.http import HttpResponse
    import json
    res_json = json.dumps({
        'code':code,
        'data':data,
        'msg':msg
    }).encode('utf-8').decode('unicode_escape')
    return HttpResponse(res_json)

def 微信认证(js_code,app_id):
    try:
        import requests
        import json
        import myConfig
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': app_id, 'secret': myConfig.appid_secret_dict[app_id], 'js_code': js_code,
                    'grant_type': 'authorization_code'}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        openid = r_json['openid']
        return {'openid':openid,'app_id':app_id}
    except:
        import traceback
        print(traceback.format_exc())
        return {'openid':'','app_id':''}

def get_str_time(i):
    import time
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + i*86400))

def get_str_date(i):
    import time
    return time.strftime('%Y-%m-%d', time.localtime(time.time() + i*86400))



@deprecated_async
def async_import_excel(mydata,flag,action):
    # from mysite import ding_can_mongo as ding_can_mongo #老版订餐后台
    from . import models as ding_can_mongo  #新版订餐后台
    import pandas
    import time
    try:
        if action == '上传用餐人员清单':
            for one in mydata:
                db.订餐人员表新增(one)
            db.创建订餐主界面表()
            ding_can_mongo1 = ding_can_mongo.订餐导入时间戳表.objects(flag=flag).first()
            if ding_can_mongo1 == None:
                ding_can_mongo.订餐导入时间戳表(
                    flag=flag,
                    isOk=True
                ).save()
            else:
                ding_can_mongo1.update(isOk=True)
        elif action == '上传充值清单':
            for one in mydata:
                手机号 = str(one['手机号'])
                充值金额 = one['充值金额']
                备注 = one['备注']
                ding_can_mongo.订餐钱包充值表(
                    手机号=手机号,
                    充值金额 = int(充值金额)*100, #分转换元
                    充值时间=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                    备注 = 备注
                ).save()
            ding_can_mongo1 = ding_can_mongo.订餐导入时间戳表.objects(flag=flag).first()
            if ding_can_mongo1 == None:
                ding_can_mongo.订餐导入时间戳表(
                    flag=flag,
                    isOk=True
                ).save()
            else:
                ding_can_mongo1.update(isOk=True)
        else:
            print('无效请求')
    except:
        import traceback
        r = traceback.format_exc()
        print(r)
        ding_can_mongo1 = ding_can_mongo.订餐导入时间戳表.objects(flag=flag).first()
        if ding_can_mongo1 == None:
            ding_can_mongo.订餐导入时间戳表(
                flag=flag,
                isOk=False,
                eLog={'log':r}
            ).save()
        else:
            ding_can_mongo1.update(isOk=False,eLog={'log':r})
