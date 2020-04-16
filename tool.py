import json
import uuid
import sys

def get_str_of_now_time():
    import time
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

def str_to_json(json_str):
    return json.loads(json_str.encode('utf-8').decode('unicode_escape'))

def qset_to_json(qset):
    return json.loads(qset.to_json().encode('utf-8').decode('unicode_escape'))

def create_uuid1n():
    return str( uuid.uuid1() )

def debug_print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False):
    flag = True
    if flag:
        print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)

def traceback_print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False):
    flag = True
    if flag:
        print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)
