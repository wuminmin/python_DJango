from mongoengine import *

# 数据库连接
import myConfig

connect(db=myConfig.db, host=myConfig.host, port=myConfig.port, username=myConfig.username, password=myConfig.password)

class 分析扇区同方向表(Document):
    营业部 = StringField()
    扇区组 = ListField()

class 分析扇区同方向结果表(Document):
    营业部 = StringField()
    扇区中文名1 = StringField()
    扇区中文名2 = StringField()
    天线方位角1 = StringField()
    天线方位角2 = StringField()
