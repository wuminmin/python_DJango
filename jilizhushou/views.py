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
        当前月 = str(datetime.datetime.now().year) + '年'+str(datetime.datetime.now().month)+'月'
        qset1 = models.qyrd_article_col.objects(
            tittle=tittle, type=type).first()
        if qset1 == None:
            models.qyrd_article_col(
                article=article,
                tittle=tittle,
                type=type,
                my_time = now,
                my_date = datetime.datetime.now(),
                my_month = 当前月,
                other={'request_body_encoding': 'utf-8'}
            ).save()
        else:
            qset1.update(
                article = article,
                my_time = now,
                my_date = datetime.datetime.now(),
                my_month = 当前月,
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
        qset = models.qyrd_image_col.objects(col_id=id).first()
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
    client = MongoClient('mongodb://' + myConfig.username + ':' + myConfig.password + '@' + str(myConfig.host) + ':' + str(myConfig.port) + '/'+myConfig.db)
    db = client['mydb']
    r = db.qyrd_article_col.find({'type':mytype}).sort([("_id", -1)])
    if r == []:
        response = HttpResponse( '{\"article\":\"<p>没有文章</p>\",\"tittle\":\"没有文章\"}')
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    else:
        r2 = []
        for one in r:
            r2.append(one['article'])
        response = HttpResponse( r2 )
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
    client = MongoClient('mongodb://' + myConfig.username + ':' + myConfig.password + '@' + str(myConfig.host) + ':' + str(myConfig.port) + '/'+myConfig.db)
    db = client['mydb']
    r = db.qyrd_article_col.find({'type':mytype}).sort([("_id", -1)]).limit(6)
    if r == []:
        response = HttpResponse( '[]')
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    else:
        # r2 = '[{"tittle":"1111","my_time":"22222"}]'
        r2 = []
        for one in r:
            r2.append({'tittle':one['tittle'],'time':one['my_time']})
        response = HttpResponse( json.dumps(r2))
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
        qset2 = models.qyrd_article_col.objects(type=myVar2).first()
        if qset2 == None:
            response = HttpResponse( '')
        else:
            response = HttpResponse( qset2.article)
    else:
        import myConfig
        qset1 = models.qyrd_article_col.objects(tittle=myVar).first()
        if qset1 == None:
            response = HttpResponse( '')
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
        qset2 = models.qyrd_article_col.objects(type=myVar2).first()
        if qset2 == None:
            response = HttpResponse( '{\"tittle\":\"没有文章\",\"my_time\":\"没有文章\"}')
        else:
            response = HttpResponse( '{\"tittle\":\"'+ qset2.tittle +'\",\"my_time\":\"'+qset2.my_time+'\"}')
    else:
        import myConfig
        qset1 = models.qyrd_article_col.objects(tittle=myVar).first()
        if qset1 == None:
            response = HttpResponse( '{\"tittle\":\"'+ myVar +'\",\"my_time\":\"\"}')
        else:
            response = HttpResponse('{\"tittle\":\"'+ myVar +'\",\"my_time\":\"'+qset1.my_time+'\"}')
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
    print('根据栏目下载目录',myVar)
    # import myConfig
    # from pymongo import MongoClient
    # client = MongoClient('mongodb://' + myConfig.username + ':' + myConfig.password + '@' + str(myConfig.host) + ':' + str(myConfig.port) + '/'+myConfig.db)
    # db = client['mydb']
    qset1 = models.qyrd_article_col.objects(type=myVar)
    myVar2 = []
    myVar3 = []
    for one in qset1:
        if one.my_month in myVar2:
            pass
        else:
            myVar2.append(one.my_month)
    for one in myVar2:
        myVar4 = []
        qset2 = models.qyrd_article_col.objects( type = myVar,my_month = one)
        for one2 in qset2:
            myVar4.append({'标题':one2.tittle,})
        myVar3.append({'月份':one,'新闻标题列表':myVar4})
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
        qset2 = models.qyrd_article_col.objects( type = one).limit(10)
        for one2 in qset2:
            myVar4.append({'key':one2.tittle,'key2':one2.my_time,'url':'/mynews?ban_kuai='+myVar+'&lan_mu='+one+'&tittle='+one2.tittle})
        myVar3.append({
            'table_key':i,
            'table_name':one,
            'list_data':myVar4
        })
    response = HttpResponse(json.dumps(myVar3))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response