from . import db
#自定义的工具函数----------------------------------------------
import json
import uuid
import sys

def objectid_to_json(data): #转换ObjectId未'$oid'
    import json
    from bson import json_util, ObjectId
    res = json.loads(json_util.dumps(data))
    return res

def get_str_of_now_time(i):
    import time
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 86400*i))

def get_str_of_date(i):
    import time
    return time.strftime('%Y-%m-%d', time.localtime(time.time()+ 86400*i))

def str_to_json(json_str):
    return json.loads(json_str.encode('utf-8').decode('unicode_escape'))

def qset_to_json(qset):
    return json.loads(qset.to_json().encode('utf-8').decode('unicode_escape'))

def create_32_bit_main_id():
    return str( uuid.uuid1() ).replace('-','')

def debug_print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False):
    flag = True
    if flag:
        print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)

def traceback_print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False):
    flag = True
    if flag:
        print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)
#--------------------------------------------------
# table_info_list = [
#     {'id':1,'name':'基本信息','table_name':'teacher_base_info'},
#     {'id':2,'name':'工作信息','table_name':'teacher_work_info'},
#     {'id':3,'name':'学历信息','table_name':'teacher_education_info'},
#     {'id':4,'name':'工作履历','table_name':'teacher_resume_info'},
#     {'id':5,'name':'考核信息','table_name':'teacher_assessment_info'},
#     {'id':6,'name':'家庭信息','table_name':'teacher_family_info'},
#     {'id':7,'name':'专业技术职务','table_name':'teacher_profession_info'},
#     {'id':8,'name':'职业资格名称','table_name':'teacher_occupation_info'},
#     {'id':9,'name':'奖励情况','table_name':'teacher_reward_info'},
# ]
table_info_list = [
    {'id':1,'name':'基本信息','table_name':'基本信息'},
    {'id':2,'name':'工作信息','table_name':'工作信息'},
    {'id':3,'name':'学历信息','table_name':'学历信息'},
    {'id':4,'name':'工作履历','table_name':'工作履历'},
    {'id':5,'name':'考核信息','table_name':'考核信息'},
    {'id':6,'name':'家庭信息','table_name':'家庭信息'},
    {'id':7,'name':'专业技术职务','table_name':'专业技术职务'},
    {'id':8,'name':'职业资格名称','table_name':'职业资格名称'},
    {'id':9,'name':'奖励情况','table_name':'奖励情况'},
]

# table_header_dict = {
#     'teacher_base_info':[
#         {'id':1,'name':'编号','key':'main_id'},
#         {'id':2,'name':'姓名','key':'name'},
#         {'id':3,'name':'性别','key':'gender'},
#         {'id':4,'name':'出生日期','key':'birth_day'},
#         {'id':5,'name':'民族','key':'nation'},
#         {'id':6,'name':'身份证','key':'identity_number'},
#         {'id':7,'name':'籍贯','key':'birth_area'},
#         {'id':8,'name':'政治面貌','key':'political_status'},
#         {'id':9,'name':'入党日期','key':'join_party_day'},
#         {'id':10,'name':'参加工作日期','key':'join_work_day'},
#         {'id':11,'name':'婚姻状况','key':'marital_status'},
#         {'id':12,'name':'出生地','key':'birth_place'},
#         {'id':13,'name':'户口所在地','key':'hu_kou_location'},
#         {'id':14,'name':'办公电话','key':'work_phone'},
#         {'id':15,'name':'手机号码','key':'cell_phone'},
#         {'id':16,'name':'电子邮件','key':'email'},
#         {'id':17,'name':'紧急联系人姓名','key':'emergency_contact_name'},
#         {'id':18,'name':'紧急联系人电话','key':'emergency_contact_phone'},
#     ]
# }

table_header_dict = {
    '基本信息':[
        {'id':1,'name':'编号','key':'编号'},
        {'id':2,'name':'身份证','key':'身份证'},
        {'id':3,'name':'姓名','key':'姓名'},
        {'id':4,'name':'出生日期','key':'出生日期'},
        {'id':5,'name':'民族','key':'民族'},
        {'id':6,'name':'性别','key':'性别'},
        {'id':7,'name':'籍贯','key':'籍贯'},
        {'id':8,'name':'政治面貌','key':'政治面貌'},
        {'id':9,'name':'入党日期','key':'入党日期'},
        {'id':10,'name':'参加工作日期','key':'参加工作日期'},
        {'id':11,'name':'婚姻状况','key':'婚姻状况'},
        {'id':12,'name':'出生地','key':'出生地'},
        {'id':13,'name':'户口所在地','key':'户口所在地'},
        {'id':14,'name':'办公电话','key':'办公电话'},
        {'id':15,'name':'手机号码','key':'手机号码'},
        {'id':16,'name':'电子邮件','key':'电子邮件'},
        {'id':17,'name':'紧急联系人姓名','key':'紧急联系人姓名'},
        {'id':18,'name':'紧急联系人电话','key':'紧急联系人电话'},
    ],
    '工作信息':[
        {'id':1,'name':'编号','key':'编号'},
        {'id':2,'name':'身份证','key':'身份证'},
        {'id':3,'name':'部门','key':'部门'},
        {'id':4,'name':'岗位序列','key':'岗位序列'},
        {'id':5,'name':'岗位','key':'岗位'},
        {'id':6,'name':'现职时间','key':'现职时间'},
        {'id':7,'name':'任现职岗位等级时间','key':'任现职岗位等级时间'},
    ],
    '学历信息':[
        {'id':1,'name':'编号','key':'编号'},
        {'id':2,'name':'身份证','key':'身份证'},
        {'id':3,'name':'入学日期','key':'入学日期'},
        {'id':4,'name':'毕业日期','key':'毕业日期'},
        {'id':5,'name':'学校','key':'学校'},
        {'id':6,'name':'专业','key':'专业'},
        {'id':7,'name':'学历','key':'学历'},
        {'id':8,'name':'学位','key':'学位'},
        {'id':9,'name':'学习方式','key':'学习方式'},
    ],
    '工作履历':[
        {'id':1,'name':'编号','key':'编号'},
        {'id':2,'name':'身份证','key':'身份证'},
        {'id':3,'name':'履历开始日期','key':'履历开始日期'},
        {'id':4,'name':'履历结束日期','key':'履历结束日期'},
        {'id':5,'name':'工作单位','key':'工作单位'},
        {'id':6,'name':'所在部门','key':'所在部门'},
        {'id':7,'name':'岗位','key':'岗位'},
        {'id':8,'name':'职务','key':'职务'},
    ],
    '考核信息':[
        {'id':1,'name':'编号','key':'编号'},
        {'id':2,'name':'身份证','key':'身份证'},
        {'id':3,'name':'考核开始日期','key':'考核开始日期'},
        {'id':4,'name':'考核结束日期','key':'考核结束日期'},
        {'id':5,'name':'考核等级','key':'考核等级'},
        {'id':6,'name':'考核单位','key':'考核单位'},
    ],
    '家庭信息':[
        {'id':1,'name':'编号','key':'编号'},
        {'id':2,'name':'身份证','key':'身份证'},
        {'id':3,'name':'称谓','key':'称谓'},
        {'id':4,'name':'姓名','key':'姓名'},
        {'id':5,'name':'生日','key':'生日'},
        {'id':6,'name':'政治面貌','key':'政治面貌'},
        {'id':7,'name':'工作单位','key':'工作单位'},
        {'id':8,'name':'职务','key':'职务'},
    ],
    '专业技术职务':[
        {'id':1,'name':'编号','key':'编号'},
        {'id':2,'name':'身份证','key':'身份证'},
        {'id':3,'name':'技术职务名称','key':'技术职务名称'},
        {'id':4,'name':'取得时间','key':'取得时间'},
    ],
    '职业资格名称':[
        {'id':1,'name':'编号','key':'编号'},
        {'id':2,'name':'职业资格名称','key':'职业资格名称'},
        {'id':3,'name':'取得时间','key':'取得时间'},
        {'id':4,'name':'资格等级','key':'资格等级'},
        {'id':5,'name':'批准单位','key':'批准单位'},
    ],
    '奖励情况':[
        {'id':1,'name':'编号','key':'编号'},
        {'id':2,'name':'奖励类别','key':'奖励类别'},
        {'id':3,'name':'奖励机构','key':'奖励机构'},
        {'id':4,'name':'奖励时间','key':'奖励时间'},
        {'id':5,'name':'奖励事由','key':'奖励事由'},
        {'id':6,'name':'奖励名称','key':'奖励名称'},
    ],
}

def get_my_basic_filter_list(data,method_dict):
    my_table_header_list = table_header_dict[method_dict['table_name']]
    my_filter_list = []
    i = 0
    filter_dict = {}
    export_excel_header_name_list = []
    export_excel_header_key_list = []
    for one in my_table_header_list:
        export_excel_header_name_list.append(one['name'])
        export_excel_header_key_list.append(one['key'])
        if i == 0:
            name = one['name']
            key = one['key']
            filter_dict['key'+str(i%3)] = key
            filter_dict['input_value'+str(i%3)] = ''
            filter_dict['input_placeholder'+str(i%3)] = name
            filter_dict['input_condition'+str(i%3)] = ''
        elif i%3 == 0 :
            my_filter_list.append(filter_dict)
            filter_dict = {}
            name = one['name']
            key = one['key']
            filter_dict['key'+str(i%3)] = key
            filter_dict['input_value'+str(i%3)] = ''
            filter_dict['input_placeholder'+str(i%3)] = name
            filter_dict['input_condition'+str(i%3)] = ''
        else:
            name = one['name']
            key = one['key']
            filter_dict['key'+str(i%3)] = key
            filter_dict['input_value'+str(i%3)] = ''
            filter_dict['input_placeholder'+str(i%3)] = name
            filter_dict['input_condition'+str(i%3)] = ''
        i = i +1
    my_filter_list.append(filter_dict)
    res_dict = {
        'code': 20000, 'data': {
            'export_excel_header_name_list':export_excel_header_name_list,
            'export_excel_header_key_list':export_excel_header_key_list,
            'my_table_header_list':my_table_header_list,
            'my_filter_list':my_filter_list,
        }, 'message': 'message'
    }
    return res_dict

def handle_my_filter_list_tmp_key0(one):
    if 'key0' in one and 'input_value0' in one and 'input_condition0' in one:
        key = one['key0']
        input_value = one['input_value0']
        input_condition = one['input_condition0']
        return {'key':key,'input_value':input_value,'input_condition':input_condition}
    else:
        return None

def handle_my_filter_list_tmp_key1(one):
    if 'key1' in one and 'input_value1' in one and 'input_condition1' in one:
        key = one['key1']
        input_value = one['input_value1']
        input_condition = one['input_condition1']
        return {'key':key,'input_value':input_value,'input_condition':input_condition}
    else:
        return None

def handle_my_filter_list_tmp_key2(one):
    if 'key2' in one and 'input_value2' in one and 'input_condition2' in one:
        key = one['key2']
        input_value = one['input_value2']
        input_condition = one['input_condition2']
        return {'key':key,'input_value':input_value,'input_condition':input_condition}
    else:
        return None

def get_my_basic_table_list(data,method_dict):
    data = json.loads(data)
    my_filter_list = []
    if 'my_filter_list' in  data :
        my_filter_list_tmp = data['my_filter_list']
        for one in my_filter_list_tmp:
            r = handle_my_filter_list_tmp_key0(one)
            if not r == None:
                my_filter_list.append(r)
            r = handle_my_filter_list_tmp_key1(one)
            if not r == None:
                my_filter_list.append(r)
            r = handle_my_filter_list_tmp_key2(one)
            if not r == None:
                my_filter_list.append(r)
    my_table_list = db.teacher_base_info_query_list(method_dict['table_name'],my_filter_list)
    total = len(my_table_list)
    res_dict = {
        'code': 20000, 
        'data': {
            'total':total,
            'my_table_list':my_table_list
        }, 
        'message': '基本信息表'
    }
    return res_dict

def create_row(data,method_dict):
    data = json.loads(data)
    my_temp = data['my_temp']
    my_temp['编号'] = create_32_bit_main_id()
    for one in table_header_dict[method_dict['table_name']]:
        key = one['key']
        if key in my_temp:
            pass
        else:
            my_temp[key] = ''
    if db.teacher_base_info_insert(method_dict['table_name'],my_temp):
        res_dict = {'code': 20000, 'data': {}, 'message': '新增成功'}
    else:
        res_dict = {'code': 3, 'data': {}, 'message': '新增失败'}
    return res_dict

def delete_row(data,method_dict):
    data = json.loads(data)
    my_temp = data['my_temp']
    if not '编号' in my_temp:
        return {'code': 1, 'data': {}, 'message': '编号不存在!'}
    main_id = my_temp['编号']
    if not db.teacher_base_info_delete_by_key(method_dict['table_name'],'编号',main_id):
        return {'code': 2, 'data': {}, 'message': '删除失败'}
    return {'code': 20000, 'data': {}, 'message': '删除成功'}

def update_row(data,method_dict):
    data = json.loads(data)
    my_temp = data['my_temp']
    if not '编号' in my_temp:
        return {'code': 1, 'data': {}, 'message': '编号不存在!'}
    main_id = my_temp['编号']
    if not db.teacher_base_info_update_by_key(method_dict['table_name'],'编号',main_id,my_temp):
        return {'code': 2, 'data': {}, 'message': '修改失败'}
    return {'code': 20000, 'data': {}, 'message': '修改成功'}

def import_excel_init(data,method_dict):
    data = json.loads(data)
    table_name_list = []
    for one in table_info_list:
        table_name_list.append({'key':one['table_name'],'name':one['name']})
    return {'code':20000,'data':{'table_name_list':table_name_list},'message':'上传excel初始化'}

def import_excel_data(data,method_dict):
    data = json.loads(data)
    tableData = data['tableData']
    for one in tableData:
        one['编号'] = create_32_bit_main_id()
        db.teacher_base_info_insert(method_dict['table_name'],one)
    return {'code':20000,'data':{},'message':method_dict['table_name']+'导入成功'}

