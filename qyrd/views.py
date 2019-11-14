from django.shortcuts import render

# Create your views here.

def 人大要闻(request):
    from . import models
    from django.http import HttpResponse
    import traceback
    qset0 = models.青阳人大人大要闻.objects.first()
    
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
    # resj = json.loads(request.body)
    # print(resj)
    request_body = request.body
    # print(request.body)
    import chardet
    request_body_encoding = chardet.detect(request_body)['encoding']
    print(request_body_encoding)
    if request_body_encoding == None:
        request_body_encoding = 'GB2312'
    ano_data = request.body.decode(request_body_encoding)
    # print(ano_data)
    import re
    import time
    当前时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    n = re.findall(r"{\"article\":\"(.+?)\",\"tittle\":\"(.+?)\",\"type\":\"(.+?)\"}", ano_data)
    if n != []:
        article = n[0][0]
        tittle = n[0][1]
        type = n[0][2]
        qset1 = models.qyrd_article_col.objects(tittle=tittle,type=type).first()
        if qset1 == None:
            models.qyrd_article_col(article=ano_data,tittle=tittle,type=type,my_time=当前时间).save()
        else:
            qset1.update(article=ano_data,my_time=当前时间)
        response = HttpResponse(ano_data.encode(request_body_encoding))
    else:
        response = HttpResponse('{"article":"<p>输入有误！</p>","tittle":"","type":""}')
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
    

def images(request):
    try:
        id = request.GET['id']
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
            image = qset.qyrd_image_col.read()
            response = HttpResponse(image)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="ano.jpg"'
            return response
    except:
        import traceback
        import myConfig
        from django.http import HttpResponse, FileResponse
        print(traceback.format_exc())
        path = myConfig.django_root_path + '/' + 'mysite' + '/' + '404.png'
        outfile = open(path, 'rb')
        response = FileResponse(outfile)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s"' % "image.jpg"
        return response