import pyperclip
from aip import AipOcr

import tkinter as tk
from tkinter import filedialog

High_precision = 1
Low_precision = 0


def IS_Linefeed(sentence):
    flag = 0
    Linefeed_sign = {'.','。',':','：'}
    for sign in Linefeed_sign:
        if sentence.endswith(sign):
            flag = 1
    return flag
           


""" Read image """
def get_file_content(filePath):
    try:   
        with open(filePath, "rb") as fp:        
            return fp.read()
    except FileNotFoundError:
        return 0

""" Transform graph to text 
return: none
parm:选择是高精度还是低精度 1.高精度 0。低精度
"""
def Transform_GT(accuracy_option):
    
    Recognize = accuracy_option

    """
    User AppID AK SK
    AK = API_KEY
    SK = Secret_KEY
    """
    APP_ID = '16289977'
    AK = '1UUME9IqLLRwlbrQFcjePBwe'
    SK = '0wNmCRtXgNGpvwGVNxFewiqqzrgKvwUv'

    client = AipOcr(APP_ID, AK, SK)

    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title='打开需要识别的图片',
        filetypes=[('JPG','*.jpg'),('BMP','*.bmp'),('PNG','*.bmp')])  # 获取文件的打开路径

    print(file_path)
    file_path = str(file_path)
   
    image = get_file_content(file_path)
    
    """ Generasion object Calling """
    try:
        client.basicGeneral(image)
    except TypeError:
        return 0
    """ IF there are optional parameter  """
    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"

    """ 带参数调用通用文字识别，图片参数为本地图片 """
    if Recognize == 0:
        word = client.basicGeneral(image, options)
    elif Recognize == 1:
        word = client.basicAccurate(image, options)
    print("识别结果如下，共识别出 {[words_result_num]} 段文字".format(word))
    data_layer = "words_result"


    words_buffer = ""

    for layer in word.keys():
        if layer == data_layer:
            layer_obj = word[layer]
            for layer1 in layer_obj:
                if isinstance(layer1, dict):
                    try:
                        
                        if IS_Linefeed("{[words]}".format(layer1)):                           
                            words_buffer += ("{[words]}".format(layer1) + "\n")
                        else:                          
                            words_buffer += (("{[words]}").format(layer1))
                    except KeyError:
                        pass

    #将文本黏贴至剪贴板
    pyperclip.copy(words_buffer)
    print(words_buffer)
    return words_buffer
    ##spam = pyperclip.paste()


if __name__ == "__main__":
    Transform_GT(High_precision)
