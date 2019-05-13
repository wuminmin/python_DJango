from mysite.jdgt_mongo import 结对共拓客户经理上传单位信息

# 查询
结对共拓客户经理上传单位信息first = 结对共拓客户经理上传单位信息.objects()
print(type(结对共拓客户经理上传单位信息first))
# print(结对共拓客户经理上传单位信息first.单位名称)
# print(结对共拓客户经理上传单位信息first.客户编码)
# print(结对共拓客户经理上传单位信息first.客户经理)
# print(结对共拓客户经理上传单位信息first.手机号码)

# for a in 结对共拓客户经理上传单位信息first:
#     print(a.单位名称)
#     print(a.客户编码)
#     print(a.客户经理)
#     print(a.手机号码)

# test=结对共拓客户经理上传单位信息first.to_json().encode('utf-8').decode('unicode_escape')
# print(test)

# 删除
test1=结对共拓客户经理上传单位信息.objects(单位名称='池州电信')
print(test1)
test1.delete()

#更新
test2=结对共拓客户经理上传单位信息.objects(单位名称='池州电信2')
print(test2)
test2.update(
单位名称='池州电信3'
)

# 增加
结对共拓客户经理上传单位信息(
单位名称='池州电信0'
).save()

test=结对共拓客户经理上传单位信息first.to_json().encode('utf-8').decode('unicode_escape')
print(test)