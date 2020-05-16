
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
        if 'input_condition' in one:
            if one['input_condition'] == '等于':
                match[one['key']] = one['input_value']
            elif one['input_condition'] == '大于':
                match[one['key']] = {
                    '$gte':one['input_value']
                }
                # match['$gte'] = {
                #     one['key']:one['input_value']
                # }
            elif one['input_condition'] == '小于':
                match[one['key']] = {
                    '$lte':one['input_value']
                }
                # match['$lte'] = {
                #     one['key']:one['input_value']
                # }
            elif one['input_condition'] == '包含':
                match[one['key']] = {
                    '$regex':".*"+one['input_value']+".*"
                }
                # match['$regex'] = {one['key']:".*"+one['input_value']+".*"}
            elif one['input_condition'] == '不包含':
                 match[one['key']] = {
                    '$not':{
                        '$regex':".*"+one['input_value']+".*"

                     }
                }
                # match['$not'] = {
                #     '$regex':{
                #         one['key']: ".*"+one['input_value']+".*"
                #     }
                # }
            else:
                pass
    pipeline.append({
        '$match':match
    })
    tool.debug_print('teacher_base_info_query_list---pipeline---',pipeline)
    if pipeline == []:
        r = mydb.teacher_base_info.aggregate(pipeline).limit(100)
    else:
        r = mydb.teacher_base_info.aggregate(pipeline)
    r_list = tool.objectid_to_json(r)
    tool.debug_print(r_list)
    return r_list
