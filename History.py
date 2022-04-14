import os


class history:

    def __init__(self, filepath, filename,tk_window):
        '''
        filepath     历史信息路径
        hover_text   鼠标停留在图标上方时显示的文字
        menu_options 右键菜单，格式: (('a', None, callback), ('b', None, (('b1', None, callback),)))
        tk_window    传递Tk窗口，s.root，用于单击图标显示窗口
        '''

        self.path = filepath
        self.name = filename

    def save_Transrecord(self):
        
        