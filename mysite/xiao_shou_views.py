import json
import traceback
import uuid

import requests
import time
from django.http import HttpResponse, FileResponse

import myConfig
from myConfig import xiao_shou_appid, xiao_shou_secret, xiao_shou_grant_type, sign_name, template_code, 销售微信小程序审核开关
from mysite.demo_sms_send import send_sms
from mysite.xiao_shou_mongo import 销售用户表, 销售登录状态表, 销售验证码表, 销售主界面表, 销售楼宇表, 可出售, 已登记, 已出售, 门牌号分隔符, 销售房屋信息表


def 销售推送微信验证(request):
    return None


def 销售登录检查(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': xiao_shou_appid, 'secret': xiao_shou_secret, 'js_code': js_code,
                   'grant_type': xiao_shou_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        查询结果 = 销售用户表.objects(openid=r_json['openid']).first()
        if 查询结果 == None:
            自定义登录状态 = "{\"描述\":\"用户不存在\",\"会话\":\"\"}"
            return HttpResponse(自定义登录状态)
        else:
            r = 销售登录状态表(session_key=r_json['session_key'], openid=r_json['openid']).save()
            自定义登录状态 = "{\"描述\":\"验证通过\",\"会话\":\"" + str(r.id) + "\"}"
            return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')


def 销售发送验证码(request):
    try:
        手机号 = str(request.GET['phone'])
        if 手机号 == '':
            return HttpResponse("手机号为空")
        else:
            import random
            j = 6
            验证码 = ''.join(str(i) for i in random.sample(range(0, 9), j))  # sample(seq, n) 从序列seq中选择n个随机且独立的元素；
            __business_id = uuid.uuid1()
            params = "{\"code\":\"" + 验证码 + "\"}"
            r = send_sms(__business_id, 手机号, sign_name, template_code, params)
            r2 = json.loads(r)
            if r2['Code'] == 'OK':
                r = 销售验证码表(验证码=验证码, 手机号=手机号).save()
            return HttpResponse(r2['Code'])
    except:
        return HttpResponse('500')


def 销售校验验证码(request):
    手机号 = str(request.GET['phone'])
    验证码 = str(request.GET['sms_code'])
    js_code = request.GET['code']
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    payload = {'appid': xiao_shou_appid, 'secret': xiao_shou_secret, 'js_code': js_code,
               'grant_type': xiao_shou_grant_type}
    r = requests.get(url=url, params=payload)
    r_json = json.loads(r.text)
    openid = r_json['openid']
    抽奖验证码表_objects = 销售验证码表.objects(手机号=手机号)
    for 抽奖验证码表_obj in 抽奖验证码表_objects:
        if 抽奖验证码表_obj.验证码 == 验证码:
            抽奖用户表_first = 销售用户表.objects(手机号=手机号).first()
            if 抽奖用户表_first == None:
                销售用户表(手机号=手机号, openid=openid).save()
            else:
                抽奖用户表_first.update(openid=openid)
            return HttpResponse('绑定成功')
    return HttpResponse('绑定失败')


def 销售下载主界面数据(request):
    try:
        js_code = request.GET['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': xiao_shou_appid, 'secret': xiao_shou_secret, 'js_code': js_code,
                   'grant_type': xiao_shou_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 销售用户表.objects(openid=r_json['openid']).first()
        手机号 = 用户.手机号
        print(手机号)
        主界面 = 销售主界面表.objects(手机号=用户.手机号).first()
        if 主界面 == None:
            if 销售微信小程序审核开关:
                创建时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                描述 = '下载成功'
                主页标题 = '销售助手123'
                主页描述 = '销售助手123'
                验证码标题 = ''
                验证码描述 = ''
                二级部门 = '测试'
                三级部门 = '测试'
                四级部门 = '测试'
                姓名 = '测试'
                主界内容 = [
                    {
                        'id': 'lu_ru',
                        'name': '录入销售数据',
                        'open': False,
                        'pages': [
                            {
                                'url': 'lu_ru',
                                'page_name': '碧桂园',
                                'page_desc': '录入数据'
                            },
                            {
                                'url': 'lu_ru',
                                'page_name': '万科',
                                'page_desc': '录入数据'
                            },
                            {
                                'url': 'lu_ru',
                                'page_name': '绿地',
                                'page_desc': '录入数据'
                            }
                        ]
                    },
                    {
                        'id': 'xiao_shou_guan_li',
                        'name': '销售管理',
                        'open': False,
                        'pages': [
                            {
                                'url': 'xiao_shou_guan_li',
                                'page_name': '碧桂园',
                                'page_desc': '销售进度'
                            },
                            {
                                'url': 'xiao_shou_guan_li',
                                'page_name': '万科',
                                'page_desc': '销售进度'
                            },
                            {
                                'url': 'xiao_shou_guan_li',
                                'page_name': '绿地',
                                'page_desc': '销售进度'
                            }
                        ]
                    }
                ]
                主界面表_save = 销售主界面表(手机号=str(用户.手机号), 描述=str(描述), 创建时间=str(创建时间),
                       主页标题=str(主页标题),主页描述=str(主页描述), 验证码标题=str(验证码标题),
                       验证码描述=str(验证码描述), 二级部门=二级部门, 三级部门=三级部门, 四级部门=四级部门, 姓名=姓名,
                       主界内容=主界内容).save()
                自定义登录状态 = 主界面表_save.to_json().encode('utf-8').decode('unicode_escape')
                return HttpResponse(自定义登录状态)
            自定义登录状态 = "{\"描述\":\"没有数据\",\"会话\":\"" + r_json['session_key'] + "\"}"
            return HttpResponse(自定义登录状态)
        else:
            自定义登录状态 = 主界面.to_json().encode('utf-8').decode('unicode_escape')
            return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')

def 下载录入数据(request):
    try:
        js_code = request.GET['code']
        name = request.GET['name']
        page_name = request.GET['page_name']
        page_desc = request.GET['page_desc']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': xiao_shou_appid, 'secret': xiao_shou_secret, 'js_code': js_code,
                   'grant_type': xiao_shou_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 销售用户表.objects(openid=r_json['openid']).first()
        主界面表first = 销售主界面表.objects(手机号=用户.手机号).first()
        if 主界面表first == None:
            手机号 = ''
        else:
            手机号 = 主界面表first.手机号
        销售楼宇表objs = 销售楼宇表.objects(手机号列表__contains= 手机号 ,小区名称=page_name )
        楼宇名称list = []
        楼宇编号list = []
        if list(销售楼宇表objs) == []:
            销售楼宇表(
                手机号列表=[手机号],
                小区名称 = page_name,
                小区编号 = page_name,
                楼宇名称 = '1号楼',
                楼宇编号 = '1',
                楼宇详情列表 = [
                        {
                            'dan_yuan_id': '1',
                            'dan_yuan_name': '一单元',
                            'dan_yuan': [
                                {
                                    'lou_ceng_id': '6',
                                    'ceng': [
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'1_1_6_601',
                                            'men_pai_hao': '601',
                                            'zhuang_tai': 可出售,
                                        },
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'1_1_6_602',
                                            'men_pai_hao': '602',
                                            'zhuang_tai': 可出售,
                                        }
                                    ]
                                },
                                {
                                    'lou_ceng_id': '5',
                                    'ceng': [
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'1_1_5_501',
                                            'men_pai_hao': '501',
                                            'zhuang_tai': 可出售,
                                        },
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'1_1_5_502',
                                            'men_pai_hao': '502',
                                            'zhuang_tai': 可出售,
                                        }
                                    ]
                                },
                                {
                                    'lou_ceng_id': '4',
                                    'ceng': [
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'1_1_4_401',
                                            'men_pai_hao': '401',
                                            'zhuang_tai': 可出售,
                                        },
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'1_1_4_402',
                                            'men_pai_hao': '402',
                                            'zhuang_tai': 可出售,
                                        }
                                    ]
                                },
                                {
                                    'lou_ceng_id': '3',
                                    'ceng': [
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'1_1_3_301',
                                            'men_pai_hao': '301',
                                            'zhuang_tai': 可出售,
                                        },
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'1_1_3_302',
                                            'men_pai_hao': '302',
                                            'zhuang_tai': 可出售,
                                        }
                                    ]
                                },
                                {
                                    'lou_ceng_id': '2',
                                    'ceng': [
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'1_1_2_201',
                                            'men_pai_hao': '201',
                                            'zhuang_tai': 可出售,
                                        },
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'1_1_2_202',
                                            'men_pai_hao': '202',
                                            'zhuang_tai': 可出售,
                                        }
                                    ]
                                },
                                {
                                    'lou_ceng_id': '1',
                                    'ceng': [
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'1_1_1_101',
                                            'men_pai_hao': '101',
                                            'zhuang_tai': 可出售,
                                        },
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'1_1_1_102',
                                            'men_pai_hao': '102',
                                            'zhuang_tai': 可出售,
                                        }
                                    ]
                                },
                            ],
                        },
                        {
                            'dan_yuan_id': '2',
                            'dan_yuan_name': '二单元',
                            'dan_yuan': [
                                {
                                    'lou_ceng_id': '3',
                                    'ceng': [
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'1_2_3_301',
                                            'men_pai_hao': '301',
                                            'zhuang_tai': 可出售,
                                        },
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'1_2_3_302',
                                            'men_pai_hao': '302',
                                            'zhuang_tai': 可出售,
                                        }
                                    ]
                                },
                                {
                                    'lou_ceng_id': '2',
                                    'ceng': [
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'1_2_2_201',
                                            'men_pai_hao': '201',
                                            'zhuang_tai': 可出售,
                                        },
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'1_2_2_202',
                                            'men_pai_hao': '202',
                                            'zhuang_tai': 可出售,
                                        }
                                    ]
                                },
                                {
                                    'lou_ceng_id': '1',
                                    'ceng': [
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'1_2_1_101',
                                            'men_pai_hao': '101',
                                            'zhuang_tai': 可出售,
                                        },
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'1_2_1_102',
                                            'men_pai_hao': '102',
                                            'zhuang_tai': 可出售,
                                        }
                                    ]
                                },
                            ],
                        }
                    ]
            ).save()
            销售楼宇表(
                手机号列表=[手机号],
                小区名称 = page_name,
                小区编号 = page_name,
                楼宇名称 = '2号楼',
                楼宇编号 = '2',
                楼宇详情列表 = [
                        {
                            'dan_yuan_id': '1',
                            'dan_yuan_name': '一单元',
                            'dan_yuan': [
                                {
                                    'lou_ceng_id': '6',
                                    'ceng': [
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'2_1_6_601',
                                            'men_pai_hao': '601',
                                            'zhuang_tai': 可出售,
                                        },
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'2_1_6_602',
                                            'men_pai_hao': '602',
                                            'zhuang_tai': 可出售,
                                        }
                                    ]
                                },
                                {
                                    'lou_ceng_id': '5',
                                    'ceng': [
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'2_1_5_501',
                                            'men_pai_hao': '501',
                                            'zhuang_tai': 可出售,
                                        },
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'2_1_5_502',
                                            'men_pai_hao': '502',
                                            'zhuang_tai': 可出售,
                                        }
                                    ]
                                },
                                {
                                    'lou_ceng_id': '4',
                                    'ceng': [
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'2_1_4_401',
                                            'men_pai_hao': '401',
                                            'zhuang_tai': 可出售,
                                        },
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'2_1_4_402',
                                            'men_pai_hao': '402',
                                            'zhuang_tai': 可出售,
                                        }
                                    ]
                                },
                                {
                                    'lou_ceng_id': '3',
                                    'ceng': [
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'2_1_3_301',
                                            'men_pai_hao': '301',
                                            'zhuang_tai': 可出售,
                                        },
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'2_1_3_302',
                                            'men_pai_hao': '302',
                                            'zhuang_tai': 可出售,
                                        }
                                    ]
                                },
                                {
                                    'lou_ceng_id': '2',
                                    'ceng': [
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'2_1_2_201',
                                            'men_pai_hao': '201',
                                            'zhuang_tai': 可出售,
                                        },
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'2_1_2_202',
                                            'men_pai_hao': '202',
                                            'zhuang_tai': 可出售,
                                        }
                                    ]
                                },
                                {
                                    'lou_ceng_id': '1',
                                    'ceng': [
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'2_1_1_101',
                                            'men_pai_hao': '101',
                                            'zhuang_tai': 可出售,
                                        },
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'2_1_1_102',
                                            'men_pai_hao': '102',
                                            'zhuang_tai': 可出售,
                                        }
                                    ]
                                },
                            ],
                        },
                        {
                            'dan_yuan_id': '2',
                            'dan_yuan_name': '二单元',
                            'dan_yuan': [
                                {
                                    'lou_ceng_id': '3',
                                    'ceng': [
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'2_2_3_301',
                                            'men_pai_hao': '301',
                                            'zhuang_tai': 可出售,
                                        },
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'2_2_3_302',
                                            'men_pai_hao': '302',
                                            'zhuang_tai': 可出售,
                                        }
                                    ]
                                },
                                {
                                    'lou_ceng_id': '2',
                                    'ceng': [
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'2_2_2_201',
                                            'men_pai_hao': '201',
                                            'zhuang_tai': 可出售,
                                        },
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'2_2_2_202',
                                            'men_pai_hao': '202',
                                            'zhuang_tai': 可出售,
                                        }
                                    ]
                                },
                                {
                                    'lou_ceng_id': '1',
                                    'ceng': [
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'2_2_1_101',
                                            'men_pai_hao': '101',
                                            'zhuang_tai': 可出售,
                                        },
                                        {
                                            'men_pai_id': page_name+门牌号分隔符+'2_2_1_102',
                                            'men_pai_hao': '102',
                                            'zhuang_tai': 可出售,
                                        }
                                    ]
                                },
                            ],
                        }
                    ]
            ).save()
            销售楼宇表(
                手机号列表=[手机号],
                小区名称=page_name,
                小区编号=page_name,
                楼宇名称='3号楼',
                楼宇编号='3',
                楼宇详情列表=[
                    {
                        'dan_yuan_id': '1',
                        'dan_yuan_name': '一单元',
                        'dan_yuan': [
                            {
                                'lou_ceng_id': '6',
                                'ceng': [
                                    {
                                        'men_pai_id': page_name + 门牌号分隔符 + '3_1_6_601',
                                        'men_pai_hao': '601',
                                        'zhuang_tai': 可出售,
                                    },
                                    {
                                        'men_pai_id': page_name + 门牌号分隔符 + '3_1_6_602',
                                        'men_pai_hao': '602',
                                        'zhuang_tai': 可出售,
                                    }
                                ]
                            },
                            {
                                'lou_ceng_id': '5',
                                'ceng': [
                                    {
                                        'men_pai_id': page_name + 门牌号分隔符 + '3_1_5_501',
                                        'men_pai_hao': '501',
                                        'zhuang_tai': 可出售,
                                    },
                                    {
                                        'men_pai_id': page_name + 门牌号分隔符 + '3_1_5_502',
                                        'men_pai_hao': '502',
                                        'zhuang_tai': 可出售,
                                    }
                                ]
                            },
                            {
                                'lou_ceng_id': '4',
                                'ceng': [
                                    {
                                        'men_pai_id': page_name + 门牌号分隔符 + '3_1_4_401',
                                        'men_pai_hao': '401',
                                        'zhuang_tai': 可出售,
                                    },
                                    {
                                        'men_pai_id': page_name + 门牌号分隔符 + '3_1_4_402',
                                        'men_pai_hao': '402',
                                        'zhuang_tai': 可出售,
                                    }
                                ]
                            },
                            {
                                'lou_ceng_id': '3',
                                'ceng': [
                                    {
                                        'men_pai_id': page_name + 门牌号分隔符 + '3_1_3_301',
                                        'men_pai_hao': '301',
                                        'zhuang_tai': 可出售,
                                    },
                                    {
                                        'men_pai_id': page_name + 门牌号分隔符 + '3_1_3_302',
                                        'men_pai_hao': '302',
                                        'zhuang_tai': 可出售,
                                    }
                                ]
                            },
                            {
                                'lou_ceng_id': '2',
                                'ceng': [
                                    {
                                        'men_pai_id': page_name + 门牌号分隔符 + '3_1_2_201',
                                        'men_pai_hao': '201',
                                        'zhuang_tai': 可出售,
                                    },
                                    {
                                        'men_pai_id': page_name + 门牌号分隔符 + '3_1_2_202',
                                        'men_pai_hao': '202',
                                        'zhuang_tai': 可出售,
                                    }
                                ]
                            },
                            {
                                'lou_ceng_id': '1',
                                'ceng': [
                                    {
                                        'men_pai_id': page_name + 门牌号分隔符 + '3_1_1_101',
                                        'men_pai_hao': '101',
                                        'zhuang_tai': 可出售,
                                    },
                                    {
                                        'men_pai_id': page_name + 门牌号分隔符 + '3_1_1_102',
                                        'men_pai_hao': '102',
                                        'zhuang_tai': 可出售,
                                    }
                                ]
                            },
                        ],
                    },
                    {
                        'dan_yuan_id': '2',
                        'dan_yuan_name': '二单元',
                        'dan_yuan': [
                            {
                                'lou_ceng_id': '3',
                                'ceng': [
                                    {
                                        'men_pai_id': page_name + 门牌号分隔符 + '3_2_3_301',
                                        'men_pai_hao': '301',
                                        'zhuang_tai': 可出售,
                                    },
                                    {
                                        'men_pai_id': page_name + 门牌号分隔符 + '3_2_3_302',
                                        'men_pai_hao': '302',
                                        'zhuang_tai': 可出售,
                                    }
                                ]
                            },
                            {
                                'lou_ceng_id': '2',
                                'ceng': [
                                    {
                                        'men_pai_id': page_name + 门牌号分隔符 + '3_2_2_201',
                                        'men_pai_hao': '201',
                                        'zhuang_tai': 可出售,
                                    },
                                    {
                                        'men_pai_id': page_name + 门牌号分隔符 + '3_2_2_202',
                                        'men_pai_hao': '202',
                                        'zhuang_tai': 可出售,
                                    }
                                ]
                            },
                            {
                                'lou_ceng_id': '1',
                                'ceng': [
                                    {
                                        'men_pai_id': page_name + 门牌号分隔符 + '3_2_1_101',
                                        'men_pai_hao': '101',
                                        'zhuang_tai': 可出售,
                                    },
                                    {
                                        'men_pai_id': page_name + 门牌号分隔符 + '3_2_1_102',
                                        'men_pai_hao': '102',
                                        'zhuang_tai': 可出售,
                                    }
                                ]
                            },
                        ],
                    }
                ]
            ).save()
        for 销售楼宇表obj in 销售楼宇表objs:
            print(销售楼宇表obj.楼宇名称)
            if 销售楼宇表obj.楼宇名称 in 楼宇名称list:
                pass
            else:
                楼宇名称list.append(销售楼宇表obj.楼宇名称)
            if 销售楼宇表obj.楼宇编号 in 楼宇编号list:
                pass
            else:
                楼宇编号list.append(销售楼宇表obj.楼宇编号)
        if 楼宇名称list == []:
            lou_yu_id = ''
            lou_yu_list = []
        else:
            lou_yu_id = 楼宇编号list[0]
            lou_yu_list = 销售楼宇表.objects(
                手机号列表__contains= 手机号,
                小区名称=page_name
            ).first().楼宇详情列表
        自定义登录状态 = {
            '描述': '成功',
            'name': name,
            'page_name':page_name,
            'page_desc':page_desc,
            'xiao_qu_id':page_name,
            'array':楼宇名称list,
            'lou_yu_list': lou_yu_list,
            'index':0,
            'lou_yu_id':lou_yu_id,
            'lou_yu_id_list':楼宇编号list,
        }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')


def 修改楼宇状态(request):
    try:
        js_code = request.GET['code']
        bindMenPaiHao_id = request.GET['bindMenPaiHao_id']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': xiao_shou_appid, 'secret': xiao_shou_secret, 'js_code': js_code,
                   'grant_type': xiao_shou_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 销售用户表.objects(openid=r_json['openid']).first()
        主界面表first = 销售主界面表.objects(手机号=用户.手机号).first()
        if 主界面表first == None:
            手机号 = ''
        else:
            手机号 = 主界面表first.手机号
        bindMenPaiHao_id_list = bindMenPaiHao_id.split(门牌号分隔符)
        print(bindMenPaiHao_id_list)
        小区编号 = bindMenPaiHao_id_list[0]
        楼宇编号 = bindMenPaiHao_id_list[1]
        销售楼宇表objs = 销售楼宇表.objects(
            手机号列表__contains=手机号,
            小区编号=小区编号,
            楼宇编号=楼宇编号
        )
        for 销售楼宇表obj in 销售楼宇表objs:
            楼宇详情列表list = []
            for 楼宇详情列表one in 销售楼宇表obj.楼宇详情列表:
                for dan_yuan_one in 楼宇详情列表one['dan_yuan']:
                    for ceng_one in dan_yuan_one['ceng']:
                        men_pai_id = ceng_one['men_pai_id']
                        zhuang_tai = ceng_one['zhuang_tai']
                        if men_pai_id == bindMenPaiHao_id:
                            if zhuang_tai == 可出售:
                                ceng_one['zhuang_tai'] = 已登记
                            if zhuang_tai == 已登记:
                                ceng_one['zhuang_tai'] = 已出售
                楼宇详情列表list.append(楼宇详情列表one)
            销售楼宇表obj.update(楼宇详情列表=楼宇详情列表list)

        销售楼宇表first = 销售楼宇表.objects(
            手机号列表__contains=手机号,
            小区编号=小区编号,
            楼宇编号=楼宇编号
        ).first()
        自定义登录状态 = {
            '描述': '成功',
            'lou_yu_list':销售楼宇表first.楼宇详情列表
        }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')


def 下载楼宇信息(request):
    try:
        js_code = request.GET['code']
        page_name = request.GET['page_name']
        lou_yu_id = request.GET['lou_yu_id']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': xiao_shou_appid, 'secret': xiao_shou_secret, 'js_code': js_code,
                   'grant_type': xiao_shou_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 销售用户表.objects(openid=r_json['openid']).first()
        主界面表first = 销售主界面表.objects(手机号=用户.手机号).first()
        if 主界面表first == None:
            手机号 = ''
        else:
            手机号 = 主界面表first.手机号
        销售楼宇表first = 销售楼宇表.objects(
            手机号列表__contains=手机号,
            小区名称=page_name,
            楼宇编号=lou_yu_id
        ).first()
        if 销售楼宇表first == None:
            lou_yu_list = []
        else:
            lou_yu_list =  销售楼宇表first.楼宇详情列表
        自定义登录状态 = {
            '描述': '成功',
            'lou_yu_list': lou_yu_list
        }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')


def 下载小区统计(request):
    try:
        js_code = request.GET['code']
        name = request.GET['name']
        page_name = request.GET['page_name']
        page_desc = request.GET['page_desc']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': xiao_shou_appid, 'secret': xiao_shou_secret, 'js_code': js_code,
                   'grant_type': xiao_shou_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 销售用户表.objects(openid=r_json['openid']).first()
        主界面表first = 销售主界面表.objects(手机号=用户.手机号).first()
        if 主界面表first == None:
            手机号 = ''
        else:
            手机号 = 主界面表first.手机号
        销售楼宇表objs = 销售楼宇表.objects(
            手机号列表__contains=手机号,
            小区名称=page_name,
        )
        xiao_qu_all_list = []
        xiao_qu_red_list = []
        xiao_qu_blue_list = []
        xiao_qu_green_list = []
        xiao_qu = []
        for 销售楼宇表obj in 销售楼宇表objs:
            all_list = []
            red_list = []
            blue_list = []
            green_list = []
            for 楼宇详情列表one in 销售楼宇表obj.楼宇详情列表:
                for dan_yuan_one in 楼宇详情列表one['dan_yuan']:
                    for ceng_one in dan_yuan_one['ceng']:
                        men_pai_id = ceng_one['men_pai_id']
                        zhuang_tai = ceng_one['zhuang_tai']
                        xiao_qu_all_list.append(men_pai_id)
                        all_list.append(men_pai_id)
                        if zhuang_tai == 可出售:
                            xiao_qu_red_list.append(zhuang_tai)
                            red_list.append(zhuang_tai)
                        elif zhuang_tai == 已登记:
                            xiao_qu_blue_list.append(zhuang_tai)
                            blue_list.append(zhuang_tai)
                        elif zhuang_tai == 已出售:
                            xiao_qu_green_list.append(zhuang_tai)
                            green_list.append(zhuang_tai)
                        else:
                            pass
            lou_yu_id = 销售楼宇表obj.楼宇编号
            lou_yu_name = 销售楼宇表obj.楼宇名称

            all = len(all_list)
            red = len(red_list)
            blue = len(blue_list)
            green = len(green_list)
            xiao_qu_dict = {
                'lou_yu_id':lou_yu_id,
                'lou_yu_name':lou_yu_name,
                'all': all,
                'red': red,
                'blue': blue,
                'green': green,
            }
            xiao_qu.append(xiao_qu_dict)

        xiao_qu_all = len(xiao_qu_all_list)
        xiao_qu_red = len(xiao_qu_red_list)
        xiao_qu_blue = len(xiao_qu_blue_list)
        xiao_qu_green = len(xiao_qu_green_list)
        自定义登录状态 = {
            '描述': '成功',
            'name': name,
            'page_name': page_name,
            'page_desc': page_desc,
            'xiao_qu_all':xiao_qu_all,
            'xiao_qu_red': xiao_qu_red,
            'xiao_qu_blue': xiao_qu_blue,
            'xiao_qu_green': xiao_qu_green,
            'xiao_qu': xiao_qu,
        }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')


def 录入页面初始化(request):
    try:
        js_code = request.GET['code']
        bindMenPaiHao_id = request.GET['bindMenPaiHao_id']
        # page_name = request.GET['page_name']
        # page_desc = request.GET['page_desc']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': xiao_shou_appid, 'secret': xiao_shou_secret, 'js_code': js_code,
                   'grant_type': xiao_shou_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 销售用户表.objects(openid=r_json['openid']).first()
        主界面表first = 销售主界面表.objects(手机号=用户.手机号).first()
        if 主界面表first == None:
            手机号 = ''
        else:
            手机号 = 主界面表first.手机号
        bindMenPaiHao_id_list = bindMenPaiHao_id.split(门牌号分隔符)
        print(bindMenPaiHao_id_list)
        小区名称 = bindMenPaiHao_id_list[0]
        楼宇名称 = bindMenPaiHao_id_list[1]
        门牌编号 = bindMenPaiHao_id
        countries = [小区名称]
        countries2 = [楼宇名称]
        countries3 = [门牌编号]
        销售房屋信息表first =销售房屋信息表.objects(门牌编号=bindMenPaiHao_id).first()
        if 销售房屋信息表first == None:
            chang_suo_lou_yu_zong_dong_shu = ''
            lou_yu_ceng_shu = ''
            shi_fou_you_di_xia_ting_cha_chang = False
            shi_fou_you_yi_wang_shi_feng = False
            shi_fou_you_yi_kan_cha = False
        else:
            chang_suo_lou_yu_zong_dong_shu = 销售房屋信息表first.房屋信息['受买人姓名']
            lou_yu_ceng_shu = 销售房屋信息表first.房屋信息['受买人身份证号码']
            shi_fou_you_di_xia_ting_cha_chang = 销售房屋信息表first.房屋信息['是否缴纳定金']
            shi_fou_you_yi_wang_shi_feng = 销售房屋信息表first.房屋信息['是否签到购房合同']
            shi_fou_you_yi_kan_cha = 销售房屋信息表first.房屋信息['是否已付清尾款']
        自定义登录状态 = {
            '描述': '成功',
            'countries': countries,
            'countries2': countries2,
            'countries3': countries3,
            'chang_suo_lou_yu_zong_dong_shu': chang_suo_lou_yu_zong_dong_shu,
            'lou_yu_ceng_shu': lou_yu_ceng_shu,
            'shi_fou_you_di_xia_ting_cha_chang': shi_fou_you_di_xia_ting_cha_chang,
            'shi_fou_you_yi_wang_shi_feng': shi_fou_you_yi_wang_shi_feng,
            'shi_fou_you_yi_kan_cha': shi_fou_you_yi_kan_cha,
        }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')


def 上传录入数据(request):
    try:
        js_code = request.GET['code']
        print(type(request.GET['filePath']))
        filePath = request.GET['filePath']
        print(filePath)
        if filePath == '' or filePath == None:
            自定义登录状态 = {
                '描述': '没有选择图片'
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        bindMenPaiHao_id = request.GET['bindMenPaiHao_id']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': xiao_shou_appid, 'secret': xiao_shou_secret, 'js_code': js_code,
                   'grant_type': xiao_shou_grant_type}
        r = requests.get(url=url, params=payload)
        r_json = json.loads(r.text)
        用户 = 销售用户表.objects(openid=r_json['openid']).first()
        主界面表first = 销售主界面表.objects(手机号=用户.手机号).first()
        if 主界面表first == None:
            手机号 = ''
        else:
            手机号 = 主界面表first.手机号
        bindMenPaiHao_id_list = bindMenPaiHao_id.split(门牌号分隔符)
        print(bindMenPaiHao_id_list)
        小区编号 = bindMenPaiHao_id_list[0]
        楼宇编号 = bindMenPaiHao_id_list[1]

        创建时间 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        chang_suo_lou_yu_zong_dong_shu = request.GET['chang_suo_lou_yu_zong_dong_shu']
        lou_yu_ceng_shu = request.GET['lou_yu_ceng_shu']
        shi_fou_you_di_xia_ting_cha_chang = request.GET['shi_fou_you_di_xia_ting_cha_chang']
        shi_fou_you_yi_wang_shi_feng = request.GET['shi_fou_you_yi_wang_shi_feng']
        shi_fou_you_yi_kan_cha = request.GET['shi_fou_you_yi_kan_cha']
        if shi_fou_you_di_xia_ting_cha_chang == 'true':
            shi_fou_you_di_xia_ting_cha_chang = True
        else:
            shi_fou_you_di_xia_ting_cha_chang = False
        if shi_fou_you_yi_wang_shi_feng == 'true':
            shi_fou_you_yi_wang_shi_feng = True
        else:
            shi_fou_you_yi_wang_shi_feng = False
        if shi_fou_you_yi_kan_cha == 'true':
            shi_fou_you_yi_kan_cha = True
        else:
            shi_fou_you_yi_kan_cha = False
        房屋信息 = {
            '受买人姓名':chang_suo_lou_yu_zong_dong_shu,
            '受买人身份证号码':lou_yu_ceng_shu,
            '是否缴纳定金':shi_fou_you_di_xia_ting_cha_chang,
            '是否签到购房合同':shi_fou_you_yi_wang_shi_feng,
            '是否已付清尾款':shi_fou_you_yi_kan_cha
        }
        销售房屋信息表first = 销售房屋信息表.objects(门牌编号=bindMenPaiHao_id).first()
        if 销售房屋信息表first == None:
            if shi_fou_you_di_xia_ting_cha_chang:
                if shi_fou_you_yi_wang_shi_feng:
                    销售状态 = 已出售
                else:
                    销售状态 = 已登记
            else:
                if shi_fou_you_yi_wang_shi_feng:
                    自定义登录状态 = {
                        '描述': '无定金签合同'
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                else:
                    销售状态 = 可出售
            销售房屋信息表(
                门牌编号=bindMenPaiHao_id,
                创建时间=创建时间,
                房屋信息=房屋信息,
                销售状态=销售状态
            ).save()
        else:
            if shi_fou_you_di_xia_ting_cha_chang:
                if shi_fou_you_yi_wang_shi_feng:
                    # if 销售房屋信息表first.销售状态 == 已出售:
                    #     销售状态 = 销售房屋信息表first.销售状态
                    # elif 销售房屋信息表first.销售状态 == 已登记:
                    #     销售状态 = 已出售
                    # elif 销售房屋信息表first.销售状态 == 可出售:
                    #     销售状态 = 已出售
                    # else:
                    #     销售状态 = 已出售
                    销售状态 = 已出售
                else:
                    # if 销售房屋信息表first.销售状态 == 已出售:
                    #     销售状态 = 销售房屋信息表first.销售状态
                    # elif 销售房屋信息表first.销售状态 == 已登记:
                    #     销售状态 = 销售房屋信息表first.销售状态
                    # elif 销售房屋信息表first.销售状态 == 可出售:
                    #     销售状态 = 已登记
                    # else:
                    #     销售状态 = 已登记
                    销售状态 = 已登记
            else:
                if shi_fou_you_yi_wang_shi_feng:
                    自定义登录状态 = {
                        '描述': '无定金签合同'
                    }
                    自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                    自定义登录状态 = str(自定义登录状态)
                    return HttpResponse(自定义登录状态)
                else:
                    # if 销售房屋信息表first.销售状态 == 已出售:
                    #     销售状态 = 销售房屋信息表first.销售状态
                    # elif 销售房屋信息表first.销售状态 == 已登记:
                    #     销售状态 = 销售房屋信息表first.销售状态
                    # elif 销售房屋信息表first.销售状态 == 可出售:
                    #     销售状态 = 销售房屋信息表first.销售状态
                    # else:
                    #     销售状态 = 可出售
                    销售状态 = 可出售
            销售房屋信息表first.update(
                门牌编号=bindMenPaiHao_id,
                创建时间=创建时间,
                房屋信息=房屋信息,
                销售状态=销售状态
            )
        销售楼宇表objs = 销售楼宇表.objects(
            手机号列表__contains=手机号,
            小区编号=小区编号,
            楼宇编号=楼宇编号
        )
        for 销售楼宇表obj in 销售楼宇表objs:
            楼宇详情列表list = []
            for 楼宇详情列表one in 销售楼宇表obj.楼宇详情列表:
                for dan_yuan_one in 楼宇详情列表one['dan_yuan']:
                    for ceng_one in dan_yuan_one['ceng']:
                        men_pai_id = ceng_one['men_pai_id']
                        zhuang_tai = ceng_one['zhuang_tai']
                        if men_pai_id == bindMenPaiHao_id:
                            ceng_one['zhuang_tai'] = 销售状态
                            # if zhuang_tai == 可出售:
                            #     ceng_one['zhuang_tai'] = 已登记
                            # if zhuang_tai == 已登记:
                            #     ceng_one['zhuang_tai'] = 已出售
                楼宇详情列表list.append(楼宇详情列表one)
            销售楼宇表obj.update(楼宇详情列表=楼宇详情列表list)

        自定义登录状态 = {
            '描述': '成功'
        }
        自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
        自定义登录状态 = str(自定义登录状态)
        return HttpResponse(自定义登录状态)
    except:
        print(traceback.format_exc())
        return HttpResponse('500')


def 上传图片(request):
    if request.method == 'POST':
        js_code = request.POST['code']
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {'appid': xiao_shou_appid, 'secret': xiao_shou_secret, 'js_code': js_code,
                   'grant_type': xiao_shou_grant_type}
        r = requests.get(url=url, params=payload)
        print(r.text)
        r_json = json.loads(r.text)
        抽奖用户表first = 销售用户表.objects(openid=r_json['openid']).first()
        if 抽奖用户表first == None:
            自定义登录状态 = {
                '描述': '用户不存在',
                '会话': ''
            }
            自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
            自定义登录状态 = str(自定义登录状态)
            return HttpResponse(自定义登录状态)
        else:
            bindMenPaiHao_id =  request.POST['bindMenPaiHao_id']
            手机号 = 抽奖用户表first.手机号
            当前时间 = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            uploaded_filename = 手机号+'_'+bindMenPaiHao_id+'_'+当前时间+'.jpg'
            销售房屋信息表first = 销售房屋信息表.objects(门牌编号=bindMenPaiHao_id).first()
            if 销售房屋信息表first == None:
                自定义登录状态 = {
                    '描述': '用户不存在',
                    '会话': ''
                }
                自定义登录状态 = json.dumps(自定义登录状态).encode('utf-8').decode('unicode_escape')
                自定义登录状态 = str(自定义登录状态)
                return HttpResponse(自定义登录状态)
            else:
                销售房屋信息表first.update(
                    图片路径 =  uploaded_filename
                )
            # jian_zhu_wi_id = request.POST['jian_zhu_wu_id']
            # jian_zhu_wu_ming_cheng = request.POST['jian_zhu_wu_ming_cheng']
            print(手机号,bindMenPaiHao_id)
            img_file = request.FILES.get('file')
            print(type(img_file))
            folder = request.path.replace("/", "_")
            with open(myConfig.django_root_path + '/'+folder+ '/'+uploaded_filename , 'wb+') as destination:
                for chunk in img_file.chunks():
                    destination.write(chunk)
    return HttpResponse('200')


def 下载图片(request):
    try:
        bindMenPaiHao_id = request.GET['bindMenPaiHao_id']
        # 手机号 = 用户.手机号
        销售房屋信息表first = 销售房屋信息表.objects(门牌编号=bindMenPaiHao_id).first()
        if 销售房屋信息表first == None:
            return ''
        else:
            uploaded_filename = 销售房屋信息表first.图片路径
            path = myConfig.django_root_path + '/' + '_xiao_shou_shang_chuang_tu_pian_' + '/' + uploaded_filename
            outfile = open(path, 'rb')
            response = FileResponse(outfile)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="%s"' % "采集模版表.csv"
            return response
    except:
        print(traceback.format_exc())
        return HttpResponse('500')