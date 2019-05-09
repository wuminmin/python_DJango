
""" 读取图片 """
from aip import AipSpeech, AipOcr


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

image = get_file_content('IMG_20190304_220418.jpg')
""" 你的 APPID AK SK """
APP_ID = '15680859'
API_KEY = '1Tfn60ipyC1BHYYdStflilBW'
SECRET_KEY = 'VL2kW5r5YF10SKHR42DG54mC2gvzexkl'
# client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

if __name__ == '__main__':

    # """ 调用通用文字识别（高精度版） """
    # r = client.basicAccurate(image);
    # print(r)
    #
    # """ 如果有可选参数 """
    # options = {}
    # options["detect_direction"] = "true"
    # options["probability"] = "true"

    """ 带参数调用通用文字识别（高精度版） """
    # client.basicAccurate(image, options)

    # """ 调用通用文字识别（含位置信息版）, 图片参数为本地图片 """
    r = client.general(image);
    print(r)
    #
    # """ 如果有可选参数 """
    # options = {}
    # options["recognize_granularity"] = "big"
    # options["language_type"] = "CHN_ENG"
    # options["detect_direction"] = "true"
    # options["detect_language"] = "true"
    # options["vertexes_location"] = "true"
    # options["probability"] = "true"
    #
    # """ 带参数调用通用文字识别（含位置信息版）, 图片参数为本地图片 """
    # # client.general(image, options)
    #
    # url = "http//www.x.com/sample.jpg"
    #
    # """ 调用通用文字识别（含位置信息版）, 图片参数为远程url图片 """
    # # client.generalUrl(url);
    #
    # """ 如果有可选参数 """
    # options = {}
    # options["recognize_granularity"] = "big"
    # options["language_type"] = "CHN_ENG"
    # options["detect_direction"] = "true"
    # options["detect_language"] = "true"
    # options["vertexes_location"] = "true"
    # options["probability"] = "true"
    #
    # """ 带参数调用通用文字识别（含位置信息版）, 图片参数为远程url图片 """
    # client.generalUrl(url, options)

