#!/usr/bin/python
# -*- coding: UTF-8 -*-

from tkinter.constants import BOTH, E, END, INSERT, LEFT, N, TOP, W, X, YES
from turtle import color

from PIL import ImageGrab
from time import sleep
from minIcon import SysTrayIcon

import pyperclip
import os
import tkinter as tk          # 导入 Tkinter 库
from tkinter import Y,ttk
from tkinter import * 
import tkinter.messagebox
import traceback
import IMG_Tran_TEXT as Itt
import Text_transAPI as TextT


About = "版本号信息 v1.2 \n\n 一款小而美的Ocr软件\n该软件仅用于交流学习应用，禁止任何形式的商用行为" 
Shareble = 1


#默认配置项
default_lang = 'en'
current_lang = default_lang


def message_askyesno(root):
    '''
    # Gets the requested values of the height and width.
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()

    # Gets both half the screen width/height and window width/height
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    '''
    root.withdraw()  # ****实现主窗口隐藏
    root.update()  # *********需要update一下
    
    return (tk.messagebox.askyesno("提示","要执行此操作？"))
   


def clearEdit(Editx):
        Editx.delete('1.0',END)
       # Editx.configure(fg='black')  # 修改字体颜色，修改其它参数只需要传入对应的参数即可


#图片识别的结果显示在Edit1
def OcrDisplayCallback(Edit1,Edit2):
    clearEdit(Edit1)
    clearEdit(Edit2)
    Edit1.insert(INSERT,pyperclip.paste())


def TransCallback(Edit1,Edit2,fm):
    clearEdit(Edit2)
    var = TextT.TextTranslate(current_lang,Edit1.get('1.0',END))
    Edit2.insert(INSERT,var)
    fm.pack(side=LEFT, fill=BOTH, expand=YES)
 
#语言菜单
languages = {"英语":"en", "简中":"zh",  "日语":"jp", "西班牙语": "spa",
              "韩语":"kor",  "繁中":"cht",  "意大利语":"it", "捷克语":"cs","法语":"fra"}

'''
OPTIONS = []
for k,v in languages.items():
    OPTIONS.append(k)
'''
def showAbout():
    tkinter.messagebox.showinfo(title='Topic', message= About,)

class MyCapture:
    def __init__(self, png, root):
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
            file_path = './image/somefile.png'
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

application_path = "./image/"
iconFile = "icon.ico"
        
class _Main:  #调用SysTrayIcon的Demo窗口
    def __init__(s):
        s.SysTrayIcon  = None  # 判断是否打开系统托盘图标

    def popup(s,event):
        s.menu.post(event.x_root, event.y_root)   # post在指定的位置显示弹出菜单

    def setlang(s,event): 
        global current_lang  
        print(s.v.get())
        current_lang = languages.get(s.v.get())  

    def Edit_about(s,action):
        '''option obtain "back","callback","clear","copy"."cut","paste",'''
        #撤销、重做
        
        if(action == "back"):
            try:
                s.Edit1.edit_undo()
                s.Edit2.edit_undo()
            except Exception as e:
                traceback.print_exc()
    
        if(action == "callback"):
            try:
                s.Edit1.edit_redo()
                s.Edit2.edit_redo()
            except Exception as e:
                traceback.print_exc()

        if(action == "clear"):
            try:
                s.Edit1.delete('1.0',END)
                s.Edit2.delete('1.0',END)
            except Exception as e:
                traceback.print_exc()

        if(action == "cut"):
            s.Edit2.event_generate('<<Cut>>')
            s.Edit1.event_generate('<<Cut>>')
            
        if(action == "copy"):
            s.Edit1.event_generate('<<copy>>')
            s.Edit2.event_generate('<<copy>>')
            
        if(action == "Paste"):
            s.Edit2.event_generate('<<Paste>>')
            s.Edit1.event_generate('<<Paste>>')
    #用来显示全屏幕截图并响应二次截图的窗口类


    def buttonCaptureClick(s):
        #当前在截图.不支持最小化判断
        global Shareble
        Shareble = 0
        isNormal = 0
        #最小化主窗口
        if(s.root.state() == "normal"):
            s.root.withdraw() #隐藏tk窗口
            isNormal = 1
        #s.root.state('icon')
        sleep(0.2)
        global filename
        filename = 'temp.png'

        #grab()方法默认对全屏幕进行截图

        im = ImageGrab.grab()
        im.save(filename)
        im.close()
        #显示全屏幕截图
        w = MyCapture(filename,s.root)
        s.G.wait_window(w.top)
        #截图结束，恢复主窗口，并删除临时的全屏幕截图文件
        os.remove(filename)
        s.Catch_chipboard()
        if(isNormal):
            s.root.deiconify()
        else:
            s.resume()
        Shareble = 1

    def display(s):
        #Frame1
        s.B.pack(side=TOP,anchor=W,fill=X,expand=N)
        s.G.pack(side=TOP,anchor=W,fill=X,expand=N)
        s.D.pack(side=TOP,anchor=W,fill=X,expand=N)
        s.Notice.pack(side=TOP,anchor=W,fill=BOTH,expand=Y)

        #Frame2
        s.OcrRes.pack(side=TOP,anchor=W,fill=X,expand=N) 
        s.Edit1.pack(side=TOP,anchor=W,fill=BOTH,expand=Y)
        
        s.TransButton.pack(side=LEFT,anchor=CENTER,fill=X,expand=Y)
        s.TransChoose.pack(side=RIGHT,anchor=W,fill=BOTH,expand=Y)

        #Frame3
        s.TransRes.pack(side=TOP,anchor=W,fill=X,expand=N) 
        s.Edit2.pack(side=TOP,anchor=W,fill=BOTH,expand=Y)

        s.fm1.pack(side=LEFT, fill=BOTH, expand=YES)
        s.fm2.pack(side=LEFT, fill=BOTH, expand=YES)
        s.fm3.forget()

    def switch_icon(s, _sysTrayIcon, icon = 'D:\\2.ico'):
        #点击右键菜单项目会传递SysTrayIcon自身给引用的函数，所以这里的_sysTrayIcon = s.sysTrayIcon
        #只是一个改图标的例子，不需要的可以删除此函数
        _sysTrayIcon.icon = icon
        _sysTrayIcon.refresh()
        
        #气泡提示的例子
        s.show_msg(title = '图标更换', msg = '图标更换成功！', time = 500)
    
    def show_msg(s, title = '标题', msg = '内容', time = 500):
        s.SysTrayIcon.refresh(title = title, msg = msg, time = time)

    def Hidden_window(s, icon = './image./icon.ico', hover_text = "图文精灵"):
        '''隐藏窗口至托盘区，调用SysTrayIcon的重要函数'''

        #托盘图标右键菜单, 格式: ('name', None, callback),下面也是二级菜单的例子
        #24行有自动添加‘退出’，不需要的可删除
        
        menu_options=(('打开主界面', None,s.resume), 
                      ('识别图像', None, (('截图', None,s.buttonCaptureClick),('打开图像', None,s.Ocrtranslated))),
                      ('退出', None,s.beforeExit)
                      )       

        s.root.withdraw()   #隐藏tk窗口
        if not s.SysTrayIcon: s.SysTrayIcon = SysTrayIcon(
                                        icon,               #图标
                                        hover_text,         #光标停留显示文字
                                        menu_options,       #右键菜单
                                        on_quit = s.beforeExit,   #退出调用
                                        tk_window = s.root, #Tk窗口
                                        )
        s.SysTrayIcon.activation()

    def resume(s):
        s.SysTrayIcon.destroy(exit = 0)


    def exit(s, _sysTrayIcon=None):
        s.root.destroy()
        print ('exit...')

    def beforeExit(s):
        s.SysTrayIcon.destroy(exit=0)
        sleep(1.0)
        s.root.update()
        s.exit()

    def Catch_chipboard(s):
        file_path = './image/somefile.png'
        image = Itt.get_file_content(file_path)
        if Itt.Transform_GT(Itt.High_precision, image):
            s.varInFm1.set('识别完成，结果已复制到粘贴板')
        else:        
            s.varInFm1.set('未识别到文字信息')
        
    def Ocrtranslated(s):
        if Itt.Transform_GT(Itt.High_precision):
            s.varInFm1.set('识别完成，结果已复制到粘贴板')
        else:
            s.varInFm1.set('未识别到文字信息')

        print(s.root.state())
        if(s.root.state() == "withdrawn"):
            s.resume()

        

    def main(s):
        #tk窗口
        s.root = tk.Tk()
        s.root.title('图像转文字 v2.0')
        s.root.geometry('500x300+100+100')
        s.fm1 = ttk.Frame(s.root,takefocus= "blue")
        s.fm2 = ttk.Frame(s.root)
        s.fm3 = ttk.Frame(s.root)
     
        s.varInFm1= StringVar()
        starkabe = tk.PhotoImage(file = "./image/background.png")
        s.Notice = ttk.Label(s.fm1,anchor='center',image=starkabe,textvariable=s.varInFm1, wraplength = 130,foreground='grey', font=('Microsoft Yahei', 12),compound="top")
        s.varInFm1.set('请打开图片或截图')

        #窗口大小不可变化
        #root.resizable(True, False)  

        #在图形界面上设定输入框控件entry并放置控件
        #Edit1 = tk.Text(fm1, show='*', font=('Courier New', 12))   # 显示成密文形式
        #Edit2 = tk.Text(fm3, show=None, font=('Courier New', 12))  # 显示成明文形式

        '''Farme1 function area'''

        s.B = ttk.Button(s.fm1, text="打开图像",command =s.Ocrtranslated,width=5)
        s.G = ttk.Button(s.fm1, text="屏幕截图",command=s.buttonCaptureClick,width=5)
        s.D = ttk.Button(s.fm1,text = "显示结果",command = lambda:OcrDisplayCallback(s.Edit1,s.Edit2),width=5)

        s.OcrRes = ttk.Label(s.fm2, text='识别结果', font=('Microsoft Yahei', 10), width=10)
        s.Edit1 = tk.Text(s.fm2,width=10, height=5,padx=10,pady=1, undo = True,font=("Microsoft Yahei",9))
        s.TableStr = ttk.Label(s.fm2, anchor='e',text='To:', font=('Microsoft Yahei', 10))

        s.TransButton = ttk.Button(s.fm2,text = "翻译成 >",command = lambda:TransCallback(s.Edit1,s.Edit2,s.fm3),width=10)
        s.TransRes = ttk.Label(s.fm3, text='翻译结果', font=('Microsoft Yahei', 10), width=10)
        s.Edit2 = tk.Text(s.fm3,width=10, height=5,padx=10,pady=1, undo = True,font=("Microsoft Yahei",9))

        '''创建一个弹出菜单'''
        
        s.menu = tk.Menu(s.root,
            tearoff=False,
            #bg="grey",
            )
        s.menu.add_command(label="剪切", command=s.Edit_about("cut"))
        s.menu.add_command(label="复制", command=s.Edit_about("copy"))
        s.menu.add_command(label="黏贴", command=s.Edit_about("paste"))

        s.Edit1.bind("<Button-3>", s.popup)                 # 绑定鼠标右键,执行popup函数
        s.Edit2.bind("<Button-3>", s.popup)               # 绑定鼠标右键,执行popup函数

        s.v = Variable()
        s.v.set('英语')
        '''Farme2 function area'''
        s.TransChoose = ttk.OptionMenu(s.fm2, s.v , '',
                            "英语", 
                            "简中", 
                            "日语",
                            "西班牙语",
                            "韩语", 
                            "繁中",
                            "意大利语", 
                            "捷克语",
                            "法语"
                            ,command=s.setlang)

        #菜单栏
        s.menubar = tk.Menu(s.root)
        s.root.config(menu=s.menubar)

        #添加菜单选项
        s.menu1 = tk.Menu(s.menubar,borderwidth = 3,tearoff=False)
        s.menubar.add_cascade(label="选项", menu = s.menu1)

        s.menu1.add_command(label="撤销↶",command = lambda: s.Edit_about("back"))
        s.menu1.add_command(label="重做↷",command = lambda: s.Edit_about("callback"))
        s.menu1.add_command(label="清空",command = lambda: s.Edit_about("clear"))
        s.menu1.add_separator()
        s.menu1.add_command(label="历史",command = lambda: showHistroy)
        s.menu1.add_command(label="清空历史",command = lambda: clearHistory)
        s.menu1.add_separator()
        s.menu1.add_command(label="关于",command = showAbout)
        '''快捷键'''
        s.display()                    
        s.root.bind("<Control-Button-1>",lambda:s.buttonCaptureClick())
        s.root.bind("<Unmap>", lambda event: s.Hidden_window() if ((s.root.state() == 'iconic') and Shareble) else False) #窗口最小化判断，可以说是调用最重要的一步
        s.root.protocol('WM_DELETE_WINDOW', s.exit) #点击Tk窗口关闭时直接调用s.exit，不使用默认关闭
        
        s.root.mainloop()


if __name__ == '__main__':
    Main = _Main()
    Main.main()

    