from cProfile import label
import datetime
from distutils.log import debug
import logging
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import BOTH, E, END, INSERT, LEFT, N, TOP, W, X, YES

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program')
HistoryList = []
MAX_HISTORY = 50
PATH = ['res','history']

WinWidth = 220
WinHeight = 400
LabelList = []

class history:

    def __init__(self, filepath, filename,tk_window = None):
        '''
        filepath     历史信息路径
        hover_text   鼠标停留在图标上方时显示的文字
        menu_options 右键菜单，格式: (('a', None, callback), ('b', None, (('b1', None, callback),)))
        tk_window    传递Tk窗口，s.root，用于单击图标显示窗口
        '''

        self.path = filepath
        self.name = filename
        self.time = ''
        if(tk_window != None):
            self.root = tk_window
        else:
            self.root = tk.Tk() 
        #self.CreatHistory()

    def CreatHistory(self):
        """创建顶层窗口"""
        self.window = tk.Toplevel(self.root, width=WinWidth, height=WinHeight)
        #take a name for this windows
        self.window.title("历史记录")
        #set window size for GUI
        self.window.geometry(str(WinWidth)+"x"+str(WinHeight))
        self.window.resizable(False, False)
        #创建画布
        self.canvas= tk.Canvas( self.window,width = WinWidth,height=WinHeight, scrollregion=(0,0,WinWidth,WinHeight),bg="white") #

        self.fm1 = tk.Frame(self.canvas)
        self.fm2 = ttk.Frame(self.window,height=80)
        #竖直滚动条
        self.vbar=tk.Scrollbar(self.canvas,
                  orient=tk.VERTICAL,
                  command=self.canvas.yview,
                  width=5) 
        self.canvas.config(yscrollcommand= self.vbar.set,selectforeground="white")
        self.canvas.place(x = 0, y = 0,width=WinWidth,height=WinHeight) #放置canvas的位置  
        self.vbar.place(x = 215,y=0,width=5,height=440)
        self.canvas.create_window(((0,0)), window=self.fm1,anchor='nw')  #create_window       

        self.btnSet = tk.Button(self.fm2,
                        text='增加',
                        command=self.labelSetClick)
        self.btnClear = tk.Button(self.fm2,
                          text='清空按钮',
                          command=self.labelClearClick)

        #两按键，用于调试  实际应用可注释 fm2，并将command函数重写
        self.btnSet.pack(side=LEFT,anchor=W,fill=X,expand=YES)
        self.btnClear.pack(side=LEFT,anchor=W,fill=X,expand=YES) 

        #创建菜单
        self.menu = tk.Menu(self.root,
            tearoff=False,
            #bg="grey",
            )
        self.menu.add_command(label="置顶", command=self.ListItem_about("top"))
        self.menu.add_command(label="删除", command=self.ListItem_about("del"))
        
        self.fm1.bind("<Configure>",self.updateCanvas)
        self.canvas.bind_all("<MouseWheel>",self.WheelCtrl)
        self.fm2.pack(side=tk.BOTTOM, fill=X, expand=N)
        self.window.mainloop()

    def getTime(self):
        """更新当前时间"""
        self.time = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')

    def WheelCtrl(self,event):
        """滚轮事件，绑定画布'"""
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
        """
        for label in LabelList:
            label.destroy()
        LabelList = []
        """
        self.DeleteHistory(Index=2)
        if(self.IsEmpty()):
             self.btnClear['state'] = 'disabled'
        self.btnSet['state'] = 'normal'
   
    def AddHistory(self,_EditIndex,text):
        """创建的组件"""
        self.getTime()
        self.place(self.time,text)
    
    def place(self,time,text):
        """在fm1中动态创建Text组件,time当前时间,text"""
        i = len(LabelList)
        exec('label'+str(i)+'=tk.Text(self.fm1,bg = "LightYellow",highlightcolor = "Orange",padx = 5,pady = 5,undo = True, height=4,font=("微软雅黑",9))')
        eval('label'+str(i)).insert(INSERT,time+'\n'+text)
        eval('label'+str(i)).pack(side=TOP,anchor="w",fill=X,expand=N)
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
        """清除所有历史记录"""
        for label in LabelList:
            label.destroy()
        LabelList = []

    def IsEmpty(self):
        """清除所有历史记录"""
        if(len(LabelList)):
            return False
        return True
    #def SelectHistroy(self):
        """鼠标左键点击历史元素返回内容"""

if __name__ == '__main__':
    mypath = os.path.join(os.sep,*PATH)
    logging.debug(mypath)
    myhistory = history(mypath,"history.txt")
    myhistory.CreatHistory()

        