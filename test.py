import hashlib
import time
import requests
import json
# 创建获取时间戳的对象


class Time(object):
    def t_stamp(self):
        t = time.time()
        t_stamp = int(t)
        print('当前时间戳:', t_stamp)
        return t_stamp

# 创建获取token的对象


class Token(object):
    def __init__(self, api_secret, project_code, account):
        self._API_SECRET = api_secret
        self.project_code = project_code
        self.account = account

    def get_token(self):
        strs = self.project_code + self.account + \
            str(Time().t_stamp()) + self._API_SECRET
        hl = hashlib.md5()
        hl.update(strs.encode("utf8"))  # 指定编码格式，否则会报错
        token = hl.hexdigest()
        print('MD5加密前为 ：', strs)
        print('MD5加密后为 ：', token)
        return token


def 根据栏目查询文章列表(lan_mu):
    import pymongo
    import myConfig
    mongo_src = "mongodb://"+myConfig.username+":"+myConfig.password + \
        "@"+myConfig.host+":"+myConfig.port_str+"/?authSource="+myConfig.db
    myclient = pymongo.MongoClient(mongo_src)
    mydb = myclient[myConfig.db]
    pipeline = [
         {
            '$match': {
                'type': lan_mu
            }
        },
        {
            '$project': 
            {
                'article':False,
                # 'type': 1, 'tittle': 1, 'my_time': 1,
                # 'my_date': 1, 'my_month': 1, 'author': 1, 'other': 1,'_id':1
            }
        },
    ]
    r = mydb.qyrd_article_col.aggregate(pipeline)
    print(list(r))


if __name__ == '__main__':
    # tokenprogramer = Token('api_secret具体值', 'project_code具体值', 'account具体值')  # 对象实例化
    # tokenprogramer.get_token()   #调用token对象
    根据栏目查询文章列表('人大要闻')
