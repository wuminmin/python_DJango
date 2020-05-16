
import pymongo
import myConfig
from . import tool
mongo_src = "mongodb://"+myConfig.teacher_username+":"+myConfig.teacher_password + \
    "@"+myConfig.host+":"+myConfig.port_str+"/?authSource="+myConfig.teacher_db
myclient = pymongo.MongoClient(mongo_src)
mydb = myclient[myConfig.teacher_db]

def teacher_base_info_insert(table_name,d):
    tool.debug_print('teacher_base_info_insert--',d)
    if table_name == 'teacher_base_info':
        mydb.teacher_base_info.insert(d)
        return True
    elif table_name == 'teacher_work_info':
        mydb.teacher_work_info.insert(d)
        return True
    else:
        return False

def teacher_base_info_query_list(table_name,my_filter_list):
    pipeline = []
    match = {}
    for one in my_filter_list:
        if 'input_condition' in one:
            if one['input_condition'] == '等于':
                match[one['key']] = one['input_value']
            elif one['input_condition'] == '大于':
                match[one['key']] = {
                    '$gte':one['input_value']
                }
            elif one['input_condition'] == '小于':
                match[one['key']] = {
                    '$lte':one['input_value']
                }
            elif one['input_condition'] == '包含':
                match[one['key']] = {
                    '$regex':".*"+one['input_value']+".*"
                }
            elif one['input_condition'] == '不包含':
                 match[one['key']] = {
                    '$not':{
                        '$regex':".*"+one['input_value']+".*"
                     }
                }
            else:
                pass
    pipeline.append({
        '$match':match
    })
    if pipeline == []:
        if table_name == 'teacher_base_info':
            r = mydb.teacher_base_info.aggregate(pipeline).limit(100)
        else:
            r = []
    else:
        if table_name == 'teacher_base_info':
            r = mydb.teacher_base_info.aggregate(pipeline)
        else:
            r = []
    r_list = tool.objectid_to_json(r)
    return r_list

def teacher_base_info_delete_by_key(table_name,key,value):
    print('teacher_base_info_delete_by_key',table_name)
    if table_name == 'teacher_base_info':
        r = mydb.teacher_base_info.remove({key:value})
        return True
    else:
        return False

def teacher_base_info_update_by_key(table_name,key,value,my_temp):
    if '_id' in my_temp:
        my_temp.pop('_id')
    if table_name == 'teacher_base_info':
        r = mydb.teacher_base_info.update(
            {key:value},
            {'$set':my_temp}
        )
    else:
        r = {}
    tool.debug_print(key,value,my_temp,r)
    if 'updatedExisting' in r:
        if r['updatedExisting']:
            return True
    return False