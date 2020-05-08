
from . import models

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

# def 更新订餐结果表(oid)