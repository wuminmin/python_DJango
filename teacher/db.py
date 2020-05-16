
import pymongo
import myConfig
from . import tool
mongo_src = "mongodb://"+myConfig.teacher_username+":"+myConfig.teacher_password + \
    "@"+myConfig.host+":"+myConfig.port_str+"/?authSource="+myConfig.teacher_db
myclient = pymongo.MongoClient(mongo_src)
mydb = myclient[myConfig.teacher_db]

def teacher_base_info_insert(d,identity_number):
    r = tool.objectid_to_json(mydb.teacher_base_info.find({'identity_number':identity_number}))
    if r == []:
        mydb.teacher_base_info.insert(d)
        return True
    else:
        return False

def teacher_base_info_query_list(my_filter_list):
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
        r = mydb.teacher_base_info.aggregate(pipeline).limit(100)
    else:
        r = mydb.teacher_base_info.aggregate(pipeline)
    r_list = tool.objectid_to_json(r)
    return r_list

def teacher_base_info_delete_by_key(key,value):
    r = mydb.teacher_base_info.remove({key:value})
    return True

def teacher_base_info_update_by_key(key,value,my_temp):
    if '_id' in my_temp:
        my_temp.pop('_id')
    r = mydb.teacher_base_info.update(
        {key:value},
        {'$set':my_temp}
    )
    tool.debug_print(key,value,my_temp,r)
    return True