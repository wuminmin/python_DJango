
def get_my_basic_filter_list(data):
    my_table_header_list = [
        {'id':1,'name':'编号','key':'main_id'},
        {'id':2,'name':'姓名','key':'name'},
        {'id':3,'name':'性别','key':'gender'},
        {'id':4,'name':'出生日期','key':'birth_day'},
        {'id':5,'name':'民族','key':'nation'},
        {'id':6,'name':'身份证','key':'identity_number'},
        {'id':7,'name':'籍贯','key':'birth_area'},
        {'id':8,'name':'政治面貌','key':'political_status'},
        {'id':9,'name':'入党日期','key':'join_party_day'},
        {'id':10,'name':'参加工作日期','key':'join_work_day'},
        {'id':11,'name':'婚姻状况','key':'marital_status'},
        {'id':12,'name':'出生地','key':'birth_place'},
        {'id':13,'name':'户口所在地','key':'hu_kou_location'},
        {'id':14,'name':'办公电话','key':'work_phone'},
        {'id':15,'name':'手机号码','key':'cell_phone'},
        {'id':16,'name':'电子邮件','key':'email'},
        {'id':17,'name':'紧急联系人姓名','key':'emergency_contact_name'},
        {'id':18,'name':'紧急联系人电话','key':'emergency_contact_phone'},
    ]
    my_filter_list = []
    i = 0
    filter_dict = {}
    for one in my_table_header_list:
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
            'my_table_header_list':my_table_header_list,
            'my_filter_list':my_filter_list
        }, 'message': 'message'
    }
    return res_dict

def get_my_basic_table_list(data):
    my_table_list = [
        {
            'd':{
                'main_id':'1',
                'name':'',
                'gender':'',
                'birth_day':'',
                'nation':'',
                'identity_number':'341002222',
                'birth_area':'birth_area',
                'political_status':'',
                'join_party_day':'',
                'join_work_day':'',
                'marital_status':'未婚',
                'birth_place':'',
                'hu_kou_location':'',
                'work_phone':'',
                'cell_phone':'',
                'email':'',
                'emergency_contact_name':'',
                'emergency_contact_phone':'',
            }
        },
        {
            'd':{
                'main_id':'2',
                'name':'',
                'gender':'',
                'birth_day':'',
                'nation':'',
                'identity_number':'341003',
                'birth_area':'birth_area',
                'political_status':'',
                'join_party_day':'',
                'join_work_day':'',
                'marital_status':'未婚',
                'birth_place':'',
                'hu_kou_location':'',
                'work_phone':'',
                'cell_phone':'',
                'email':'',
                'emergency_contact_name':'',
                'emergency_contact_phone':'',
            }
        },
    ]
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





