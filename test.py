from canteen import models
from django.test import TestCase

# Create your tests here.
import sys
import os
root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_path)

# r = models.订餐结果临时表.objects(__raw__ = {
#     "$aggregate":{
#     "产品.包子.签到":"没吃",

#     }
#     })

# from . import models
产品名称 = '包子'
日期_list_one = '2020-01-13'
pipeline = [
    {
        "$match": {
            "产品."+产品名称+".预定数量": {
                "$gte":1
            },
            # "产品."+产品名称+".签到":"没吃",
            "用餐日期":日期_list_one
        }
    }
    ,
    {
        "$group": {
            "_id": "null",
            产品名称: {
                "$sum": "$产品."+产品名称+".预定数量"
            }
        }
    }
]
for r in list(models.订餐结果表.objects.aggregate(*pipeline)):
    print(r)
    
# r = models.订餐结果表.objects.aggregate(*pipeline)
# print((list(r)))
# print(r.to_json().encode('utf-8').decode('unicode_escape'))


# lll = [{'_id': 'null', '包子': 7}]
# print(lll[0]['包子'])
