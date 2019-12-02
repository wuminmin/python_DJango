from django.shortcuts import render

# Create your views here.


def deprecated_async(f):
    def wrapper(*args, **kwargs):
        from threading import Thread
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def 人大要闻(request):
    from . import models
    from django.http import HttpResponse
    import traceback
    print(traceback.format_exc())
    response = HttpResponse('系统故障')
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def 上传新闻(request):
    from . import models
    from django.http import HttpResponse
    import traceback
    import json
    import datetime
    try:
        article = request.POST['article']
        tittle = request.POST['tittle']
        mylan_mu = request.POST['lan_mu']
        now = request.POST['now']
        当前月 = str(datetime.datetime.now().year) + '年' + \
            str(datetime.datetime.now().month)+'月'
        qset1 = models.ji_li_zhu_shou_article.objects(
            tittle=tittle, lan_mu=mylan_mu).first()
        if qset1 == None:
            models.ji_li_zhu_shou_article(
                article=article,
                tittle=tittle,
                lan_mu=mylan_mu,
                my_time=now,
                my_date=datetime.datetime.now(),
                my_month=当前月,
                other={'request_body_encoding': 'utf-8'}
            ).save()
        else:
            qset1.update(
                article=article,
                my_time=now,
                my_date=datetime.datetime.now(),
                my_month=当前月,
                other={'request_body_encoding': 'utf-8'}
            )
        response = HttpResponse('<p>上传成功！</p>')
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    except:
        import traceback
        print(traceback.format_exc())
        response = HttpResponse('<p>上传失败！</p>')
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

def images(request):
    from . import models
    from django.http import HttpResponse, FileResponse
    try:
        id = request.GET['id']
        print(id)
        qset = models.ji_li_zhu_shou_image.objects(col_id=id).first()
        print(qset)
        if qset == None:
            path = myConfig.django_root_path + '/' + 'mysite' + '/' + '404.png'
            outfile = open(path, 'rb')
            response = FileResponse(outfile)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="%s"' % "image.jpg"
            return response
        else:
            image = qset.col_image.read()
            response = HttpResponse(image)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="ano.jpg"'
            return response
    except:
        import traceback
        import myConfig
        print(traceback.format_exc())
        path = myConfig.django_root_path + '/' + 'mysite' + '/' + '404.png'
        outfile = open(path, 'rb')
        response = FileResponse(outfile)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s"' % "image.jpg"
        return response


def 新闻下载(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    mylan_mu = request.POST['lan_mu']
    import myConfig
    from pymongo import MongoClient
    client = MongoClient('mongodb://' + myConfig.username + ':' + myConfig.password +
                         '@' + str(myConfig.host) + ':' + str(myConfig.port) + '/'+myConfig.db)
    db = client['mydb']
    r = db.qyrd_article_col.find({'lan_mu': mylan_mu}).sort([("_id", -1)])
    if r == []:
        response = HttpResponse(
            '{\"article\":\"<p>没有文章</p>\",\"tittle\":\"没有文章\"}')
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    else:
        r2 = []
        for one in r:
            r2.append(one['article'])
        response = HttpResponse(r2)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response


def 新闻列表下载(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    mylan_mu = request.POST['lan_mu']
    import myConfig
    from pymongo import MongoClient
    client = MongoClient('mongodb://' + myConfig.username + ':' + myConfig.password +
                         '@' + str(myConfig.host) + ':' + str(myConfig.port) + '/'+myConfig.db)
    db = client['mydb']
    r = db.qyrd_article_col.find({'lan_mu': mylan_mu}).sort([("_id", -1)]).limit(6)
    if r == []:
        response = HttpResponse('[]')
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    else:
        # r2 = '[{"tittle":"1111","my_time":"22222"}]'
        r2 = []
        for one in r:
            r2.append({'tittle': one['tittle'], 'time': one['my_time']})
        response = HttpResponse(json.dumps(r2))
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response


def 根据标题下载文章(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    myVar = request.POST['tittle']
    if myVar == '默认':
        myVar2 = request.POST['lan_mu']
        qset2 = models.ji_li_zhu_shou_article.objects(lan_mu=myVar2).first()
        if qset2 == None:
            response = HttpResponse('')
        else:
            response = HttpResponse(qset2.article)
    else:
        import myConfig
        qset1 = models.ji_li_zhu_shou_article.objects(tittle=myVar).first()
        if qset1 == None:
            response = HttpResponse('')
        else:
            response = HttpResponse(qset1.article)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def 根据标题下载时间(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    myVar = request.POST['tittle']
    if myVar == '默认':
        myVar2 = request.POST['lan_mu']
        qset2 = models.ji_li_zhu_shou_article.objects(lan_mu=myVar2).first()
        if qset2 == None:
            response = HttpResponse(
                '{\"tittle\":\"没有文章\",\"my_time\":\"没有文章\"}')
        else:
            response = HttpResponse(
                '{\"tittle\":\"' + qset2.tittle + '\",\"my_time\":\"'+qset2.my_time+'\"}')
    else:
        import myConfig
        qset1 = models.ji_li_zhu_shou_article.objects(tittle=myVar).first()
        if qset1 == None:
            response = HttpResponse(
                '{\"tittle\":\"' + myVar + '\",\"my_time\":\"\"}')
        else:
            response = HttpResponse(
                '{\"tittle\":\"' + myVar + '\",\"my_time\":\"'+qset1.my_time+'\"}')
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def 根据栏目下载目录(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    myVar = request.POST['lan_mu']
    print('根据栏目下载目录', myVar)
    # import myConfig
    # from pymongo import MongoClient
    # client = MongoClient('mongodb://' + myConfig.username + ':' + myConfig.password + '@' + str(myConfig.host) + ':' + str(myConfig.port) + '/'+myConfig.db)
    # db = client['mydb']
    qset1 = models.ji_li_zhu_shou_article.objects(lan_mu=myVar)
    myVar2 = []
    myVar3 = []
    for one in qset1:
        if one.my_month in myVar2:
            pass
        else:
            myVar2.append(one.my_month)
    for one in myVar2:
        myVar4 = []
        qset2 = models.ji_li_zhu_shou_article.objects(lan_mu=myVar, my_month=one)
        for one2 in qset2:
            myVar4.append({'标题': one2.tittle, })
        myVar3.append({'月份': one, '新闻标题列表': myVar4})
    response = HttpResponse(json.dumps(myVar3))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def 根据板块下载表格(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    myVar = request.POST['ban_kuai']
    myVar2 = models.ban_kuai_lan_mu_dict[myVar]
    myVar3 = []
    i = 0
    for one in myVar2:
        i = i+1
        myVar4 = []
        qset2 = models.ji_li_zhu_shou_article.objects(lan_mu=one).limit(10)
        for one2 in qset2:
            myVar4.append({'key': one2.tittle, 'key2': one2.my_time,
                           'url': '/mynews?ban_kuai='+myVar+'&lan_mu='+one+'&tittle='+one2.tittle})
        myVar3.append({
            'table_key': i,
            'table_name': one,
            'list_data': myVar4
        })
    response = HttpResponse(json.dumps(myVar3))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def 获取用户信息(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    import myConfig
    try:
        myVar1 = request.POST['usertoken']
        print('获取用户信息',myVar1)
        if myVar1 == '':
            r_dict = {
                'username': '',
                'userphone': '',
                'userrole': '',
                'mainid': '',
                'lan_mu1': '',
                'lan_mu2': '',
                'lan_mu3': ''
            }
            response = HttpResponse(json.dumps(r_dict))
        else:
            qset1 = models.ji_li_zhu_shou_userinfo.objects(
                usertoken=myVar1).first()
            if qset1 == None:
                r_dict = {
                    'username': '',
                    'userphone': '',
                    'userrole': '',
                    'mainid': '',
                    'lan_mu1': '',
                    'lan_mu2': '',
                    'lan_mu3': ''
                }
                response = HttpResponse(json.dumps(r_dict))
            else:
                r_dict = {
                    'username': qset1.username,
                    'userphone': qset1.userphone,
                    'userrole': qset1.userrole,
                    'mainid': qset1.mainid,
                    'lan_mu1': qset1.lan_mu1,
                    'lan_mu2': qset1.lan_mu2,
                    'lan_mu3': qset1.lan_mu3
                }
                response = HttpResponse(json.dumps(r_dict))
    except:
        response = HttpResponse(
            json.dumps({
                'username': '',
                'userphone': '',
                'userrole': '',
                'mainid': '',
                'lan_mu1': '',
                'lan_mu2': '',
                'lan_mu3': ''
            })
        )
        import traceback
        print(traceback.format_exc())
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


@deprecated_async
def 异步处理兑现激励文件(myfile,tittle):
    from . import models
    import pandas as pd
    df1 = pd.read_excel(myfile)
    def save_row_to_mongo(row):
        try:
            主数据工号 = row['主数据工号']
            活动名称 = tittle
            销售品编码 = row['销售品编码']
            激励金额 = row['激励金额']
            激励账期 = row['激励账期']
            银行卡 = row['银行卡']
            print(主数据工号, 活动名称, 销售品编码, 激励金额, 激励账期, 银行卡)
            qset1 = models.ji_li_zhu_shou_dui_xian_qing_dan.objects(sellid=销售品编码).first()
            if qset1 == None:
                models.ji_li_zhu_shou_dui_xian_qing_dan(
                    mainid=str(主数据工号),
                    tittle=str(活动名称),
                    sellid=str(销售品编码),
                    money=float(激励金额),
                    mydate=str(激励账期),
                    bankid=str(银行卡)
                ).save()
            else:
                qset1.update(
                    mainid=str(主数据工号),
                    tittle=str(活动名称),
                    sellid=str(销售品编码),
                    money=float(激励金额),
                    mydate=str(激励账期),
                    bankid=str(银行卡)
                )

        except:
            import traceback
            print(traceback.format_exc())
        return row['主数据工号']
    df1['主数据工号'] = df1.apply(
        save_row_to_mongo, axis=1
    )
    qset2 = models.ji_li_zhu_shou_article.objects(tittle=tittle).first()
    if qset2 == None:
        pass
    else:
        qset2.update( lan_mu = models.ban_kuai1_lan_mu2)

def 兑现激励上传文件(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    import myConfig
    try:
        print(request.FILES)
        print(request.POST)
        usertoken = request.POST['usertoken']
        tittle = request.POST['tittle']
        qset1 = models.ji_li_zhu_shou_userinfo.objects(usertoken=usertoken).first()
        if qset1 == None:
            response = HttpResponse(json.dumps({'code':'非法用户'}))
        else:
            if qset1.userrole == models.userrole2:
                file_object = request.FILES['file'].file
                my_file_name = request.FILES['file'].name
                print(file_object)
                fo = open(my_file_name, "wb")
                fo.write(request.FILES['file'].file.read())
                fo.close()
                异步处理兑现激励文件(my_file_name,tittle)
                response = HttpResponse(json.dumps({'code':'成功'}))
            else:
                response = HttpResponse(json.dumps({'code':'没有权限'}))

    except:
        import traceback
        print(traceback.format_exc())
        response = HttpResponse(json.dumps({'code':'系统错误'}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def 获得活动列表(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    import myConfig
    qset2 = models.ji_li_zhu_shou_article.objects()
    myVar2list = []
    for one in qset2:
        if one.tittle in myVar2list:
            pass
        else:
            myVar2list.append(one.tittle)
    response = HttpResponse(json.dumps(myVar2list).encode(
        'utf-8').decode('unicode_escape'))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def 获得兑现详单(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    import myConfig
    try:
        myVar1 = request.POST['usertoken']
        myVar2 = request.POST['tittle']
        print('获得兑现详单', myVar1, myVar2)
        qset1 = models.ji_li_zhu_shou_userinfo.objects(
            usertoken=myVar1).first()
        if qset1 == None:
            response = HttpResponse(json.dumps([]))
        else:
            if qset1.userrole == models.userrole2:
                qset2 = models.ji_li_zhu_shou_dui_xian_qing_dan.objects(
                    tittle=myVar2
                )
                rlist = []
                i = 0
                for one in qset2:
                    i = i + 1
                    rdict = {
                        'key': str(i),
                        'name': one.mainid,
                        'tittle': one.tittle,
                        'age': one.sellid,
                        'address': one.money,
                        'tags': [str(one.mydate)],
                        'bankid': one.bankid,
                        'mystate': one.mystate
                    }
                    rlist.append(rdict)
                response = HttpResponse(json.dumps(rlist))
            elif qset1.userrole == models.userrole1:
                qset2 = models.ji_li_zhu_shou_dui_xian_qing_dan.objects(
                    tittle = myVar2,
                    mainid =  qset1.mainid
                )
                rlist = []
                i = 0
                for one in qset2:
                    i = i + 1
                    rdict = {
                        'key': str(i),
                        'name': one.mainid,
                        'tittle': one.tittle,
                        'age': one.sellid,
                        'address': one.money,
                        'tags': [str(one.mydate)],
                        'bankid': one.bankid,
                        'mystate': one.mystate
                    }
                    rlist.append(rdict)
                response = HttpResponse(json.dumps(rlist))
            else:
                response = HttpResponse(json.dumps([]))
    except:
        response = HttpResponse(json.dumps([]))
        import traceback
        print(traceback.format_exc())
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

@deprecated_async
def 异步归档活动(tittle):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    import myConfig
    qset1 = models.ji_li_zhu_shou_dui_xian_qing_dan.objects(tittle = tittle,mystate = models.mystate1).first()
    if qset1 == None:
        models.ji_li_zhu_shou_dui_xian_qing_dan.objects(tittle = tittle,mystate = models.mystate2).update(mystate = models.mystate4 )
        models.ji_li_zhu_shou_article.objects(tittle = tittle).first().update(lan_mu = models.ban_kuai1_lan_mu3)

def 根据销售品编号确认收款(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    import myConfig
    try:
        myVar1 = request.POST['usertoken']
        myVar2 = request.POST['sellid']
        qset1 = models.ji_li_zhu_shou_userinfo.objects(
            usertoken=myVar1).first()
        if qset1 == None:
            response = HttpResponse(json.dumps({'code':'用户不存在'}))
        else:
            if qset1.userrole == models.userrole1:
                qset2 = models.ji_li_zhu_shou_dui_xian_qing_dan.objects(sellid=myVar2).first()
                if qset2 == None:
                    response = HttpResponse(json.dumps({'code':'没有权限'}))
                else:
                    qset2.update(mystate=models.mystate2)
                    异步归档活动(qset2.tittle)
                    response = HttpResponse(json.dumps({'code':'成功'}))
            else:
                response = HttpResponse(json.dumps({'code':'角色错误'}))
    except:
        response = HttpResponse(json.dumps({'code':'系统错误'}))
        import traceback
        print(traceback.format_exc())
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def deng_lu(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    import myConfig
    import time
    try:
        myVar1 = request.POST['userphone']
        myVar2 = request.POST['smscode']
        if myVar2 == '':
            response = HttpResponse(json.dumps({'code':'验证码不为空'}))
        else:
            qset1 = models.ji_li_zhu_shou_userinfo.objects(
                userphone=myVar1,userpwd=myVar2).first()
            if qset1 == None:
                response = HttpResponse(json.dumps({'code':'账号或者密码不正确'}))
            else:
                usertoken = myVar1+'_'+str(time.time())
                qset1.update(usertoken = usertoken )
                response = HttpResponse(json.dumps({'code':'成功','usertoken':usertoken}))
    except:
        response = HttpResponse(json.dumps({'code':'系统错误'}))
        import traceback
        print(traceback.format_exc())
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def send_sms(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    import myConfig
    try:
        myVar1 = request.POST['userphone']
        qset1 = models.ji_li_zhu_shou_userinfo.objects(
            userphone=myVar1).first()
        if qset1 == None:
            response = HttpResponse(json.dumps({'code':'用户不存在'}))
        else:
            import random
            j = 6
            验证码 = ''.join(str(i) for i in random.sample(range(0, 9), j))  # sample(seq, n) 从序列seq中选择n个随机且独立的元素；
            import uuid
            __business_id = uuid.uuid1()
            params = "{\"code\":\"" + 验证码 + "\"}"
            from mysite.demo_sms_send import send_sms
            r = send_sms(__business_id, qset1.userphone, myConfig.sign_name, myConfig.template_code, params)
            r2 = json.loads(r)
            if r2['Code'] == 'OK':
                qset1.update(userpwd = 验证码 )
                response = HttpResponse(json.dumps({'code':'成功'}))
            else:
                response = HttpResponse(json.dumps({'code':'号码不正确'}))
    except:
        response = HttpResponse(json.dumps({'code':'系统错误'}))
        import traceback
        print(traceback.format_exc())
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

@deprecated_async
def 异步处理人员清单文件(myfile,tittle):
    from . import models
    import pandas as pd
    df1 = pd.read_excel(myfile)
    def save_row_to_mongo(row):
        try:
            username = row['姓名']
            userphone = row['手机号']
            userrole = row['角色']
            mainid = row['主数据编号']
            lan_mu1 = row['三级单元']
            lan_mu2 = row['四级单元']
            lan_mu3 = row['五级单元']
            qset1 = models.ji_li_zhu_shou_userinfo.objects(userphone=userphone).first()
            if qset1 == None:
                models.ji_li_zhu_shou_userinfo(
                    username=str(username),
                    userphone=str(userphone),
                    userrole=str(userrole),
                    mainid=str(mainid),
                    lan_mu1=str(lan_mu1),
                    lan_mu2 = str(lan_mu2),
                    lan_mu3 = str(lan_mu3)
                ).save()
            else:
                qset1.update(
                    username=str(username),
                    userphone=str(userphone),
                    userrole=str(userrole),
                    mainid=str(mainid),
                    lan_mu1=str(lan_mu1),
                    lan_mu2 = str(lan_mu2),
                    lan_mu3 = str(lan_mu3)
                )
        except:
            import traceback
            print(traceback.format_exc())
        return row['手机号']
    df1['手机号'] = df1.apply(
        save_row_to_mongo, axis=1
    )

def upload_userinfos(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    import myConfig
    try:
        usertoken = request.POST['usertoken']
        tittle = request.POST['tittle']
        qset1 = models.ji_li_zhu_shou_userinfo.objects(usertoken=usertoken).first()
        if qset1 == None:
            response = HttpResponse(json.dumps({'code':'非法用户'}))
        else:
            if qset1.userrole == models.userrole2:
                file_object = request.FILES['file'].file
                my_file_name = request.FILES['file'].name
                print(file_object)
                fo = open(my_file_name, "wb")
                fo.write(request.FILES['file'].file.read())
                fo.close()
                异步处理人员清单文件(my_file_name,tittle)
                response = HttpResponse(json.dumps({'code':'成功'}))
            else:
                response = HttpResponse(json.dumps({'code':'没有权限'}))
    except:
        import traceback
        print(traceback.format_exc())
        response = HttpResponse(json.dumps({'code':'系统错误'}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response













