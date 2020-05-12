
def deprecated_async(f): # 异步函数
    def wrapper(*args, **kwargs):
        from threading import Thread
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

def myHttpResponse(res):  # 合并跨域配置
    import json
    from django.http import HttpResponse, FileResponse
    response = HttpResponse(json.dumps(res))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def login(request):  # vue管理后台登录
    import json
    import traceback
    import time
    from . import manage_models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        req_body = request.body.decode('utf-8')
        req_json = json.loads(req_body)
        username = req_json['username']
        password = req_json['password']
        print(username, password)
        q1 = manage_models.my_user.objects(
            __raw__={'d.username': username, 'd.password': password}
        ).first()
        if q1 == None:
            code = 60204
            data = {'token': ''}
            message = '账号或者密码错误'
            res = {'code': code, 'data': data, 'message': message}
        else:
            tmp_d = q1.d
            from . import manage_token
            import myConfig
            tokenprogramer = manage_token.Token(
                api_secret = myConfig.wx_app_id, #微信appid
                project_code = 'canteen', #项目名称
                account = username #用户名
            )
            tmp_d['token'] = tokenprogramer.get_token()
            q1.update(d = tmp_d )
            code = 20000
            data = {'token': tokenprogramer.get_token()}
            message = '登录成功'
            res = {'code': code, 'data': data, 'message': message}
        return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        res = {'code': 500, 'data': {}, 'message': '系统故障'}
        return myHttpResponse(res)

def info(request):  # vue后台获取用户信息
    import json
    import traceback
    from . import manage_models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        token = request.GET['token']
        print(token)
        q1 = manage_models.my_user.objects(__raw__ = {'d.token':token}).first()
        if q1 == None:
            code = 50008
            data = {}
            message = '已超时，请重新登录'
            res = {'code':code,'data':data,'message':message}
        else:
            code = 20000
            data = {
                'roles': ['admin'],
                'introduction': 'I am a super administrator',
                'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
                'name': 'Super Admin'
            }
            message = '登录成功'
            res = {'code': code, 'data': data, 'message': message}
        return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        res = {'code': 500, 'data': {}, 'message': '系统故障'}
        return myHttpResponse(res)

def logout(request):
    import json
    import traceback
    from . import manage_models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    try:
        req_body = request.body.decode('utf-8')
        print(req_body)
        code = 20000
        data = 'success'
        message = '退出成功'
        res = {'code': code, 'data': data, 'message': message}
        return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        res = {'code': 500, 'data': {}, 'message': '系统故障'}
        return myHttpResponse(res)

@deprecated_async
def async_import_excel(mydata,flag,action):
    # from mysite import ding_can_mongo as ding_can_mongo #老版订餐后台
    from . import models as ding_can_mongo  #新版订餐后台
    print(mydata)
    import pandas
    import time
    try:
        if action == '上传用餐人员清单':
            df_main = pandas.read_json(mydata,encoding="utf-8", orient='records')
            手机号_list = []
            主菜单id_list = []
            for row_main in df_main.iterrows():
                手机号 = str(row_main[1]['手机号'])
                主菜单id = row_main[1]['主菜单id']
                if 手机号 in 手机号_list:
                    pass
                else:
                    手机号_list.append(手机号)
                if 主菜单id in 主菜单id_list:
                    pass
                else:
                    主菜单id_list.append(主菜单id)
            for 手机号 in 手机号_list:
                主界内容 = []
                df_手机号 = df_main.loc[(df_main['手机号'] == int(手机号))]
                for row in df_手机号.iterrows():
                    创建时间 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    描述 = str(row[1]['描述'])
                    主页标题 = str(row[1]['主页标题'])
                    主页描述 = str(row[1]['主页描述'])
                    验证码标题 = str(row[1]['验证码标题'])
                    验证码描述 = str(row[1]['验证码描述'])
                    二级部门 = str(row[1]['二级部门'])
                    三级部门 = str(row[1]['三级部门'])
                    四级部门 = str(row[1]['四级部门'])
                    姓名 = str(row[1]['姓名'])
                    主菜单name = str(row[1]['主菜单name'])
                    主菜单id = str(row[1]['主菜单id'])
                    df_手机号_主菜单name = df_main.loc[(df_main['手机号'] == int(手机号)) & (df_main['主菜单name'] == 主菜单name)]
                    pages = []
                    for index, row in df_手机号_主菜单name.iterrows():
                        子菜单page_name = row['子菜单page_name']
                        子菜单page_desc = row['子菜单page_desc']
                        子菜单url = row['子菜单url']
                        page = {}
                        page['url'] = 子菜单url
                        page['page_name'] = 子菜单page_name
                        page['page_desc'] = 子菜单page_desc
                        if page in pages:
                            pass
                        else:
                            pages.append(page)
                    主菜单id_dict = {
                        'id': 主菜单id,
                        'name': 主菜单name,
                        'open': False,
                        'pages': pages
                    }
                    if 主菜单id_dict in 主界内容:
                        pass
                    else:
                        主界内容.append(主菜单id_dict)
                    主界面表_one = ding_can_mongo.订餐主界面表.objects(手机号=str(手机号)).first()
                    if 主界面表_one == None:
                        ding_can_mongo.订餐主界面表(手机号=str(手机号), 描述=str(描述), 创建时间=str(创建时间), 主页标题=str(主页标题), 主页描述=str(主页描述), 验证码标题=str(验证码标题)
                            , 验证码描述=str(验证码描述),二级部门=二级部门,三级部门=三级部门,四级部门=四级部门,姓名=姓名, 主界内容=主界内容).save()
                    else:
                        主界面表_one.update(手机号=str(手机号), 描述=str(描述), 创建时间=str(创建时间), 主页标题=str(主页标题), 主页描述=str(主页描述), 验证码标题=str(验证码标题)
                            , 验证码描述=str(验证码描述),二级部门=二级部门,三级部门=三级部门,四级部门=四级部门,姓名=姓名, 主界内容=主界内容)
            ding_can_mongo1 = ding_can_mongo.订餐导入时间戳表.objects(flag=flag).first()
            if ding_can_mongo1 == None:
                ding_can_mongo.订餐导入时间戳表(
                    flag=flag,
                    isOk=True
                ).save()
            else:
                ding_can_mongo1.update(isOk=True)
        elif action == '上传充值清单':
            df_main = pandas.read_json(mydata,encoding="utf-8", orient='records')
            for row_main in df_main.iterrows():
                手机号 = str(row_main[1]['手机号'])
                充值金额 = row_main[1]['充值金额']
                备注 = row_main[1]['备注']
                ding_can_mongo.订餐钱包充值表(
                    手机号=手机号,
                    充值金额 = int(充值金额),
                    充值时间=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                    备注 = 备注
                ).save()
            ding_can_mongo1 = ding_can_mongo.订餐导入时间戳表.objects(flag=flag).first()
            if ding_can_mongo1 == None:
                ding_can_mongo.订餐导入时间戳表(
                    flag=flag,
                    isOk=True
                ).save()
            else:
                ding_can_mongo1.update(isOk=True)
        else:
            print('无效请求')
    except:
        import traceback
        r = traceback.format_exc()
        print(r)
        ding_can_mongo1 = ding_can_mongo.订餐导入时间戳表.objects(flag=flag).first()
        if ding_can_mongo1 == None:
            ding_can_mongo.订餐导入时间戳表(
                flag=flag,
                isOk=False,
                eLog={'log':r}
            ).save()
        else:
            ding_can_mongo1.update(isOk=False,eLog={'log':r})

def upload_canteen_list(request):
    import json
    import traceback
    from . import manage_models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    from . import models as ding_can_mongo  #新版订餐后台
    try:
        req_body = request.body.decode('utf-8')
        print(req_body)
        req_json = json.loads(req_body)
        mydata = req_json['data']
        mydata = json.dumps(mydata)
        flag =  req_json['flag']
        action = req_json['key']
        token = req_json['token']
        q1 = manage_models.my_user.objects(__raw__ = {'d.token':token}).first()
        if q1 == None:
            code = 50008
            data = {}
            message = '已超时，请重新登录'
            res = {'code':code,'data':data,'message':message}
            return myHttpResponse(res)
        else:
            if action == '上传用餐人员清单':
                async_import_excel(mydata,flag,action)
                code = 20000
                data = 'success'
                message = '正在处理'
                res = {'code': code, 'data': data, 'message': message}
                return myHttpResponse(res)
            elif action == '上传充值清单':
                async_import_excel(mydata,flag,action)
                code = 20000
                data = 'success'
                message = '正在处理'
                res = {'code': code, 'data': data, 'message': message}
                return myHttpResponse(res)
            elif action == '查询结果':
                ding_can_mongo1 = ding_can_mongo.订餐导入时间戳表.objects(flag=flag).first()
                if ding_can_mongo1 == None:
                    message = '正在处理'
                else:
                    if ding_can_mongo1.isOk :
                        message = '成功'
                    else:
                        message = '失败'
                code = 20000
                data = 'success'
                res = {'code': code, 'data': data, 'message': message}
                return myHttpResponse(res)
            else:
                code = 20000
                data = 'success'
                message = '退出成功'
                res = {'code': code, 'data': data, 'message': message}
                return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        res = {'code': 500, 'data': {}, 'message': '系统故障'}
        return myHttpResponse(res)

def export_canteen_data(request):
    import json
    import traceback
    from . import manage_models
    from . import models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    from . import models as ding_can_mongo  #新版订餐后台
    import myConfig
    try:
        req_body = request.body.decode('utf-8')
        print(req_body)
        req_json = json.loads(req_body)
        token = req_json['token']
        q1 = manage_models.my_user.objects(__raw__ = {'d.token':token}).first()
        if q1 == None:
            code = 50008
            data = {}
            message = '已超时，请重新登录'
            res = {'code':code,'data':data,'message':message}
        key =  req_json['key']
        if key == '导出充值清单':
            value_start = req_json['value_start']
            value_end = req_json['value_end']
            ql2 = models.订餐钱包充值表.objects(
                充值时间__gte = value_start + ' 00:00:00',
                充值时间__lte = value_end + ' 23:59:59' 
            )
            code = 20000
            data = { 
                'total':len(ql2),
                'items': json.loads(ql2.to_json().encode('utf-8').decode('unicode_escape'))
            }
            message = '成功'
            res = {'code': code, 'data': data, 'message': message}
            return myHttpResponse(res)
        elif key == '导出消费清单':
            value_start = req_json['value_start']
            value_end = req_json['value_end']
            ql2 = models.订餐结果表.objects(用餐日期__gte = value_start,用餐日期__lte = value_end )
            产品全局字典 = ding_can_mongo.产品全局字典
            产品名称列表 = 产品全局字典[myConfig.wx_app_id]['产品名称列表']
            items = []
            for o in ql2:
                手机号 = o.手机号
                用餐日期 = o.用餐日期
                产品 = ','
                for o2 in 产品名称列表:
                    名称 = o2
                    if 名称 in o.产品:
                        预定数量 = o.产品[o2]['预定数量']
                        签到 = o.产品[o2]['签到']
                        项目 = 名称+','+str(预定数量)+','+签到
                        产品 = 产品+项目+','
                items.append({
                    '手机号':手机号,
                    '用餐日期':用餐日期,
                    '产品':产品
                })
                产品 = ','
            code = 20000
            data = {
                'total':len(ql2),
                'items':items,
            }
            message = '成功'
            res = {'code': code, 'data': data, 'message': message}
            return myHttpResponse(res)
        elif key == '导出员工清单':
            ql2 = models.订餐主界面表.objects()
            items = []
            for one in ql2:
                items.append({
                            '手机号':one.手机号,
                            '描述':one.描述,
                            '创建时间':one.创建时间,
                            '主页标题':one.主页标题,
                            '主页描述':one.主页描述,
                            '验证码标题':one.验证码标题,
                            '验证码描述':one.验证码描述,
                            '二级部门':one.二级部门,
                            '三级部门':one.三级部门,
                            '四级部门':one.四级部门,
                            '姓名':one.姓名,
                            '主界内容':one.主界内容
                        })
            code = 20000
            data = {
                'total':len(ql2),
                'items': items
            }
            message = '成功'
            res = {'code': code, 'data': data, 'message': message}
            return myHttpResponse(res)
        else:
            code = 20000
            data = {
                'total':0,
                'items':[]
            }
            message = '成功'
            res = {'code': code, 'data': data, 'message': message}
            return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        res = {'code': 500, 'data': {}, 'message': '系统故障'}
        return myHttpResponse(res)

def base_table_fetchList(request):
    import json
    import traceback
    from . import manage_models
    from . import models
    from django.http import HttpResponse, FileResponse
    from django.http import JsonResponse
    from . import models as ding_can_mongo  #新版订餐后台
    import myConfig
    from . import tool
    try:
        code = request.GET['code']
        if code == 1 or code == '1':
            data = request.GET['data']
            message = request.GET['message']
            res = tool.get_my_filter_list(data)
        else:
            res = {'code': 0, 'data': {}, 'message': '参数错误'}
        return myHttpResponse(res)
    except:
        print(traceback.format_exc())
        res = {'code': 500, 'data': {}, 'message': '系统故障'}
        return myHttpResponse(res)




























