
def is_holiday(riqi):
    riqi_2 = riqi.replace('-','')
    print(riqi_2)
    import requests
    import json
    payload = {'date': riqi_2}
    r = requests.get("http://api.goseek.cn/Tools/holiday", params=payload)
    r_text = r.text
    r_json = json.loads(r_text)
    print(r_json['data'])
    if r_json['data'] == 0 or r_json['data'] == 2:
        return False
    elif r_json['data'] == 1 or r_json['data'] == 3:
        return True
    else:
        return 'error'

if __name__ == "__main__":
    r = is_holiday('2019-11-10')
    print(r)