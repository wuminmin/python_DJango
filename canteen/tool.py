
# 异步函数
def deprecated_async(f):
    def wrapper(*args, **kwargs):
        from threading import Thread
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper
    
def 动态计算金额(数量,产品字典,折扣标签):
    if '价格' in 产品字典:
        if '折扣' in 产品字典:
            if 折扣标签 in 产品字典['折扣']:
                金额 = 数量*产品字典['价格']*产品字典['折扣'][折扣标签]
            else:
                金额 = 数量*产品字典['价格']
        else:
            金额 = 数量*产品字典['价格']
    else:
        金额 = 0
    print('动态计算金额-----------------',金额,数量,产品字典,折扣标签)
    return 金额

def 动态计算价格(产品字典,折扣标签):
    if '价格' in 产品字典:
        if '折扣' in 产品字典:
            if 折扣标签 in 产品字典['折扣']:
                价格 = 产品字典['价格']*产品字典['折扣'][折扣标签]
            else:
                价格 = 产品字典['价格']
        else:
            价格 = 产品字典['价格']
    else:
        价格 = 0
    print('动态计算价格-----------------',价格,产品字典,折扣标签)
    return 价格