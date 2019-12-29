from django.test import TestCase
import json
import sys, os
root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_path)
# Create your tests here.

# res = '{"key":"<p></p><div class=\"media-wrap image-wrap\"><img src=\"data:image/png;base64,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\"/></div><p>你好，<strong>世界!</strong></p><p></p>","type":"人大要闻"}'

# res_j = json.loads(res)

# print(res_j['firstName'])

# import re
# n = re.findall(r"{\"key\":\"(.+?)\",\"type\":\"(.+?)\"}", res)
# print(n)
# if n != []:
#     key = n[0][0]
#     type = n[0][1]
#     print(key)
#     print(type)


# import chardet
# data = '离离原上草，一岁一枯荣'.encode('gbk')
# r = chardet.detect(data)
# print(r['encoding'])


# from qyrd import models
# from django.http import HttpResponse
# import traceback
# import myConfig
# from pymongo import MongoClient
# client = MongoClient('mongodb://' + myConfig.username + ':' + myConfig.password + '@' + str(myConfig.host) + ':' + str(myConfig.port) + '/'+myConfig.db)
# db = client['mydb']
# r = db.qyrd_article_col.find({'type':'首页新闻'}).sort([("_id", -1)])
# from bson import json_util 
# import json
# j = {}
# j['article'] = r[0]['article']
# j['type'] = r[0]['type']
# j['tittle'] = r[0]['tittle']
# j['my_time'] = r[0]['my_time']
# j['other'] = r[0]['other']
# r = json.dumps(j).encode('utf-8').decode('unicode_escape')
# print(r)


# r = [{'tittle':'1111','my_time':'22222'}]
# r = {'tittle':'1111','my_time':'22222'}
# r = json.dumps(r)
# print(r)
# import datetime
# now = datetime.datetime.now()
# print( str(now.year) + '年'+str(now.month)+'月' )

# import myConfig
# from pymongo import MongoClient
# client = MongoClient('mongodb://' + myConfig.username + ':' + myConfig.password + '@' + str(myConfig.host) + ':' + str(myConfig.port) + '/'+myConfig.db)
# db = client['mydb']
# r = db.qyrd_article_col.aggregate([
#   { "$match": { "type": "人大要闻" }},
#   { "$group": {
#     "_id": { "$month": "$date" },
#     "tittle": {
#       "$push": "$$ROOT"
#     }
#   }}
# ])
# r = db.qyrd_article_col.aggregate( [
#    {
#      "$group": {
#         "_id": {
#            "cust_id": "$cust_id",
#            "my_date": {
#                "month": { "$month": "$my_date" },
#                "day": { "$dayOfMonth": "$my_date" },
#                "year": { "$year": "$my_date"}
#            }
#         },
#         "tittle": "&tittle"
#      }
#    }
# ] )
# print(list(r))

# from . import models
# qset1 = models.qyrd_article_col.objects(type=myVar)
# print(qset1.to_json())

import requests
wmmurl = 'http://t.weather.sojson.com/api/weather/city/101221703'
r = requests.get(url=wmmurl)
r_json = json.loads(r.text)
print(r_json)