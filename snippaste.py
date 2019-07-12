#此模块主要提供抓图功能，支持以下三种抓图方式：
#1、抓取全屏,快捷键CTRL+F1
#2、抓取当前窗口，快捷键CTRL+F2
#3、抓取所选区域，快捷键CTRL+F3
#抓到之后，会自动弹出保存对话框，选择路径保存即可
#*******************************************
#更新记录
#0.1 2012-03-10 create by dyx1024
#********************************************

import time
from PIL import ImageGrab,Image
import pyautogui

'''使用外部工具'''


def Screenshot():
    pyautogui.press('f1')
    time.sleep(1) 
    image = ImageGrab.grabclipboard()   
    image.save('somefile.png', 'PNG')


if __name__ == "__main__":
    Screenshot()
