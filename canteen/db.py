
from . import models
import pymongo
import myConfig
from . import tool
import json
mongo_src = "mongodb://"+myConfig.canteen_username+":"+myConfig.canteen_password + \
    "@"+myConfig.host+":"+myConfig.port_str+"/?authSource="+myConfig.canteen_db
myclient = pymongo.MongoClient(mongo_src)
mydb = myclient[myConfig.canteen_db]

def 订餐人员表新增(d):
    r = tool.objectid_to_json( mydb.订餐人员表.find(d) )
    if r == []:
        mydb.订餐人员表.insert(d)
    

def 订餐主界面新增(d):
    if not '手机号' in d:
        return False
    手机号 = d['手机号']
    r = tool.objectid_to_json( mydb.订餐主界面表.find({'手机号':手机号}) )
    if r == []:
        mydb.订餐主界面表.insert(d)
        return True
    else:
        mydb.订餐主界面表.remove({'手机号':手机号})
        mydb.订餐主界面表.insert(d)
        return True

def 查询预消费和已消费(手机号,产品名称列表):
    index1 = 0
    index2 = 0
    for 产品名称 in 产品名称列表:
        list1 = list(models.订餐结果表.objects(__raw__={
            '产品.'+产品名称+'.签到':'没吃',
            '手机号':手机号
        }))
        for one1 in list1:
            预定数量 = one1.产品[产品名称]['预定数量']
            价格 = one1.产品[产品名称]['价格']
            index1 = index1 +预定数量*价格

        list2 = list(models.订餐结果表.objects(__raw__={
            '产品.'+产品名称+'.签到':'吃过',
            '手机号':手机号
        }))
        for one2 in list2:
            预定数量 = one2.产品[产品名称]['预定数量']
            价格 = one2.产品[产品名称]['价格']
            index2 = index2 + 预定数量*价格

    预消费 = index1
    已消费 = index2
    r = {
        '预消费':预消费,
        '已消费':已消费
    }
    print('查询预消费和已消费-------',r)
    return r

def 查询第一个订单结果(oid):
    from bson.objectid import ObjectId
    qset1 = models.订餐结果表.objects(__raw__={
        '_id':ObjectId(oid)
    }).first()
    return qset1

def 创建订餐提醒发货表(oid,name,d):
    d['oid'] = oid
    d['name'] = name
    qset1 = models.订餐提醒发货表.objects(__raw__={
        'd.oid':oid,'d.name':name
    }).first()
    if qset1 == None:
        models.订餐提醒发货表(d=d).save()
    else:
        qset1.update(d=d)

def 创建订餐主界面表():
    手机号_list =  mydb.订餐人员表.distinct('手机号')
    for one in 手机号_list:
        mydb.订餐人员表手机号中间表.drop()
        for one1 in tool.objectid_to_json(mydb.订餐人员表.find({'手机号':one})):
            one1.pop('_id')
            print('订餐人员表--',one1)
            mydb.订餐人员表手机号中间表.insert(one1)
        主菜单id_distinct_list = mydb.订餐人员表手机号中间表.distinct('主菜单id')
        listb = []
        for one2 in 主菜单id_distinct_list:
            listc = []
            for one3 in tool.objectid_to_json( mydb.订餐人员表.find({'手机号':one,'主菜单id':one2})):
                listc.append({
                    'page_name':one3['子菜单page_name'],
                    'page_desc':one3['子菜单page_desc'],
                    'url':one3['子菜单url'],
                })
            r_list_2 = tool.objectid_to_json( mydb.订餐人员表.find({'手机号':one,'主菜单id':one2}).limit(1))
            if r_list_2 == []:
                return False
            else:
                r_diect_2 = r_list_2[0]
                listb.append({
                    'name':r_diect_2['主菜单name'],
                    'id':r_diect_2['主菜单id'],
                    'pages':listc
                })
        r_list_1 = tool.objectid_to_json( mydb.订餐人员表.find({'手机号':one}).limit(1) )
        if r_list_1 == []:
            return False
        r_dict_1 = r_list_1[0]
        d = {
            '手机号':str(one),
            '描述':r_dict_1['描述'],
            '主页标题':r_dict_1['主页标题'],
            '主页描述':r_dict_1['主页描述'],
            '验证码标题':r_dict_1['验证码标题'],
            '验证码描述':r_dict_1['验证码描述'],
            '二级部门':r_dict_1['二级部门'],
            '三级部门':r_dict_1['三级部门'],
            '四级部门':r_dict_1['四级部门'],
            '姓名':r_dict_1['姓名'],
            '主界内容':listb
        }
        订餐主界面新增(d)
    return True

        
    