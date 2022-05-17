# 软件功能
  1. 截图或打开图片识别图像上的文字
  2. 显示识别文字，翻译成其他语言
  3. 访问识别历史记录

# 软件架构
  gui.py-----------------------thinker框架的gui主界面
  History.py------------------用于toplevel的历史记录浮窗显示和历史记录存取实现
  ImgTranText.py-----------基于百度Api，实现图文转换
  minIcon.py----------------  用于实现串口最小化到托盘


## 主要类及其函数一览

### gui.py
```python
class _Main:  #Mian window class
      def main(s):
        """初始化窗口"""
      def buttonCaptureClick(s):
        """桌面截图函数"""
      def display(s):
        """显示布局"""
```

2022.05.17 wendi last edit
