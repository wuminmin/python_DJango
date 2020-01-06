import _thread
import json
import time
import pandas
import datetime

def make_sign():
    import myConfig
    scrit_key = myConfig.chinaums_scrit_key
    msgId = myConfig.chinaums_msgId
    msgSrc = myConfig.chinaums_msgSrc
    msgType = myConfig.chinaums_msgType
    requestTimestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    merOrderId = myConfig.chinaums_msgId+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    mid = myConfig.chinaums_mid
    tid = myConfig.chinaums_tid
    totalAmount = myConfig.chinaums_totalAmount
    instMid = myConfig.chinaums_instMid
    tradeType = myConfig.chinaums_tradeType
    subAppId = myConfig.chinaums_subAppId
    subOpenId = myConfig.chinaums_subOpenId
    goods = [
        {'body':'微信二维码测试',
        'price': '1',
        'goodsName': '微信二维码测试',
        'goodsId': '1',
        'quantity': '1',
        'goodsCategory': 'TEST'}
    ]

    wmm_json = {'msgId': msgId, 'msgSrc': msgSrc, 'msgType': msgType, 'requestTimestamp': requestTimestamp,
                'merOrderId': merOrderId, 'mid': mid, 'tid': tid, 'totalAmount': totalAmount,
                 'subOpenId': subOpenId,'goods':goods,
                'tradeType': tradeType, 'subAppId': subAppId, 'subOpenId': subOpenId, 'instMid': instMid}
    wmm_list = list(wmm_json.keys())
    list.sort(wmm_list)
    wmm_str = ''
    for one in wmm_list:
        if wmm_json[one] == '' or wmm_json[one] == None:
            pass
        else:
            if one == 'goods':
                wmm_str = wmm_str+one+'='+json.dumps(wmm_json[one]).encode('utf-8').decode('unicode_escape').replace(' ','')+'&'
            else:
                wmm_str = wmm_str+one+'='+wmm_json[one]+'&'
    wmm_str = wmm_str.rstrip('&')
    wmm_str = wmm_str + scrit_key
    print(wmm_str)
    import hashlib
    wmm_sign = hashlib.md5(wmm_str.encode('utf-8')).hexdigest()
    print(wmm_sign)
    wmm_json['sign'] = wmm_sign
    # wmm_json_str = json.dumps(wmm_json)
    print(wmm_json)
    import requests
    r = requests.post(
        'https://qr.chinaums.com/netpay-route-server/api/', json=wmm_json)
    print(r.status_code)
    json_res = r.json()
    print(json.dumps(json_res))


if __name__ == '__main__':
    # 两高采集表每天发邮件()
    make_sign()
