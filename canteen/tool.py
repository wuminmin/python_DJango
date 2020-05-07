
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

def my_httpResponse(code,data,msg):
    from django.http import HttpResponse
    import json
    res_json = json.dumps({
        'code':code,
        'data':data,
        'msg':msg
    }).encode('utf-8').decode('unicode_escape')
    return HttpResponse(res_json)

def 微信认证(js_code,app_id):
    try:
        import requests
        import json
        import myConfig
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': app_id, 'secret': myConfig.appid_secret_dict[app_id], 'js_code': js_code,
                    'grant_type': 'authorization_code'}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        openid = r_json['openid']
        return {'openid':openid,'app_id':app_id}
    except:
        import traceback
        print(traceback.format_exc())
        return {'openid':'','app_id':''}

def get_str_time(i):
    import time
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + i*86400))