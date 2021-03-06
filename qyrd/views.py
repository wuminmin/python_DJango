from django.shortcuts import render
from . import db,tool
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
    import myConfig
    from django.http import HttpResponse, FileResponse
    try:
        id = request.GET['id']
        print(id)
        qset = models.qyrd_image_col.objects(col_id=id).first()
        print(qset)
        if qset == None:
            path = myConfig.django_root_path + '/' + 'mysite' + '/' + '404'
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
        path = myConfig.django_root_path + '/' + 'mysite' + '/' + '404'
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
    # from pymongo import MongoClient
    # client = MongoClient('mongodb://' + myConfig.username + ':' + myConfig.password +
    #                      '@' + str(myConfig.host) + ':' + str(myConfig.port) + '/'+myConfig.db)
    # db = client['mydb']
    # qyrd_article_col2 = list( models.qyrd_article_col.objects(type=mytype).limit(10).order_by('-my_date') )
    # r = db.qyrd_article_col.find({'type': mytype}).sort([("_id", -1)])
    r = list(models.qyrd_article_col.objects(
        type=mytype).limit(10).order_by('-my_date'))
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
    print(myVar)
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
            res = {'tittle': '没有文章', 'my_time': '没有文章', 'count': 0}
            response = HttpResponse(json.dumps(res).encode(
                'utf-8').decode('unicode_escape'))
        else:
            if 'count' in qset2.other:
                count = qset2.other['count']+1
                other = qset2.other
                other['count'] = count
                qset2.update(other=other)
            else:
                count = 1
                other = qset2.other
                other['count'] = count
                qset2.update(other=other)
            res = {'tittle': qset2.tittle,
                   'my_time': qset2.my_time, 'count': count}
            response = HttpResponse(json.dumps(res).encode(
                'utf-8').decode('unicode_escape'))
    else:
        import myConfig
        qset1 = models.qyrd_article_col.objects(tittle=myVar).first()
        if qset1 == None:
            res = {'tittle': '没有文章', 'my_time': '没有文章', 'count': 0}
            response = HttpResponse(json.dumps(res).encode(
                'utf-8').decode('unicode_escape'))
        else:
            if 'count' in qset1.other:
                count = qset1.other['count']+1
                other = qset1.other
                other['count'] = count
                qset1.update(other=other)
            else:
                count = 1
                other = qset1.other
                other['count'] = count
                qset1.update(other=other)
            res = {'tittle': myVar, 'my_time': qset1.my_time, 'count': count}
            response = HttpResponse(json.dumps(res).encode(
                'utf-8').decode('unicode_escape'))
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
    qset1 = models.qyrd_article_col.objects(type=myVar).order_by('-my_date')
    myVar2 = []
    myVar3 = []
    for one in qset1:
        if one.my_month in myVar2:
            pass
        else:
            myVar2.append(one.my_month)
    for one in myVar2:
        myVar4 = []
        qset2 = models.qyrd_article_col.objects(
            type=myVar, my_month=one).order_by('-my_date')
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
    if myVar == '新闻中心':
        limit1 = 10
    elif myVar == '':
        limit1 = 7
    else:
        limit1 = 7

    for one in myVar2:
        myVar4 = []
        qset2 = models.qyrd_article_col.objects(
            type=one).limit(limit1).order_by('-my_date')
        for one2 in qset2:
            myVar4.append({
                '图片名称': one2.tittle,
                '网页地址': '/#/myimggrid?ban_kuai='+myVar+'&lan_mu='+one+'&tittle=默认',
                '图片地址': 'https://wx.wuminmin.top/qyrd/image?id='+one+'-'+one2.tittle,
                'key': one2.tittle,
                'key2': str(one2.my_date.year)+'-'+str(one2.my_date.month)+'-'+str(one2.my_date.day),
                'img_src': 'https://wx.wuminmin.top/qyrd/image?id=新闻图片1',
                'url': '/mynews?ban_kuai='+myVar+'&lan_mu='+one+'&tittle='+one2.tittle
            })
        myVar3.append({
            'table_key': i,
            'table_name': one,
            'list_data': myVar4
        })
        i = i+1
    response = HttpResponse(json.dumps(myVar3))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def rd_xia_zai_tabs_by_ban_kuai2(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    myVar = request.POST['ban_kuai']
    myVar2 = models.ban_kuai_lan_mu_dict[myVar]
    myVar3 = []
    i = 0
    for one in myVar2:
        myVar4 = []
        qset2 = models.qyrd_article_col.objects(
            type=one).limit(12).order_by('-my_date')
        sub_list_data = []
        for one2 in qset2:
            myVar4.append({
                '图片名称': one2.tittle,
                '网页地址': '/#/myimggrid?ban_kuai='+myVar+'&lan_mu='+one+'&tittle=默认',
                '图片地址': 'https://wx.wuminmin.top/qyrd/image?id='+one+'-'+one2.tittle,
                'key': one2.tittle,
                'key2': str(one2.my_date.year)+'-'+str(one2.my_date.month)+'-'+str(one2.my_date.day),
                'img_src': 'https://wx.wuminmin.top/qyrd/image?id=新闻图片1',
                'url': '/mynews?ban_kuai='+myVar+'&lan_mu='+one+'&tittle='+one2.tittle
            })
            if len(myVar4) == 3:
                sub_list_data.append(
                    {'sub_list_data': myVar4}
                )
                myVar4 = []
        sub_list_data.append(
            {'sub_list_data': myVar4}
        )
        myVar3.append({
            'table_key': i,
            'table_name': one,
            'list_data': sub_list_data
        })
        i = i+1
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
                        {
                            'subname': one2,
                            'subUrl': 'my_lan_mu?ban_kuai='+one['name']+'&lan_mu='+one2
                            # 'subUrl': '/mynews?ban_kuai='+one['name']+'&lan_mu='+one2+'&tittle=默认'
                        }
                    )
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


def get_headermenu_list_data2(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    import myConfig
    try:
        mylist = []
        首页 = models.ban_kuai_lan_mu_dict['首页']
        首页图片 = models.ban_kuai_lan_mu_dict['首页图片']
        首页滚动 = models.ban_kuai_lan_mu_dict['首页滚动']
        新闻中心 = models.ban_kuai_lan_mu_dict['新闻中心']
        人大概况 = models.ban_kuai_lan_mu_dict['人大概况']
        依法履职 = models.ban_kuai_lan_mu_dict['依法履职']
        代表工作 = models.ban_kuai_lan_mu_dict['代表工作']
        会议之窗 = models.ban_kuai_lan_mu_dict['会议之窗']
        一府一委两院 = models.ban_kuai_lan_mu_dict['一府一委两院']
        乡镇人大 = models.ban_kuai_lan_mu_dict['乡镇人大']
        mylist.append({'name': '首页', 'mymenu': 首页})
        mylist.append({'name': '首页图片', 'mymenu': 首页图片})
        mylist.append({'name': '首页滚动', 'mymenu': 首页滚动})
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
        print(username, password)
        qyrd_userinfo1 = models.qyrd_userinfo.objects(
            username=username, userpwd=password).first()
        if qyrd_userinfo1 == None:
            response = HttpResponse(json.dumps(
                {'code': '201', 'usertoken': ''}))
        else:
            usertoken = str(datetime.datetime.now())
            qyrd_userinfo1.update(usertoken=usertoken)
            response = HttpResponse(json.dumps(
                {'code': '200', 'usertoken': usertoken}))
    except:
        import traceback
        print(traceback.format_exc())
        response = HttpResponse(json.dumps({'code': '500', 'usertoken': ''}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def upload_img2(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    import myConfig
    try:
        print(request.FILES)
        print(request.POST)
        usertoken = request.POST['usertoken']
        当前模块 = request.POST['subname']
        当前图片名称 = request.POST['tittle']
        print('upload_img2--------------------', 当前模块, 当前图片名称)
        qset1 = models.qyrd_userinfo.objects(usertoken=usertoken).first()
        if qset1 == None:
            response = HttpResponse(json.dumps({'code': '非法用户'}))
        else:
            file_object = request.FILES['file'].file
            qset3 = models.qyrd_article_col.objects(
                type=当前模块, tittle=当前图片名称).first()
            if qset3 == None:
                models.qyrd_article_col(
                    my_month=当前模块,
                    type=当前模块,
                    tittle=当前图片名称
                ).save()
            else:
                pass
            qyrd_id = 当前模块+'-'+当前图片名称
            qset2 = models.qyrd_image_col.objects(col_id=qyrd_id).first()
            if qset2 == None:
                models.qyrd_image_col(
                    col_id=qyrd_id,
                    col_image=file_object
                ).save()
            else:
                qset2.delete()
                models.qyrd_image_col(
                    col_id=qyrd_id,
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


def get_tablei_data_by_lan_mu_key(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    import myConfig
    try:
        ban_kuai = request.POST['ban_kuai']
        lan_mu_key = request.POST['lan_mu_key']
        lan_mu = models.ban_kuai_lan_mu_dict[ban_kuai][int(lan_mu_key)]
        qset1 = models.qyrd_article_col.objects(type=lan_mu).order_by('-my_date')
        res_list = []
        i = 0
        for one in qset1:
            i = i+1
            if 'count' in one.other:
                address = one.other['count']
            else:
                address = 0
            res_list.append(
                {
                    'key': i,
                    'name': {
                        '标题': one.tittle,
                        '地址': 'mynews?ban_kuai='+ban_kuai+'&lan_mu='+lan_mu+'&tittle='+one.tittle
                    },
                    'age': str(one.my_date.year)+'-'+str(one.my_date.month)+'-'+str(one.my_date.day),
                    'address': address,
                }
            )
        response = HttpResponse(json.dumps(
            {'code': '成功', 'res_list': res_list}))
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    except:
        import traceback
        print(traceback.format_exc())
        response = HttpResponse(json.dumps({'code': '系统错误', 'res_list': []}))
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response


def get_tablei_data_by_lanmu(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    import myConfig
    try:
        ban_kuai = request.POST['ban_kuai']
        lan_mu = request.POST['lan_mu']
        r = db.根据栏目查询文章列表(lan_mu)
        res_list = []
        i = 0
        for one in r:
            i = i+1
            if 'count' in one['other']:
                address = one['other']['count']
            else:
                address = 0
            res_list.append(
                {
                    'key': i,
                    'name': {
                        '标题': one['tittle'],
                        '地址': 'mynews?ban_kuai='+ban_kuai+'&lan_mu='+lan_mu+'&tittle='+one['tittle'],
                    },
                    'age': str(one['my_date'].year)+'-'+str(one['my_date'].month)+'-'+str(one['my_date'].day),
                    'address': address,
                }
            )
        response = HttpResponse(json.dumps(
            {'code': '成功', 'res_list': res_list}))
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    except:
        import traceback
        print(traceback.format_exc())
        response = HttpResponse(json.dumps({'code': '系统错误', 'res_list': []}))
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response


def delete_wz(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    import myConfig
    try:
        tittle = request.POST['tittle']
        lan_mu = request.POST['lan_mu']
        print(tittle, lan_mu)
        qset0 = models.qyrd_article_col.objects(
            type=lan_mu, tittle=tittle).first()
        if qset0 == None:
            response = HttpResponse(json.dumps('文章不存在'))
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
            response["Access-Control-Max-Age"] = "1000"
            response["Access-Control-Allow-Headers"] = "*"
            return response
        else:
            qset0.delete()
            qset1 = models.qyrd_image_col.objects(
                col_id=lan_mu+'-'+tittle).first()
            if qset1 == None:
                pass
            else:
                qset1.delete()
            response = HttpResponse(json.dumps('删除成功'))
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
            response["Access-Control-Max-Age"] = "1000"
            response["Access-Control-Allow-Headers"] = "*"
            return response
    except:
        response = HttpResponse(json.dumps('系统错误'))
        import traceback
        print(traceback.format_exc())
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

def get_tablei_data_by_search(request):
    import json
    from . import models
    from django.http import HttpResponse
    import traceback
    import myConfig
    try:
        tittle = request.POST['tittle']
        print('get_tablei_data_by_search',tittle)
        qset1 = models.qyrd_article_col.objects(tittle__icontains = tittle).order_by('-my_date')
        res_list = []
        i = 0
        for one in qset1:
            i = i+1
            if 'count' in one.other:
                address = one.other['count']
            else:
                address = 0
            res_list.append(
                {
                    'key': i,
                    'name': {
                        '标题': one.tittle,
                        '地址': 'mynews?ban_kuai='+' '+'&lan_mu='+one.type+'&tittle='+one.tittle,
                    },
                    'age': str(one.my_date.year)+'-'+str(one.my_date.month)+'-'+str(one.my_date.day),
                    'address': address,
                }
            )
        response = HttpResponse(json.dumps(
            {'code': '成功', 'res_list': res_list}))
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    except:
        import traceback
        print(traceback.format_exc())
        response = HttpResponse(json.dumps({'code': '系统错误', 'res_list': []}))
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
