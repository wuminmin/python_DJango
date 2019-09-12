from django.shortcuts import render
import myConfig
import datetime
import json
import traceback
import uuid
import os
import pandas
import requests
import time
from django.http import HttpResponse, FileResponse
# Create your views here.
from . import models
import datetime
import hashlib
import json
import traceback
import uuid

import pandas
import pytz
import requests
import time
from django.http import HttpResponse
from django.shortcuts import render_to_response

import myConfig
from myConfig import appid, secret, grant_type, sign_name, template_code, django_root_path
import sys

#微信认证
def wx(request):
    signature = request.GET["signature"]
    timestamp = request.GET["timestamp"]
    nonce = request.GET["nonce"]
    echostr = request.GET["echostr"]
    token = myConfig.wx_token
    list = [token, timestamp, nonce]
    list.sort()
    list2 = ''.join(list)
    sha1 = hashlib.sha1()
    sha1.update(list2.encode('utf-8'))
    hashcode = sha1.hexdigest()
    if hashcode == signature:
        return HttpResponse(echostr)
    else:
        return HttpResponse(echostr)

def images(request):
    try:
        id = request.GET['id']
        qset = models.wxyl_image_col.objects(wxyl_id=id).first()
        print(qset)
        if qset == None:
            path = myConfig.django_root_path + '/' + 'mysite' + '/' + '404.png'
            outfile = open(path, 'rb')
            response = FileResponse(outfile)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="%s"' % "image.jpg"
            return response
        else:
            image = qset.wxyl_image.read()
            response = HttpResponse(image)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="ano.jpg"'
            return response
    except:
        print(traceback.format_exc())
        path = myConfig.django_root_path + '/' + 'mysite' + '/' + '404.png'
        outfile = open(path, 'rb')
        response = FileResponse(outfile)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s"' % "image.jpg"
        return response