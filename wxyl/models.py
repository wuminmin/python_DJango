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
    # save_image('1','D:\WMM\青阳人大\池州人大.jpg')
    # save_image('2','D:\WMM\皱燕民\景观工程（假山、驳岸）\微信图片_201903201145217.jpg')
    # save_image('3','D:\WMM\皱燕民\景观工程（假山、驳岸）\微信图片_201903201145219.jpg')
    # save_image('4','D:\WMM\皱燕民\景观工程（假山、驳岸）\微信图片_201903201147335.jpg')
    # save_image('5','D:\WMM\皱燕民\景观工程（假山、驳岸）\微信图片_201903201147343.jpg')
    # save_image('6','D:\WMM\皱燕民\景观工程（假山、驳岸）\微信图片_201903201147347.jpg')
    # save_image('7','D:\WMM\皱燕民\景观工程（假山、驳岸）\微信图片_201903201147349.jpg')
    # save_image('8','D:\WMM\皱燕民\景观工程（假山、驳岸）\微信图片_201903201142176.jpg')
    # save_image('9','D:\WMM\皱燕民\景观工程（假山、驳岸）\微信图片_201903201142179.jpg')
    # save_image('10','D:\WMM\皱燕民\景观工程（假山、驳岸）\微信图片_201903201145215.jpg')
    # save_image('11','D:/WMM/青阳人大/3da17aca-6a99-4d77-ba8b-8ad7aac424ab.jpg')
    # save_image('12','D:/WMM/青阳人大/50e3d8bc-16dd-4027-9a9e-696651e0ce13.jpg')
    # save_image('13','D:/WMM/青阳人大/bf0ed711-9e3b-44e8-a857-415d952f3a53.jpg')
    # save_image('14','D:/WMM/青阳人大/bf97e427-0381-4567-9a96-9203d70d9758.jpg')
    # save_image('15','D:/WMM/青阳人大/池州人大网络履职平台.jpg')
    # save_image('16','D:/WMM/青阳人大/修身福地灵秀青阳.png')
    # save_image('17','D:/WMM/青阳人大/微信图片_20191105095435.jpg')
    # save_image('18','D:/WMM/青阳人大/微信图片_20191105095449.jpg')
    # save_image('19','D:/WMM/青阳人大/微信图片_20191105095504.jpg')
    # save_image('20','D:/WMM/青阳人大/微信图片_20191105095507.jpg')
    # save_image('21','D:/WMM/青阳人大/微信图片_20191105095516.jpg')
    # save_image('22','D:/WMM/青阳人大/微信图片_20191105095522.jpg')
    # save_image('23','D:/WMM/青阳人大/微信图片_20191105095526.jpg')
    # save_image('24','D:/WMM/青阳人大/微信图片_20191105095529.jpg')
    save_image('25','C:/Users/WMM\Pictures/青阳人大/8b31fa16247dfa6260f7e202ca1c5d36.jpg')
    save_image('26','C:/Users/WMM\Pictures/青阳人大/673d352f8e6351e4aa2aa962409d93ca.jpg')
    