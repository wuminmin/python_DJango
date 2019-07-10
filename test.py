import json

import requests
任务调度器添加任务HTTP = 'http://127.0.0.1:8000/v1/api/'
sss = '''{
    "sender": "GPELE",
    "time": "2016-11-06 09:07:54",
    "type": "传输维护作业工单",
    "service": "派单",
"data": [ {
 "WSID": "2018062500166",
  "APTROUBLETYPE": "传输维护工单",
                    "Emergencylevel": "一般(四级) ",
                    "Status":"完成",
                    "Applytime": "2018-06-25 09:08:37",
                    "Completetime": "2018-03-14 14:54:12",
                    "WorkOrderInformation": "DWDM 2010武汉长沙广州南宁80*40Gb/sDWDM系统（华为） 波分系统劣化（维护作业）",
                    "Note": "波分系统劣化（维护作业）%/系统=2010武汉长沙广州南宁80*40Gb/sDWDM系统（华为）/复用段=广州电信大厦-南宁民族/系统段=云浮云城区马岗-云浮罗定冲花【7250-云浮云城区马岗-0-2-12OAU1-4(发云浮罗定冲花)~7251-云浮罗定冲花-0-2-12OAU1-1(收云浮云城区马岗发云浮罗定龙园)】",
                    "Associatedsystemnumber": "关联系统编号",
                    "Associatedworkorder": "关联工单",
                    "Remainingtime": " 22:21",
                    "ChartererA": "戴琦",
                    "ChartererAmail": " zhouql@chinatelecom.cn",
                    "ChartererAphone": "15313331554",
                    "ChartererB": "赵子郁",
                    "ChartererBmail": "zhangbxcx@shtel.com.cn",
                    "ChartererBphone": "18916721217",
                    "NetworkType": "网络类型： DWDM",
                    "Trunkname": "2015上海南京合肥武汉80*100Gb/s DWDM系统(华为)",
                    "Whethercrossborder": "是否跨境： 否",
                    "FailuresiteA": "10315-无锡黄巷(上海方向)-0-8-13OAU1-4(OUT(发苏州方向))",
                    "MultiplexsectionsiteA":"无锡黄巷",
                    "FailuresiteZ": "10314-苏州闾邱坊-0-16-13OAU1-1(IN(收无锡黄巷))",
                    "MultiplexsectionsiteZ":"苏州闾邱坊局",
                    "Alarmname": "告警名称： 波分系统劣化（维护作业）",
                    "EMSmanufacturers": "EMS厂家： 华为",
                    "Whetherinternational": "是否国际： ",
                    "systemname": "系统名称：",
                    "Activeandstandbyconditions": "主备情况：",
                    "Asideequipment": "A端设备",
                    "Aendrack": "A端机架",
                    "Aendslot": "A端槽位",
                    "Aport": "A端端口",
                    "Asidealarm": "A端告警",
                    "Zsideequipment": "Z端设备",
                    "Zendrack": "Z端机架",
                    "Zendslot": "Z端槽位",
                    "Zport": "Z端端口",
                    "Zsidealarm": "Z端告警",
                    "Faultsource": "故障来源： 综合告警转传输维护单",
                    "Associatedalarms": "关联告警： 2010武汉长沙广州南宁80*40Gb/sDWDM系统（华为）",
                    "Failuretime": "故障发生时间： 2018-03-12 07:03:10 ",
                    "Faultdescription": "故障描述： 波分系统劣化（维护作业）%/系统=2010武汉长沙广州南宁80*40Gb/sDWDM系统（华为）/复用段=广州电信大厦-南宁民族/系统段=云浮云城区马岗-云浮罗定冲花【7250-云浮云城区马岗-0-2-12OAU1-4(发云浮罗定冲花)~7251-云浮罗定冲花-0-2-12OAU1-1(收云浮云城区马岗发云浮罗定龙园)】"
          }]
}'''
payload = {'data': sss}
print(payload)
r = requests.get(任务调度器添加任务HTTP, params=payload, verify=False).text
print(r)