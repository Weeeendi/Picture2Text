#!/usr/bin/python
# -*- coding: UTF-8 -*-
import IMG_Tran_TEXT as Itt
import pyperclip
import tkinter as tk          # 导入 Tkinter 库
import tkinter.messagebox
root = tk.Tk()                     # 创建窗口对象的背景色
root.title('图像转文字v1.0')
root.geometry("300x150")
                                # 创建两个列表
def TransCallback():
    tkinter.messagebox.showinfo( "翻译结果", pyperclip.paste())

translated_flag = False
var= tk.StringVar()

B = tk.Button(root, text="打开图像",command = lambda:translated(),width=10)
G = tk.Button(root,text = "屏幕截图(未实现)",width=10)
D = tk.Button(root,text = "显示结果",command = lambda:TransCallback(),width=10)
Notice = tk.Label(root, textvariable=var, fg='blue', font=('Microsoft Yahei', 10), width=30, height=2)

def translated():
    global translated_flag
    if Itt.Transform_GT(Itt.High_precision):
        translated_flag = True
        var.set('识别完成，结果已复制到粘贴板')
    else:
        translated_flag = False
        var.set('')

B.pack()
G.pack()
D.pack()
Notice.pack()
                # 将小部件放置到主窗口中
root.mainloop() 
 
