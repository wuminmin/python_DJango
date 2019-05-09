from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '15273029'
API_KEY = 'skY2wM5whRPfHgC7vc9DrsmW'
SECRET_KEY = 'UblS7MlmG30UWZjKCLL8p5HEZ9M0SG1A '

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

result = client.synthesis('柯英杰工程优化做好了吗？', 'zh', 1, {
    'vol': 5, 'per': 4
})

# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
if not isinstance(result, dict):
    with open('auido.mp3', 'wb') as f:
        f.write(result)
