
def get_my_filter_list(data):
    my_filter_list = [
        {
            'key': "identity_number",
            'input_value': "",
            'input_placeholder': "编号",
            'input_condition': "",
            'key2': "name",
            'input_value2': "",
            'input_placeholder2': "姓名",
            'input_condition2': "",
            'key3': "birthday",
            'input_value3': "",
            'input_placeholder3': "生日",
            'input_condition3': ""
        },
        {
            'key': "gender",
            'input_value': "",
            'input_placeholder': "性别",
            'input_condition': "",
        },
      ]
    res_dict = {
        'code': 20000, 'data': {'my_filter_list':my_filter_list}, 'message': 'message'
    }
    return res_dict