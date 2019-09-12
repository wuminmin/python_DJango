from django.db import models

# Create your models here.

from mongoengine import *

# 数据库连接
import sys, os
root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
print(root_path )
sys.path.append(root_path)
print(sys.path)

import myConfig


connect(db=myConfig.db, host=myConfig.host, port=myConfig.port, username=myConfig.username, password=myConfig.password)


class  wxyl_image_col(Document):
    wxyl_id = StringField()
    wxyl_image = ImageField()

def save_image(id,path):
    outfile = open(path, 'rb')
    qset = wxyl_image_col.objects(wxyl_id=id).first()
    if qset == None:
        wxyl_image_col(
            wxyl_id = id,
            wxyl_image = outfile
        ).save()
    else:
        qset.update(
            wxyl_id = '1',
            wxyl_image = outfile
        )
if __name__ == '__main__':
    save_image('1','D:\WMM\皱燕民\景观工程（假山、驳岸）\微信图片_20190320114217.jpg')