from django.db import models
from mongoengine import *

# 数据库连接
import sys, os
root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_path)
import myConfig

connect(db=myConfig.db, host=myConfig.host, port=myConfig.port, username=myConfig.username, password=myConfig.password)

class wxyl_image_col(Document):
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
        qset.delete()
        wxyl_image_col(
            wxyl_id = id,
            wxyl_image = outfile
        ).save()

if __name__ == '__main__':
    save_image('1','D:\WMM\青阳人大\profile-bg.png')
    save_image('2','D:\WMM\皱燕民\景观工程（假山、驳岸）\微信图片_201903201145217.jpg')
    save_image('3','D:\WMM\皱燕民\景观工程（假山、驳岸）\微信图片_201903201145219.jpg')
    save_image('4','D:\WMM\皱燕民\景观工程（假山、驳岸）\微信图片_201903201147335.jpg')
    save_image('5','D:\WMM\皱燕民\景观工程（假山、驳岸）\微信图片_201903201147343.jpg')
    save_image('6','D:\WMM\皱燕民\景观工程（假山、驳岸）\微信图片_201903201147347.jpg')
    save_image('7','D:\WMM\皱燕民\景观工程（假山、驳岸）\微信图片_201903201147349.jpg')
    save_image('8','D:\WMM\皱燕民\景观工程（假山、驳岸）\微信图片_201903201142176.jpg')
    save_image('9','D:\WMM\皱燕民\景观工程（假山、驳岸）\微信图片_201903201142179.jpg')
    save_image('10','D:\WMM\皱燕民\景观工程（假山、驳岸）\微信图片_201903201145215.jpg')
    