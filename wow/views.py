from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import requests
import json
import myConfig

# Create your views here.
def wow_login(request):
    # code = request.GET['code']
    # print(code)
    # return HttpResponse('{"openid":code}')
    code = request.GET['code']
    js_code = request.GET['code']
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
    payload = {'appid': myConfig.mskj_appid, 'secret': myConfig.mskj_scrit, 'code': js_code,
                'grant_type': myConfig.mskj_grant_type}
    r = requests.get(url=url, params=payload)
    r_json = json.loads(r.text)
    print(r_json)
    print(code)
    res = '{"openid":'+code+'}'
    response = HttpResponse(res)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response