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
        usertoken = request.POST['usertoken']
        qset1 = models.qyrd_userinfo.objects(usertoken=usertoken).first()
        if qset1 == None:
            response = HttpResponse(json.dumps({'code': '非法用户'}))
        else:
            article = request.POST['article']
            tittle = request.POST['tittle']
            type = request.POST['type']
            now = request.POST['now']
            当前月 = str(datetime.datetime.now().year) + '年' + \
                str(datetime.datetime.now().month)+'月'
            qset1 = models.qyrd_article_col.objects(
                tittle=tittle, type=type).first()
            if qset1 == None:
                models.qyrd_article_col(
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
            response = HttpResponse(json.dumps({'code': '上传成功'}))
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
        qset2 = models.qyrd_article_col.objects(type=myVar2).first()
        if qset2 == None:
            response = HttpResponse('')
        else:
            response = HttpResponse(qset2.article)
    else:
        import myConfig
        qset1 = models.qyrd_article_col.objects(tittle=myVar).first()
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
        qset2 = models.qyrd_article_col.objects(type=myVar2).first()
        if qset2 == None:
            response = HttpResponse(
                '{\"tittle\":\"没有文章\",\"my_time\":\"没有文章\"}')
        else:
            response = HttpResponse(
                '{\"tittle\":\"' + qset2.tittle + '\",\"my_time\":\"'+qset2.my_time+'\"}')
    else:
        import myConfig
        qset1 = models.qyrd_article_col.objects(tittle=myVar).first()
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
        qset2 = models.qyrd_article_col.objects(type=myVar, my_month=one)
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
        qset2 = models.qyrd_article_col.objects(type=one).limit(10)
        for one2 in qset2:
            print(one2.my_date.month)
            print(one2.my_date.day)
            myVar4.append({'key': one2.tittle,
                           'key2': str(one2.my_date.month)+'-'+str(one2.my_date.day),
                           'img_src':'https://wx.wuminmin.top/qyrd/image?id=新闻图片1',
                           'url': '/mynews?ban_kuai='+myVar+'&lan_mu='+one+'&tittle='+one2.tittle
                           })
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


def upload_img(request):
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
        qset1 = models.qyrd_userinfo.objects(usertoken=usertoken).first()
        if qset1 == None:
            response = HttpResponse(json.dumps({'code': '非法用户'}))
        else:
            file_object = request.FILES['file'].file
            qset2 = models.qyrd_image_col.objects(col_id=tittle).first()
            if qset2 == None:
                models.qyrd_image_col(
                    col_id=tittle,
                    col_image=file_object
                ).save()
            else:
                qset2.delete()
                models.qyrd_image_col(
                    col_id=tittle,
                    col_image=file_object
                ).save()
            response = HttpResponse(json.dumps({'code': '成功'}))
    except:
        import traceback
        print(traceback.format_exc())
        response = HttpResponse(json.dumps({'code': '系统错误'}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def 天气下载(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    import myConfig
    try:
        import requests
        wmmurl = 'http://t.weather.sojson.com/api/weather/city/101221703'
        r = requests.get(url=wmmurl)
        r_json = json.loads(r.text)
        response = HttpResponse(json.dumps(r_json))
    except:
        import traceback
        print(traceback.format_exc())
        response = HttpResponse(json.dumps({'code': '系统错误'}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def get_headermenu_list_data(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    import myConfig
    try:
        mylist = []
        首页 = models.ban_kuai_lan_mu_dict['首页']
        新闻中心 = models.ban_kuai_lan_mu_dict['新闻中心']
        人大概况 = models.ban_kuai_lan_mu_dict['人大概况']
        依法履职 = models.ban_kuai_lan_mu_dict['依法履职']
        代表工作 = models.ban_kuai_lan_mu_dict['代表工作']
        会议之窗 = models.ban_kuai_lan_mu_dict['会议之窗']
        一府一委两院 = models.ban_kuai_lan_mu_dict['一府一委两院']
        乡镇人大 = models.ban_kuai_lan_mu_dict['乡镇人大']
        mylist.append({'name': '首页', 'mymenu': 首页})
        mylist.append({'name': '新闻中心', 'mymenu': 新闻中心})
        mylist.append({'name': '人大概况', 'mymenu': 人大概况})
        mylist.append({'name': '依法履职', 'mymenu': 依法履职})
        mylist.append({'name': '代表工作', 'mymenu': 代表工作})
        mylist.append({'name': '会议之窗', 'mymenu': 会议之窗})
        mylist.append({'name': '一府一委两院', 'mymenu': 一府一委两院})
        mylist.append({'name': '乡镇人大', 'mymenu': 乡镇人大})
        headermenu_list_data = []
        for one in mylist:
            myMenu = []
            for one2 in one['mymenu']:
                if one2 == '首页':
                    myMenu.append({'subname': one2, 'subUrl': '/'})
                else:
                    myMenu.append(
                        {'subname': one2, 'subUrl': '/mynews?ban_kuai='+one['name']+'&lan_mu='+one2+'&tittle=默认'})
            headermenu_list_data.append(
                {
                    'name': one['name'],
                    'myMenu': myMenu
                }
            )
        response = HttpResponse(json.dumps(headermenu_list_data))
    except:
        import traceback
        print(traceback.format_exc())
        response = HttpResponse(json.dumps([]))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def login(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    import myConfig
    import datetime 
    try:
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        qyrd_userinfo1 = models.qyrd_userinfo.objects(username=username,userpwd=password).first()
        if qyrd_userinfo1 == None:
            response = HttpResponse(json.dumps({'code':'201','usertoken':''}))
        else:
            usertoken = str( datetime.datetime.now() )
            qyrd_userinfo1.update(usertoken=usertoken)
            response = HttpResponse(json.dumps({'code':'200','usertoken':usertoken}))
    except:
        import traceback
        print(traceback.format_exc())
        response = HttpResponse(json.dumps({'code':'500','usertoken':''}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
