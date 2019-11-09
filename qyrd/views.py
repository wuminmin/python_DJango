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
    ano_data = request.body.decode('utf-8')
    import re
    n = re.findall(r"{\"params\":{\"myState\":{\"outputHTML\":\"(.+?)\"}}}", ano_data)
    if n != []:
        res2 = n[0]
        print(res2)
    else:
        res2 = ''
    print(res2)
    response = HttpResponse(res2)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response