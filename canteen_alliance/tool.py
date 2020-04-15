# -*- coding: utf-8 -*-
import json
import sys
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.http import method_type as MT
from aliyunsdkcore.http import format_type as FT
from myConfig import AccessKeyID, AccessKeySecret, sign_name, template_code

"""
短信业务调用接口示例，版本号：v20170525

Created on 2017-06-12

"""
try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except NameError:
    pass
except Exception as err:
    raise err

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

acs_client = AcsClient(AccessKeyID, AccessKeySecret, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)

def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name)
	
    # 数据提交方式
	# smsRequest.set_method(MT.POST)
	
	# 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)
	
    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理
    return smsResponse


# 创建获取时间戳的对象
class Time(object):
    import hashlib
    import requests
    import json
    def t_stamp(self):
        import time
        t = time.time()
        t_stamp = int(t)
        return t_stamp
    def now_time(self):
        import time
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

# 创建获取token的对象
class Token(object):
    import time
    import requests
    import json
    def __init__(self, api_secret, project_code, account):
        self._API_SECRET = api_secret
        self.project_code = project_code
        self.account = account
    def get_token(self):
        import hashlib
        strs = self.project_code + self.account + str(Time().t_stamp()) + self._API_SECRET
        hl = hashlib.md5()
        hl.update(strs.encode("utf8"))  # 指定编码格式，否则会报错
        token = hl.hexdigest()
        return token

def wmm_get_now_time():
    import time
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

def wmm_to_json(qset):
    s98 = qset.to_json().encode('utf-8').decode('unicode_escape')
    return json.loads(s98)

def wmm_create_main_id():
    return str( uuid.uuid1() )

def wmm_create_token():
    return str( uuid.uuid1() )


if __name__ == '__main__':
    tokenprogramer = Token('api_secret具体值', 'project_code具体值', 'account具体值')  # 对象实例化
    tokenprogramer.get_token()   #调用token对象

    __business_id = uuid.uuid1()
    params = "{\"code\":\"123456\"}"
    print( json.loads( send_sms(__business_id, "13355661100", sign_name, template_code , params)))

   
    
    

