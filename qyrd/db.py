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
            }
        },
        {
            '$sort':{
                'my_date':-1
            }
        }
    ]
    r = mydb.qyrd_article_col.aggregate(pipeline)
    return list(r)