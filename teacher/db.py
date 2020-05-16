
import pymongo
import myConfig
from . import tool
mongo_src = "mongodb://"+myConfig.teacher_username+":"+myConfig.teacher_password + \
    "@"+myConfig.host+":"+myConfig.port_str+"/?authSource="+myConfig.teacher_db
myclient = pymongo.MongoClient(mongo_src)
mydb = myclient[myConfig.teacher_db]

def teacher_base_info_insert(table_name,d):
    if table_name == '基本信息':
        mydb.基本信息.insert(d)
        return True
    elif table_name == '工作信息':
        mydb.工作信息.insert(d)
        return True
    elif table_name == '学历信息':
        mydb.学历信息.insert(d)
        return True
    elif table_name == '工作履历':
        mydb.工作履历.insert(d)
        return True
    elif table_name == '考核信息':
        mydb.考核信息.insert(d)
        return True
    elif table_name == '家庭信息':
        mydb.家庭信息.insert(d)
        return True
    elif table_name == '专业技术职务':
        mydb.专业技术职务.insert(d)
        return True
    elif table_name == '职业资格名称':
        mydb.职业资格名称.insert(d)
        return True
    elif table_name == '奖励情况':
        mydb.奖励情况.insert(d)
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
        if table_name == '基本信息':
            r = mydb.基本信息.aggregate(pipeline).limit(100)
        elif table_name == '工作信息':
            r = mydb.工作信息.aggregate(pipeline).limit(100)
        elif table_name == '学历信息':
            r = mydb.学历信息.aggregate(pipeline).limit(100)
        elif table_name == '工作履历':
            r = mydb.工作履历.aggregate(pipeline).limit(100)
        elif table_name == '考核信息':
            r = mydb.考核信息.aggregate(pipeline).limit(100)
        elif table_name == '家庭信息':
            r = mydb.家庭信息.aggregate(pipeline).limit(100)
        elif table_name == '专业技术职务':
            r = mydb.专业技术职务.aggregate(pipeline).limit(100)
        elif table_name == '职业资格名称':
            r = mydb.职业资格名称.aggregate(pipeline).limit(100)
        elif table_name == '奖励情况':
            r = mydb.奖励情况.aggregate(pipeline).limit(100)
        else:
            r = []
    else:
        if table_name == '基本信息':
            r = mydb.基本信息.aggregate(pipeline)
        elif table_name == '工作信息':
            r = mydb.工作信息.aggregate(pipeline)
        elif table_name == '学历信息':
            r = mydb.学历信息.aggregate(pipeline)
        elif table_name == '工作履历':
            r = mydb.工作履历.aggregate(pipeline)
        elif table_name == '考核信息':
            r = mydb.考核信息.aggregate(pipeline)
        elif table_name == '家庭信息':
            r = mydb.基本信息.aggregate(pipeline)
        elif table_name == '专业技术职务':
            r = mydb.专业技术职务.aggregate(pipeline)
        elif table_name == '职业资格名称':
            r = mydb.职业资格名称.aggregate(pipeline)
        elif table_name == '奖励情况':
            r = mydb.奖励情况.aggregate(pipeline)
        else:
            r = []
    r_list = tool.objectid_to_json(r)
    return r_list

def teacher_base_info_delete_by_key(table_name,key,value):
    if table_name == '基本信息':
        mydb.基本信息.remove({key:value})
        return True
    elif table_name == '工作信息':
        mydb.工作信息.remove({key:value})
        return True
    elif table_name == '学历信息':
        mydb.学历信息.remove({key:value})
        return True
    elif table_name == '工作履历':
        mydb.工作履历.remove({key:value})
        return True
    elif table_name == '考核信息':
        mydb.考核信息.remove({key:value})
        return True
    elif table_name == '家庭信息':
        mydb.家庭信息.remove({key:value})
        return True
    elif table_name == '专业技术职务':
        mydb.专业技术职务.remove({key:value})
        return True
    elif table_name == '职业资格名称':
        mydb.职业资格名称.remove({key:value})
        return True
    elif table_name == '奖励情况':
        mydb.奖励情况.remove({key:value})
        return True
    else:
        return False

def teacher_base_info_update_by_key(table_name,key,value,my_temp):
    if '_id' in my_temp:
        my_temp.pop('_id')
    if table_name == '基本信息':
        r = mydb.基本信息.update(
            {key:value},
            {'$set':my_temp}
        )
    elif table_name == '工作信息':
        r = mydb.工作信息.update(
            {key:value},
            {'$set':my_temp}
        )
    elif table_name == '学历信息':
        r = mydb.学历信息.update(
            {key:value},
            {'$set':my_temp}
        )
    elif table_name == '工作履历':
        r = mydb.工作履历.update(
            {key:value},
            {'$set':my_temp}
        )
    elif table_name == '考核信息':
        r = mydb.考核信息.update(
            {key:value},
            {'$set':my_temp}
        )
    elif table_name == '家庭信息':
        r = mydb.家庭信息.update(
            {key:value},
            {'$set':my_temp}
        )
    elif table_name == '专业技术职务':
        r = mydb.专业技术职务.update(
            {key:value},
            {'$set':my_temp}
        )
    elif table_name == '职业资格名称':
        r = mydb.职业资格名称.update(
            {key:value},
            {'$set':my_temp}
        )
    elif table_name == '奖励情况':
        r = mydb.奖励情况.update(
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