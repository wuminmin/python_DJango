
import pymongo
import myConfig
from . import tool
mongo_src = "mongodb://"+myConfig.teacher_username+":"+myConfig.teacher_password + \
    "@"+myConfig.host+":"+myConfig.port_str+"/?authSource="+myConfig.teacher_db
myclient = pymongo.MongoClient(mongo_src)
mydb = myclient[myConfig.teacher_db]

def teacher_base_info_insert(d,identity_number):
    r = tool.objectid_to_json(mydb.teacher_base_info.find({'identity_number':identity_number}))
    tool.debug_print('teacher_base_info_insert---',r)
    if r == []:
        mydb.teacher_base_info.insert(d)
        return True
    else:
        return False

def teacher_base_info_query_list(my_filter_list):
    pipeline = [ ]
    match = {}
    for one in my_filter_list:
        if 'input_condition0' in one:
            if one['input_condition0'] == '包含':
                match[one['key0']] = one['input_value0']
            elif one['input_condition0'] == '不包含':
                match[one['key0']] = {
                    '$not':{
                        '$regex': ".*"+one['input_value0']+".*"
                    }
                }
        if 'input_condition1' in one:
            if one['input_condition1'] == '包含':
                match[one['key1']] = one['input_value1']
            elif one['input_condition1'] == '不包含':
                match[one['key1']] = one['input_value1']
        if 'input_condition2' in one:
            if one['input_condition2'] == '包含':
                match[one['key2']] = one['input_value2']
            elif one['input_condition2'] == '不包含':
                match[one['key2']] = one['input_value2']
    pipeline.append({
        '$match':match
    })
    tool.debug_print(pipeline)
    if pipeline == []:
        r = mydb.teacher_base_info.aggregate(pipeline).limit(100)
    else:
        r = mydb.teacher_base_info.aggregate(pipeline)
    r_list = tool.objectid_to_json(r)
    tool.debug_print(r_list)
    return r_list
