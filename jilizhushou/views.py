from django.shortcuts import render

# Create your views here.


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
        type = request.POST['type']
        now = request.POST['now']
        当前月 = str(datetime.datetime.now().year) + '年' + \
            str(datetime.datetime.now().month)+'月'
        qset1 = models.ji_li_zhu_shou_article.objects(
            tittle=tittle, type=type).first()
        if qset1 == None:
            models.ji_li_zhu_shou_article(
                article=article,
                tittle=tittle,
                type=type,
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

    # request_body = request.body
    # import chardet
    # request_body_encoding = chardet.detect(request_body)['encoding']
    # print(request_body_encoding)
    # if request_body_encoding == None:
    #     request_body_encoding = 'GB2312'
    # ano_data = request.body.decode(request_body_encoding)
    # import re
    # import time
    # import datetime
    # 当前月 = str(datetime.datetime.now().year) + '年'+str(datetime.datetime.now().month)+'月'
    # n = re.findall(
    #     r"{\"article\":\"(.+?)\",\"tittle\":\"(.+?)\",\"type\":\"(.+?)\",\"now\":\"(.+?)\"}", ano_data)
    # if n != []:
    #     # article = n[0][0]
    #     tittle = n[0][1]
    #     type = n[0][2]
    #     now = n[0][3]
    #     qset1 = models.qyrd_article_col.objects(
    #         tittle=tittle, type=type).first()
    #     if qset1 == None:
    #         models.qyrd_article_col(
    #             article=ano_data,
    #             tittle=tittle,
    #             type=type,
    #             my_time = now,
    #             my_date = datetime.datetime.now(),
    #             my_month = 当前月,
    #             other={'request_body_encoding': request_body_encoding}).save()
    #     else:
    #         qset1.update(
    #             article=ano_data,
    #             my_time = now,
    #             my_date = datetime.datetime.now(),
    #             my_month = 当前月,
    #             other={'request_body_encoding': request_body_encoding})
    #     response = HttpResponse(ano_data.encode(request_body_encoding))
    # else:
    #     response = HttpResponse(
    #         '{"article":"<p>输入有误！</p>","tittle":"","type":""}')
    # response["Access-Control-Allow-Origin"] = "*"
    # response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    # response["Access-Control-Max-Age"] = "1000"
    # response["Access-Control-Allow-Headers"] = "*"
    # return response


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
    mytype = request.POST['type']
    import myConfig
    from pymongo import MongoClient
    client = MongoClient('mongodb://' + myConfig.username + ':' + myConfig.password +
                         '@' + str(myConfig.host) + ':' + str(myConfig.port) + '/'+myConfig.db)
    db = client['mydb']
    r = db.qyrd_article_col.find({'type': mytype}).sort([("_id", -1)])
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
    mytype = request.POST['type']
    import myConfig
    from pymongo import MongoClient
    client = MongoClient('mongodb://' + myConfig.username + ':' + myConfig.password +
                         '@' + str(myConfig.host) + ':' + str(myConfig.port) + '/'+myConfig.db)
    db = client['mydb']
    r = db.qyrd_article_col.find({'type': mytype}).sort([("_id", -1)]).limit(6)
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
        qset2 = models.ji_li_zhu_shou_article.objects(type=myVar2).first()
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
        qset2 = models.ji_li_zhu_shou_article.objects(type=myVar2).first()
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
    myVar = request.POST['type']
    print('根据栏目下载目录', myVar)
    # import myConfig
    # from pymongo import MongoClient
    # client = MongoClient('mongodb://' + myConfig.username + ':' + myConfig.password + '@' + str(myConfig.host) + ':' + str(myConfig.port) + '/'+myConfig.db)
    # db = client['mydb']
    qset1 = models.ji_li_zhu_shou_article.objects(type=myVar)
    myVar2 = []
    myVar3 = []
    for one in qset1:
        if one.my_month in myVar2:
            pass
        else:
            myVar2.append(one.my_month)
    for one in myVar2:
        myVar4 = []
        qset2 = models.ji_li_zhu_shou_article.objects(type=myVar, my_month=one)
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
        qset2 = models.ji_li_zhu_shou_article.objects(type=one).limit(10)
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
        qset1 = models.ji_li_zhu_shou_userinfo.objects(
            usertoken=myVar1).first()
        if qset1 == None:
            r_dict = {
                'username': '',
                'userphone': '',
                'userrole': '',
                'mainid': '',
                'type1': '',
                'type2': '',
                'type3': ''
            }
            response = HttpResponse(json.dumps(r_dict))
        else:
            
            r_dict = {
                'username': qset1.username,
                'userphone': qset1.userphone,
                'userrole': qset1.userrole,
                'mainid': qset1.mainid,
                'type1': qset1.type1,
                'type2': qset1.type2,
                'type3': qset1.type3
            }
            response = HttpResponse(json.dumps(r_dict))
    except:
        response = HttpResponse(
            json.dumps({
                'username': '',
                'userphone': '',
                'userrole': '',
                'mainid': '',
                'type1': '',
                'type2': '',
                'type3': ''
            })
        )
        import traceback
        print(traceback.format_exc())
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def 兑现激励上传文件(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    import myConfig
    myfile = request.FILES.get("file", None)
    # uploaded_filename = 'file.xlsx'
    # folder = request.path.replace("/", "_")
    # print(myConfig.django_root_path + '/'+folder+ '/'+uploaded_filename)
    # with open(myConfig.django_root_path + '/'+folder+ '/'+uploaded_filename , 'wb+') as destination:
    #                     for chunk in myfile.chunks():
    #                         destination.write(chunk)
    import pandas as pd
    df1 = pd.read_excel(myfile)
    r = df1.head(10)
    print(r)
    for index, row in df1.iterrows():
        主数据工号 = row['主数据工号']
        活动名称 = row['活动名称']
        销售品编码 = row['销售品编码']
        激励金额 = row['激励金额']
        激励账期 = row['激励账期']
        银行卡 = row['银行卡']
        qset1 = models.ji_li_zhu_shou_dui_xian_qing_dan.objects(sellid=销售品编码).first()
        if qset1 == None:
            models.ji_li_zhu_shou_dui_xian_qing_dan(
                mainid=str(主数据工号),
                tittle=活动名称,
                sellid=销售品编码,
                money=激励金额,
                mydate=str(激励账期),
                bankid=银行卡,
                mystate=models.mystate1
            ).save()
        else:
            qset1.update(
                 mainid=主数据工号,
                tittle=活动名称,
                money=激励金额,
                mydate=激励账期,
                bankid=银行卡,
                mystate=models.mystate1
            )
    response = HttpResponse('成功')
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
    response = HttpResponse(json.dumps(myVar2list).encode('utf-8').decode('unicode_escape'))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response