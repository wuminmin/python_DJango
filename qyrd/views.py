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
    resj = json.loads(request.body)
    print(resj)
    ano_data = request.body.decode('utf-8')
    # import re
    # n = re.findall(r"{\"params\":{\"myState\":{\"outputHTML\":\"(.+?)\"}}}", ano_data)
    # if n != []:
    #     res2 = n[0]
    #     print(res2)
    # else:
    #     res2 = ''
    # print(res2)
    res = ano_data.encode('utf-8')
    response = HttpResponse( res)
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