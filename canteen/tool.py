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

def wx_login_get_openid(request):
    import requests
    import json
    import traceback
    import myConfig
    try:
        js_code = request.GET['code']
        app_id = request.GET['app_id']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': app_id, 'secret': myConfig.appid_secret_dict[app_id], 'js_code': js_code,
                    'grant_type': 'authorization_code'}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        openid = r_json['openid']
        return {'openid':openid,'app_id':app_id}
    except:
        print(traceback.format_exc())
        return None

def wx_pay_success_get_openid(app_id,oid):
    from . import tool
    openid = db.query_openid_by_ding_can_jie_guo_oid(oid)
    return {'openid':openid,'app_id':app_id}

@deprecated_async
def async_import_excel(mydata,flag,action):
    from . import models as ding_can_mongo  #新版订餐后台
    import pandas
    import time
    try:
        if action == '上传用餐人员清单':
            res = db.创建订餐主界面表(mydata)
            ding_can_mongo1 = ding_can_mongo.订餐导入时间戳表.objects(flag=flag).first()
            if ding_can_mongo1 == None:
                if res:
                    ding_can_mongo.订餐导入时间戳表(
                        flag=flag,
                        isOk=True
                    ).save()
                else:
                    ding_can_mongo.订餐导入时间戳表(
                        flag=flag,
                        isOk=False
                    ).save()
            else:
                if res:
                    ding_can_mongo1.update(isOk=True)
                else:
                    ding_can_mongo1.update(isOk=False)

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


@deprecated_async
def 异步计算订餐结果(子菜单page_name, 二级部门):
    from . import models
    import time
    第一天 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    第二天 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400))
    第三天 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400 + 86400))
    日期_list = [第一天, 第二天, 第三天]
    for 日期_list_one in 日期_list:
        日期 = 日期_list_one
        子菜单page_desc_list = [
            models.早餐统计, models.中餐统计, models.晚餐统计,
            models.早餐外带统计, models.中餐外带统计, models.晚餐外带统计]
        for 子菜单page_desc_list_one in 子菜单page_desc_list:
            子菜单page_desc = 子菜单page_desc_list_one
            订餐部门表_first = models.订餐部门表.objects(二级部门=二级部门).first()
            if 订餐部门表_first == None:
                name_list = []
            else:
                name_list = 订餐部门表_first.三级部门列表
            总人数 = 0
            没吃人数 = 0
            吃过人数 = 0
            总份数 = 0
            没吃份数 = 0
            吃过份数 = 0
            订餐结果表_all = models.订餐结果表.objects(子菜单page_name=子菜单page_name, 用餐日期=日期)
            r_list = []
            id = 1
            for name_one in name_list:
                r_dict = {}
                r_dict['id'] = id
                id = id + 1
                r_dict['name'] = name_one
                pages = []
                r_dict['num'] = len(pages)
                if r_dict['num'] == 0:
                    pass
                else:
                    r_dict['pages'] = pages
                    r_list.append(r_dict)
            描述 = '下载成功'
            app_tittle = 子菜单page_desc
            app_des = '总人数 ' + str(总人数) + ';总份数' + str(总份数)
            app_code_des = '吃过人数 ' + str(吃过人数) + ';吃过份数' + str(吃过份数)
            app_code = '没吃人数' + str(没吃人数) + ';没吃份数' + str(没吃份数)
            自定义登录状态 = {'描述': 描述, '会话': '23456', 'list': r_list, 'app_tittle': app_tittle, 'app_des': app_des,
                'app_code_des': app_code_des, 'app_code': app_code, 'date': 日期, 'start_date': 第一天, 'end_date': 第三天}
            订餐统计结果_first = models.订餐统计结果.objects(日期=日期, 子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc).first()
            if 订餐统计结果_first == None:
                models.订餐统计结果(日期=日期, 子菜单page_name=子菜单page_name, 子菜单page_desc=子菜单page_desc, 订餐结果=自定义登录状态).save()
            else:
                订餐统计结果_first.update(订餐结果=自定义登录状态)

@deprecated_async
def 异步统计产品(食堂名称,二级部门,wx_login_get_openid_dict):
    import time
    第一天 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    第二天 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400))
    第三天 = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400 + 86400))
    日期_list = [第一天, 第二天, 第三天]
    # 订餐部门表_first = 订餐部门表.objects(二级部门=二级部门).first()
    from . import models
    qset1 = models.订餐主界面表.objects(二级部门=二级部门)
    name_list = []
    for one in qset1:
        三级部门 = one.三级部门
        if 三级部门 in name_list:
            pass
        else:
            name_list.append(三级部门)
    for 日期_list_one in 日期_list:
        日期 = 日期_list_one
        from . import models
        for 产品 in models.产品全局字典[wx_login_get_openid_dict['app_id']]['产品列表']:
            产品名称 = 产品['名称']
            pipeline = [
                {
                    "$match": {
                        "产品."+产品名称+".预定数量": {
                            "$gte":1
                        },
                        "用餐日期":日期
                    }
                }
            ]
            总人数 = len(list(models.订餐结果表.objects.aggregate(*pipeline)))
            pipeline2 = [
                    {
                    "$match": {
                        "产品."+产品名称+".预定数量": {
                            "$gte":1
                        },
                        "产品."+产品名称+".签到":"没吃",
                        "用餐日期":日期_list_one
                    }
                }
            ]
            没吃人数 = len(list(models.订餐结果表.objects.aggregate(*pipeline2)))
            pipeline3 = [
                    {
                    "$match": {
                        "产品."+产品名称+".预定数量": {
                            "$gte":1
                        },
                        "产品."+产品名称+".签到":"吃过",
                        "用餐日期":日期_list_one
                    }
                }
            ]
            吃过人数 = len(list(models.订餐结果表.objects.aggregate(*pipeline3)))
            pipeline4 = [
                {
                    "$match": {
                        "产品."+产品名称+".预定数量": {
                            "$gte":1
                        },
                        "用餐日期":日期_list_one
                    }
                }
                ,
                {
                    "$group": {
                        "_id": "null",
                        产品名称: {
                            "$sum": "$产品."+产品名称+".预定数量"
                        }
                    }
                }
            ]
            总份数 = 0
            for r in list(models.订餐结果表.objects.aggregate(*pipeline4)):
                总份数 = r[产品名称]
            pipeline5 = [
                {
                    "$match": {
                        "产品."+产品名称+".预定数量": {
                            "$gte":1
                        },
                        "产品."+产品名称+".签到":"没吃",
                        "用餐日期":日期_list_one
                    }
                }
                ,
                {
                    "$group": {
                        "_id": "null",
                        产品名称: {
                            "$sum": "$产品."+产品名称+".预定数量"
                        }
                    }
                }
            ]
            没吃份数 = 0
            for r in list(models.订餐结果表.objects.aggregate(*pipeline5)):
                没吃份数 = r[产品名称]
            pipeline6 = [
                {
                    "$match": {
                        "产品."+产品名称+".预定数量": {
                            "$gte":1
                        },
                        "产品."+产品名称+".签到":"吃过",
                        "用餐日期":日期_list_one
                    }
                }
                ,
                {
                    "$group": {
                        "_id": "null",
                        产品名称: {
                            "$sum": "$产品."+产品名称+".预定数量"
                        }
                    }
                }
            ]
            吃过份数 = 0
            for r in list(models.订餐结果表.objects.aggregate(*pipeline6)):
                吃过份数 = r[产品名称]
            r_list = []
            id = 1
            for name_one in name_list:
                r_dict = {}
                r_dict['id'] = id
                id = id + 1
                r_dict['name'] = name_one
                pages = []
                for p in list(models.订餐结果表.objects.aggregate(*pipeline)):
                    订餐主界面表_first = models.订餐主界面表.objects(手机号=p['手机号'], 三级部门=name_one).first()
                    if 订餐主界面表_first == None:
                        continue
                    else:
                        rr_dict = {}
                        if p['产品'][产品名称]['签到'] == '没吃':
                            rr_dict['page_name'] = 订餐主界面表_first.姓名
                            rr_dict['shu_liang'] = p['产品'][产品名称]['预定数量']
                            rr_dict['page_desc'] = p['产品'][产品名称]['签到']
                            pages.append(rr_dict)
                r_dict['num'] = len(pages)
                if r_dict['num'] == 0:
                    pass
                else:
                    r_dict['pages'] = pages
                    r_list.append(r_dict)
            描述 = '下载成功'
            app_tittle = 产品名称
            app_des = '总人数 ' + str(总人数) + ';总份数' + str(总份数)
            app_code_des = '吃过人数 ' + str(吃过人数) + ';吃过份数' + str(吃过份数)
            app_code = '没吃人数' + str(没吃人数) + ';没吃份数' + str(没吃份数)
            自定义登录状态 = {'描述': 描述, '会话': '23456', 'list': r_list, 'app_tittle': app_tittle, 'app_des': app_des,
                'app_code_des': app_code_des, 'app_code': app_code, 'date': 日期, 'start_date': 第一天, 'end_date': 第三天}
            订餐统计结果_first = models.订餐统计结果.objects(日期=日期, 子菜单page_name=食堂名称, 子菜单page_desc=产品名称).first()
            if 订餐统计结果_first == None:
                models.订餐统计结果(日期=日期, 子菜单page_name=食堂名称, 子菜单page_desc=产品名称, 订餐结果=自定义登录状态).save()
            else:
                订餐统计结果_first.update(订餐结果=自定义登录状态)

#银联支付下订单
def ding_can_chinaums_pay_order(totalAmount,goods,wx_login_get_openid_dict):
    import traceback
    import json
    import time
    import myConfig
    import datetime
    try:
        # totalAmount = '1' #支付1分钱
        totalAmount = str(totalAmount)
        print('totalAmount----',totalAmount)
        totalAmount_list = totalAmount.split('.')
        totalAmount = totalAmount_list[0]
        print('ding_can_chinaums_pay_order------------------',wx_login_get_openid_dict)
        scrit_key = myConfig.chinaums_scrit_key
        msgId = myConfig.chinaums_msgId
        msgSrc = myConfig.chinaums_msgSrc
        msgType = myConfig.chinaums_msgType
        requestTimestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        merOrderId = myConfig.chinaums_msgId+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        mid = myConfig.chinaums_mid
        tid = myConfig.chinaums_tid
        instMid = myConfig.chinaums_instMid
        tradeType = myConfig.chinaums_tradeType
        subAppId = myConfig.chinaums_subAppId
        subOpenId = wx_login_get_openid_dict['openid']
        wmm_json = {
            'msgId': msgId, 'msgSrc': msgSrc, 'msgType': msgType, 'requestTimestamp': requestTimestamp,
                'merOrderId': merOrderId, 'mid': mid, 'tid': tid, 'totalAmount': totalAmount,
                'subOpenId': subOpenId,'goods':goods,
                'tradeType': tradeType, 'subAppId': subAppId, 'subOpenId': subOpenId, 'instMid': instMid
            }
        wmm_list = list(wmm_json.keys())
        list.sort(wmm_list)
        wmm_str = ''
        for one in wmm_list:
            if wmm_json[one] == '' or wmm_json[one] == None:
                pass
            else:
                if one == 'goods':
                    wmm_str = wmm_str+one+'='+json.dumps(wmm_json[one]).encode('utf-8').decode('unicode_escape').replace(' ','')+'&'
                else:
                    wmm_str = wmm_str+one+'='+wmm_json[one]+'&'
        wmm_str = wmm_str.rstrip('&')
        wmm_str = wmm_str + scrit_key
        import hashlib
        wmm_sign = hashlib.md5(wmm_str.encode('utf-8')).hexdigest()
        wmm_json['sign'] = wmm_sign
        import requests
        r = requests.post(
            'https://qr.chinaums.com/netpay-route-server/api/', json=wmm_json
        )
        json_res = r.json()
        print(json_res)
        from . import models
        models.ding_can_chinaums_pay_order_res_col(json_res=json_res,openid=wx_login_get_openid_dict['openid']).save()
        if json_res['errCode'] == 'SUCCESS':
            return  {'描述': '成功', 'miniPayRequest': json_res['miniPayRequest']}
        else:
            return  {'描述': '失败', 'miniPayRequest': {}}
    except:
        print(traceback.format_exc())
        return {'描述': '500', 'miniPayRequest': {}}
