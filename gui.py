#!/usr/bin/python
# -*- coding: UTF-8 -*-

from PIL import Image, ImageGrab
from time import sleep

import pyperclip
import os
import tkinter as tk          # 导入 Tkinter 库
import tkinter.messagebox

import IMG_Tran_TEXT as Itt
# import snippaste as sp 使用外部工具

root = tk.Tk()                     # 创建窗口对象的背景色
root.title('图像转文字v1.0')
root.geometry("300x150")
                                # 创建两个列表
def TransCallback():
    tkinter.messagebox.showinfo( "识别结果", pyperclip.paste())

var= tk.StringVar()

B = tk.Button(root, text="打开图像",command = lambda:translated(),width=10)
G = tk.Button(root, text="屏幕截图", command=lambda:buttonCaptureClick(),width=10)
D = tk.Button(root,text = "显示结果",command = lambda:TransCallback(),width=10)
Notice = tk.Label(root, textvariable=var, fg='blue', font=('Microsoft Yahei', 10), width=30, height=2)

root.resizable(False, False)
#用来显示全屏幕截图并响应二次截图的窗口类


class MyCapture:
    def __init__(self, png):
        #变量X和Y用来记录鼠标左键按下的位置
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        #屏幕尺寸
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()

        #创建顶级组件容器
        self.top = tkinter.Toplevel(
            root, width=screenWidth, height=screenHeight)

        #不显示最大化、最小化按钮
        self.top.overrideredirect(True)
        self.canvas = tkinter.Canvas(
            self.top, bg='white', width=screenWidth, height=screenHeight)

        #显示全屏截图，在全屏截图上进行区域截图
        self.image = tkinter.PhotoImage(file=png)
        self.canvas.create_image(
            screenWidth//2, screenHeight//2, image=self.image)

        def onRightButtonDown(event):
            self.top.destroy()
            os.remove(filename)
            root.state('normal')
        self.canvas.bind('<Button-3>', onRightButtonDown)

        #鼠标左键按下的位置
        def onLeftButtonDown(event):
            self.X.set(event.x)
            self.Y.set(event.y)
            #开始截图
            self.sel = True
        self.canvas.bind('<Button-1>', onLeftButtonDown)

        #鼠标左键移动，显示选取的区域
        def onLeftButtonMove(event):
            if not self.sel:
                return
            global lastDraw
            try:
                #删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
                self.canvas.delete(lastDraw)
            except Exception as e:
                pass
            lastDraw = self.canvas.create_rectangle(
                self.X.get(), self.Y.get(), event.x, event.y, outline='black')

        self.canvas.bind('<B1-Motion>', onLeftButtonMove)

        #获取鼠标左键抬起的位置，保存区域截图
        def onLeftButtonUp(event):
            self.sel = False
            '''try:
                self.canvas.delete(lastDraw)
            except Exception as e:
                pass
                '''
            sleep(0.1)
            #考虑鼠标左键从右下方按下而从左上方抬起的截图
            left, right = sorted([self.X.get(), event.x])
            top, bottom = sorted([self.Y.get(), event.y])
            pic = ImageGrab.grab((left+1, top+1, right, bottom))
            #弹出保存截图对话框
            file_path = './somefile.png'
            pic.save(file_path, 'PNG')
            sleep(1)

            '''
            fileName = tkinter.filedialog.asksaveasfilename(
                title='保存截图', filetypes=[('image', '*.jpg *.png')])
            
            if fileName:
                pic.save(fileName)
            '''
            #关闭当前窗口
            self.top.destroy()
            return pic
        self.canvas.bind('<ButtonRelease-1>', onLeftButtonUp)
#让canvas充满窗口，并随窗口自动适应大小
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)

 #开始截图


def buttonCaptureClick():

    #最小化主窗口
    root.state('icon')
    sleep(0.2)
    global filename
    filename = 'temp.png'

#grab()方法默认对全屏幕进行截图

    im = ImageGrab.grab()
    im.save(filename)
    im.close()
    #显示全屏幕截图
    w = MyCapture(filename)
    G.wait_window(w.top)
    #截图结束，恢复主窗口，并删除临时的全屏幕截图文件
    root.state('normal')
    os.remove(filename)
    Catch_chipboard()

"""Keyboard overwatch"""
def call_back(event):
    buttonCaptureClick()
root.bind("<Control-Shift-KeyPress-S>", call_back)


def Catch_chipboard():

    file_path = './somefile.png'
    image = Itt.get_file_content(file_path)
    if Itt.Transform_GT(Itt.High_precision, image):
        var.set('识别完成，结果已复制到粘贴板')
    else:        
        var.set('')    



def translated():
    if Itt.Transform_GT(Itt.High_precision):
        var.set('识别完成，结果已复制到粘贴板')
    else:
        var.set('')

B.pack()
G.pack()
D.pack()
Notice.pack()
                # 将小部件放置到主窗口中
root.mainloop() 
 
