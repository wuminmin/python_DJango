# python_django_server

微信小程序后台

Django 1.7.1及以上 用以下命令
# 1. 创建更改的文件
python manage.py makemigrations
# 2. 将生成的py文件应用到数据库
python manage.py migrate

#请确定你现在处于 manage.py 所在的目录下，然后运行这行命令来创建一个应用：
python manage.py startapp polls

python manage.py runserver 0.0.0.0:80

docker run -ti -p 8006:80 --name py_wx1 -v $(pwd):/workspace docker.io/python  bash

docker exec -it py_wx1 /bin/bash

docker logs -f -t --tail=10 9d766cea6a3f

pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple/  pandas






