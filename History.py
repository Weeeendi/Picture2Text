import datetime
import logging
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import BOTH, E, END, INSERT, LEFT, N, TOP, W, X, YES
import json
import pyperclip

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program')
HistoryList = []
MAX_HISTORY = 50
PATH = ['res','history']
File = '/history.json'

WinWidth = 220
WinHeight = 400
LabelList = []

selectEditCont = ''

class RecordHty():
    """存储历史数据"""
    def __init__(self,file) -> None:
        self.file = file
        self.dict = {}
        self.LoadRec()

    def SaveRec(self):
        if(self.file == None):
            logging.debug("Have not this file")
            return
        tf = open(self.file,"w")
        json.dump(self.dict,tf)
        tf.close()

    def LoadRec(self):
        try:
            tf = open(self.file, "r")
        except Exception as e:
            logging.debug(e)
            #如不存在则创建该文件
            tf = open(self.file, "w")
            tf.close()
            return
        try:
            self.dict = json.load(tf)
            keys = list(self.dict.keys())
            print(keys)
        except Exception as e:
            logging.debug(e)
            pass
        tf.close()


class ToolTip(object):

    def __init__(self,rootwidget,widget):
        self.widget = widget
        self.rootwidget = rootwidget

    def hovershow(self):    
        self.widget.config(bg = "#FFFFDA",cursor = "heart")

    def hoverhide(self):
        self.widget.config(bg = "#ffffff",cursor = "arrow") 

    def Leftclick(self):
        text = self.widget.get(1.0,END)
        pyperclip.copy(text[21:])
        self.rootwidget.destroy()


def CreateToolTip(rootwidget,widget):
        toolTip = ToolTip(rootwidget,widget)
        def enter(event):
            toolTip.hovershow()
        def leave(event):
            toolTip.hoverhide()
        def click(event):
            toolTip.Leftclick()
       
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)
        widget.bind('<Button-1>',click)



class history:

    def __init__(self,fileObj,tk_window = None):
        '''
        fileObj      历史文件存储结构体 RecordHty类
        hover_text   鼠标停留在图标上方时显示的文字
        menu_options 右键菜单，格式: (('a', None, callback), ('b', None, (('b1', None, callback),)))
        tk_window    传递Tk窗口，s.root，用于单击图标显示窗口
        '''
        self.fileObj = fileObj
        self.root = tk_window
      
        #self.CreatHistory()

    def CreatHistory(self):
        """创建顶层窗口"""
        if(self.root == None):
            self.window = tk.Tk() 
        else:
            self.window = tk.Toplevel(self.root, width=WinWidth, height=WinHeight)
        
        #take a name for this windows
        self.window.title("历史记录")
        #set window size for GUI
        self.window.geometry(str(WinWidth)+"x"+str(WinHeight))
        self.window.resizable(False, False)
        self.window.attributes('-alpha',0.9)
        #想要实现透明标题栏，但是失败了
        #self.window.overrideredirect(True)
        
        #创建画布
        self.canvas= tk.Canvas(self.window,width = WinWidth,height=WinHeight, scrollregion=(0,0,WinWidth,WinHeight)) #

        self.fm1 = tk.Frame(self.canvas)
        self.fm2 = ttk.Frame(self.window,height=80)

      
        pad = 0 #想要实现透明标题栏，但是失败了
        #竖直滚动条
        self.vbar=tk.Scrollbar(self.canvas,
                  orient=tk.VERTICAL,
                  command=self.canvas.yview,
                  width=5) 
        self.canvas.config(yscrollcommand= self.vbar.set,bg="white",selectforeground="white",highlightthickness = 1,insertborderwidth = 3)
        self.canvas.place(x = 0, y = 0,width=WinWidth-pad,height=WinHeight-pad) #放置canvas的位置  
        self.vbar.place(x = 215,y=0,width=5,height=WinHeight-pad)
        self.canvas.create_window(((0,0)), window=self.fm1,anchor='nw')  #create_window       
       
        self.btnSet = ttk.Button(self.fm2,
                        text='增加',
                        command=self.labelSetClick)
        self.btnClear = ttk.Button(self.fm2,
                          text='清空按钮',
                          command=self.labelClearClick)
        self.Tip = ttk.Label(self.fm2,text="点击历史，复制文本到剪贴板 ctrl+v 黏贴",wraplength = 150,font=("微软雅黑",8))

        #创建标题栏,想要实现透明标题栏，但是失败了
        #self.Lab = ttk.Label(self.window, text='历史记录', font=('Microsoft Yahei', 14))
        #self.Lab.pack(side=TOP,anchor=W,fill=X,expand=N)

        #两按键，用于调试  实际应用可注释 fm2，并将command函数重写
        #self.btnSet.pack(side=LEFT,anchor=W,fill=X,expand=YES)
        #self.btnClear.pack(side=LEFT,anchor=W,fill=X,expand=YES) 
        self.Tip.pack(side=TOP,anchor=W,fill=X,expand=YES) 
        #创建菜单
        self.menu = tk.Menu(self.window,
            tearoff=False,
            #bg="grey",
            )
        self.menu.add_command(label="置顶", command=self.ListItem_about("top"))
        self.menu.add_command(label="删除", command=self.ListItem_about("del"))
        
        self.fm1.bind("<Configure>",self.updateCanvas)
        self.canvas.bind_all("<MouseWheel>",self.WheelCtrl)
        self.fm2.pack(side=tk.BOTTOM, fill=X, expand=N)

        #失焦后退出
        def out(event):
            self.window.destroy()
        self.window.bind("<FocusOut>",out)

        #遍历历史记录
        
        for k,v in self.fileObj.dict.items():
            self.AddHistory(k,v)
        if(self.IsEmpty()):
            self.EmptyLabel = ttk.Label(self.fm1,text="空",wraplength = 150,font=("微软雅黑",12)).pack(anchor=W,fill=BOTH,expand=YES)

        #获取焦点
        self.window.focus_set()
        self.window.mainloop()

    def ClickItem(event,self):
        """点击后退出历史窗口并返回元素结果"""
        global selectEditCont
        return selectEditCont

    def getTime(self):
        """更新当前时间"""
        self.time = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')

    def WheelCtrl(self,event):
        """滚轮事件，绑定画布'"""
        self.fm2.forget()
        if((len(LabelList)*80)>WinHeight):
            self.canvas.yview_scroll(int(-1*(event.delta/120)),"units") 
    
    def ListItem_about(self,cmd):
        """弹窗操作 置顶:'top',删除：'del'"""

    def updateCanvas(self,event):
        """铺满当前画布 少了这个就滚动不了"""
        if((len(LabelList)*80)>WinHeight):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=200,height=200)
        pass
        
    def labelSetClick(self):
        """动态增加的组件"""
        self.getTime()
        self.place(self.time,"你今天真好看")
        # 根据需要禁用和启用“增加按钮”和“清空按钮”
        if(len(LabelList)!=0):
           self.btnClear['state'] = 'normal' 

    # 删除动态创建的组件
    def labelClearClick(self):
        """删除动态创建的组件"""
        global LabelList
        
        for label in LabelList:
            label.destroy()
        LabelList = []   
        #self.DeleteHistory(Index=2)
        if(self.IsEmpty()):
             self.btnClear['state'] = 'disabled'
        self.btnSet['state'] = 'normal'
   
    def AddHistory(self,time,text):
        """创建的组件"""
        #self.getTime()
        self.place(time,text)
    
    def place(self,time,text):
        """在fm1中动态创建Text组件,time当前时间,text"""
        i = len(LabelList)

        exec('label'+str(i)+'=tk.Text(self.fm1,bg = "#FFFFF0",highlightcolor = "#696969",highlightthickness = 1,undo = True, height=4,font=("微软雅黑",8))')
        eval('label'+str(i)).tag_config('tag',foreground='DimGray',font =("微软雅黑",7) ) #设置tag即插入文字的大小,颜色等
        eval('label'+str(i)).insert(1.0,text)
        eval('label'+str(i)).insert(0.0,time+'\n\n','tag')
        eval('label'+str(i)).pack(side=TOP,anchor="w",fill=X,expand=N,pady = 2)
        eval('label'+str(i))['state'] = 'disabled'
        self.SelectHistroy(eval('label'+str(i)))
        CreateToolTip(self.window,eval('label'+str(i)))
        LabelList.append(eval('label'+str(i)))
        if(i*80 > WinHeight):  
            self.fm1.config(height=(i)*80+400)
        else:
            self.fm1.config(height=400)

    def DeleteHistory(self,Index = None):
        """在fm1中动态删除Text组件,Index:删除指定下标  默认删除列表尾节点"""
        if(Index == None):
            LabelList.pop().destroy()
        else:
            LabelList[Index].destroy()
            del LabelList[Index]
        
    def DeleteAll(self):
        """清除所有历史记录(面板) -- 仅用于测试历史窗口显示配合按键labelClearClick"""
        for label in LabelList:
            label.destroy()
        LabelList = []
        self.fileObj.dict = {}

    def DelAllData(self):
        """清除所有历史记录(文件)"""
        self.fileObj.dict = {}
        self.fileObj.SaveRec()

    def IsEmpty(self):
        """判空"""
        if(len(LabelList)):
            return False
        return True

    def SelectHistroy(self,widget = None):
        """鼠标左键点击历史元素返回内容"""
        if(widget): 
            return
        text = widget.get("0,0",END)
        self.window.destroy()
        return text

    def RightSelectHistory(self,widget):
        """鼠标右键点击历史记录 弹出两种操作 置顶、删除"""
        index = LabelList.index(widget)
        widget.get("0,0",END)
        #label.pack(ipadx=1)

if __name__ == '__main__':
    path = os.path.join(os.extsep,*PATH)
    HistoryFile = RecordHty(path+File)
    myhistory = history(HistoryFile)
    myhistory.CreatHistory()

        