from mongoengine import *

# 数据库连接
import myConfig
# disconnect(alias='default')
connect(alias='teacher_alias',db=myConfig.teacher_db, host=myConfig.teacher_host, port=myConfig.teacher_port, username=myConfig.teacher_username, password=myConfig.teacher_password)

teacher_global_dict = {
    'table_key_name_list':[
        'base_info',
        'work_info',
    ]
     'base_info':{

    },
    'work_info':{
        'row_key_name_list':[
            'identity_number',
            'department',
            'job_sequence',
            'job_name',
            'job_date',
            'working_time',
        ],
        'row_key_condition_list':[
            'identity_number',
            'department',
            'job_sequence',
            'job_name',
            'job_date',
            'working_time',
        ]
        'identity_number':{},
        'department':{},
        'job_sequence':{},
        'job_name':{},
        'job_date':{},
        'working_time':{},

    },
   
}

class my_user(Document):#用户表
    meta = {"db_alias": "teacher_alias"}
    d = DictField(default={})

class teacher_base_info(Document): #教师基本信息
    meta = {"db_alias": "teacher_alias"}
    d = DictField(default={})













