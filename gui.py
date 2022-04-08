#!/usr/bin/python
# -*- coding: UTF-8 -*-

from email import message
from tkinter.constants import BOTH, E, END, INSERT, LEFT, N, TOP, W, X, YES

from PIL import Image, ImageGrab
from time import sleep

import pyperclip
import os
import tkinter as tk          # 导入 Tkinter 库
from tkinter import Y,ttk
from tkinter import * 
import tkinter.messagebox
import traceback
import IMG_Tran_TEXT as Itt
import Text_transAPI as TextT


About = "版本号信息 v1.2 \n 一款小而美的Ocr软件，该软件仅用于交流学习应用，禁止任何形式的商用行为" 

#默认配置项
default_lang = 'en'
current_lang = default_lang

root = tk.Tk()                     # 创建窗口对象的背景色
root.title('图像转文字 v2.0')
root.geometry('500x300')


fm1 = ttk.Frame(root)
fm2 = ttk.Frame(root)
fm3 = ttk.Frame(root)

def clearEdit(Editx):
        Editx.delete('1.0',END)
        Editx.configure(fg='black')  # 修改字体颜色，修改其它参数只需要传入对应的参数即可


#图片识别的结果显示在Edit1
def OcrDisplayCallback():
    clearEdit(Edit1)
    clearEdit(Edit2)
    Edit1.insert(INSERT,pyperclip.paste())


def TransCallback():
    clearEdit(Edit2)
    var = TextT.TextTranslate(current_lang,Edit1.get('1.0',END))
    Edit2.insert(INSERT,var)
    fm3.pack(side=LEFT, fill=BOTH, expand=YES)

var= tk.StringVar()

starkabe = tk.PhotoImage(file = "star.png")
  
B = ttk.Button(fm1, text="打开图像",command = lambda:Ocrtranslated(),width=5)
G = ttk.Button(fm1, text="屏幕截图",command=lambda:buttonCaptureClick(),width=5)
D = ttk.Button(fm1,text = "显示结果",command = lambda:OcrDisplayCallback(),width=5)

#具体用法

Notice = ttk.Label(fm1,anchor='center',image=starkabe,textvariable=var, wraplength = 130,foreground='grey', font=('Microsoft Yahei', 10),compound="top")
var.set('请打开图片或截图')

#窗口大小不可变化
#root.resizable(True, False)  

#在图形界面上设定输入框控件entry并放置控件
#Edit1 = tk.Text(fm1, show='*', font=('Courier New', 12))   # 显示成密文形式
#Edit2 = tk.Text(fm3, show=None, font=('Courier New', 12))  # 显示成明文形式
OcrRes = ttk.Label(fm2, text='识别结果', font=('Microsoft Yahei', 10), width=10)
Edit1 = tk.Text(fm2,width=10, height=5,padx=1,pady=1, undo = True,font=("Microsoft Yahei",10))

TransButton = ttk.Button(fm2,text = "翻译 >",command = lambda:TransCallback(),width=10)
TransRes = ttk.Label(fm3, text='翻译结果', font=('Microsoft Yahei', 10), width=10)
Edit2 = tk.Text(fm3,width=10, height=5,padx=1,pady=1, undo = True,font=("Microsoft Yahei",10))

#语言菜单
languages = {"英语":"en", "简中":"zh",  "日语":"jp", "西班牙语": "spa",
              "韩语":"kor",  "繁中":"cht",  "意大利语":"it", "捷克语":"cs"}

v = tk.Variable()
v.set('英语')
'''
OPTIONS = []
for k,v in languages.items():
    OPTIONS.append(k)
'''

def setlang(event): 
    global current_lang  
    print(v.get())
    current_lang = languages.get(v.get())  


TransChoose = ttk.OptionMenu(fm2, v , '',
                            "英语", 
                            "简中", 
                            "日语",
                            "西班牙语",
                            "韩语", 
                            "繁中",
                            "意大利语", 
                            "捷克语"
                            ,command=setlang)


#撤销、重做
def back():
    try:
        Edit1.edit_undo()
        Edit2.edit_undo()
    except Exception as e:
        traceback.print_exc()
    

def callback():
    try:
        Edit1.edit_redo()
        Edit2.edit_redo()
    except Exception as e:
        traceback.print_exc()


def showAbout():
    tkinter.messagebox.showinfo(title='Topic', message= About,)



#菜单栏
menubar = tk.Menu(root)
root.config(menu=menubar)

#添加菜单选项
menu1 = tk.Menu(menubar,borderwidth = 3,tearoff=False)
menubar.add_cascade(label="历史记录", menu=menu1)

menubar.add_command(label="关于",command = showAbout)
menubar.add_command(label="撤销↶",command = back)
menubar.add_command(label="重做↷",command = callback)


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
            self.top, bg='blue', width=screenWidth, height=screenHeight)
        
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
                self.X.get(), self.Y.get(), event.x, event.y, outline='blue')

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



#用来显示全屏幕截图并响应二次截图的窗口类
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


def Ocrtranslated():
    if Itt.Transform_GT(Itt.High_precision):
        var.set('识别完成，结果已复制到粘贴板')
    else:
        var.set('')




#右键 剪切复制黏贴
def callback1(event=None):
    global root
    Edit1.event_generate('<<Cut>>')
    Edit2.event_generate('<<Cut>>')
    
def callback2(event=None):
    global root
    Edit1.event_generate('<<copy>>')
    Edit2.event_generate('<<copy>>')
    
def callback3(event=None):
    global root
    Edit1.event_generate('<<Paste>>')
    Edit2.event_generate('<<Paste>>')

def callback4(event=None):
    global root
    Edit1.event_generate('<<Paste>>')
    Edit2.event_generate('<<Paste>>')

'''创建一个弹出菜单'''
menu = tk.Menu(root,
            tearoff=False,
            #bg="grey",
            )
menu.add_command(label="剪切", command=callback1)
menu.add_command(label="复制", command=callback2)
menu.add_command(label="黏贴", command=callback3)

def popup(event):
    menu.post(event.x_root, event.y_root)   # post在指定的位置显示弹出菜单

Edit1.bind("<Button-3>", popup)                 # 绑定鼠标右键,执行popup函数
Edit2.bind("<Button-3>", popup)                 # 绑定鼠标右键,执行popup函数


#--------------右键弹窗End--------------------------


def popup(event):
    menu.post(event.x_root, event.y_root)   # post在指定的位置显示弹出菜单

#Frame1
B.pack(side=TOP,anchor=W,fill=X,expand=N)
G.pack(side=TOP,anchor=W,fill=X,expand=N)
D.pack(side=TOP,anchor=W,fill=X,expand=N)
Notice.pack(side=TOP,anchor=W,fill=BOTH,expand=Y)

#Frame2
OcrRes.pack(side=TOP,anchor=W,fill=X,expand=N) 
Edit1.pack(side=TOP,anchor=W,fill=BOTH,expand=Y)
TransChoose.pack(side=LEFT,anchor=W,fill=BOTH,expand=Y)
TransButton.pack(side=LEFT,anchor=W,fill=BOTH,expand=Y)


#Frame3
TransRes.pack(side=TOP,anchor=W,fill=X,expand=N) 
Edit2.pack(side=TOP,anchor=W,fill=BOTH,expand=Y)

fm1.pack(side=LEFT, fill=BOTH, expand=YES)
fm2.pack(side=LEFT, fill=BOTH, expand=YES)
fm3.forget()

# 将小部件放置到主窗口中
root.mainloop() 
 
