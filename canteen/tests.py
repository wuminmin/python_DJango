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
pipeline = [
    {
        "$group": {
            "$match": {
                "产品.包子.签到": "没吃"
            }
        },
         "myCount": {
            "$sum": 1
        }


    }


]
r = models.订餐结果临时表.objects.aggregate(*pipeline)
print(list(r))
# print(r.to_json().encode('utf-8').decode('unicode_escape'))
