# python_django_server

微信小程序后台

Django 1.7.1及以上 用以下命令
# 1. 创建更改的文件
python manage.py makemigrations
# 2. 将生成的py文件应用到数据库
python manage.py migrate

#请确定你现在处于 manage.py 所在的目录下，然后运行这行命令来创建一个应用：
python manage.py startapp polls

python manage.py runserver 0.0.0.0:8005


#启动Django容器
docker run -p 18005:8005 -v /mnt/user/docker/django:/app -d dj:v2

#登录容器内部
docker exec -it 9d766cea6a3f /bin/bash
#退出容器内部
exit

#启动MongoDB容器
docker run --name mongo1 -v /mnt/user/docker/db:/data/db -p 37117:27017 -d mongo mongod --dbpath /data/db




