## Monkey Editor (Python 大作业)


制作：猴子工作室

成员名单：
吴栋、廖满文、汪潇翔、文一晴、吴雨暄、张维天

### 项目简介

Python+PyQt5实现的一个文本编辑器，支持手写输入

本项目现放在https://github.com/EXPmaster/notepad, 
后续可能会时不时地进行维护

### Installation
1. 新建Anaconda虚拟环境

   ```shell script
   conda create -n snake python=3.7 -y
   ```
   
2. 激活环境

   ```shell script
   conda activate snake
   ```

3. 安装pytorch, torchvision

   ```shell script
   conda install pytorch torchvision -c pytorch
   ```
   
   若安装太慢，可以尝试使用清华源镜像安装
   ```shell script
   conda install pytorch torchvision --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
   ```

4. 安装依赖包

   ```shell script
   pip install -r requirements.txt
   ```

5. 运行

   ```shell script
   python main.py
   ```

### 功能需求

- [x]   基础UI界面(lmw)

- [x]	程序启动界面(wyq)
- [x]   基本功能，包括打开、关闭、新建、保存、复制粘贴、提示信息以及快捷键(lmw)
- [x]   支持同时打开多个窗口，并且能在窗口间进行切换(lmw)
- [x]   修改文件之后在Tab中文件名最后前显示'*'(lmw)
- [x]   支持编程语言选择及切换(lmw)
- [x]   添加偏好设置，支持设置字体大小、样式(lmw)
- [x]   在textEdit中查找、计数、替换、标记、清除关键词(wd)
- [x]   在QsciScintilla支持查找、计数、替换、关键词(wd)
- [x]   打开文件夹，并在左侧显示文件夹目录树，点击文件可以打开浏览(wyx)
- [x]   支持关闭之后缓存上一次留下的tab(lmw)
- [x]   缓存偏好设置(lmw)
- [x]   不同语言的代码高亮(支持不同语言的高亮规则)(zwt)
- [x]   不同语言的代码自动补全规则(wyq)
- [x]   显示代码行数(wyq)
- [x]   支持调出命令行（终端）(wyx)
- [x]   支持点击按钮进行编译、运行(wyx)
- [x]   Markdown语法渲染(zwt)
- [x]   Markdown分窗口渲染(zwt)
- [x]   使用AST实现跳转(lmw)
- [x]   函数查找和跳转(zwt)
- [ ]   ~~像Typora那样进行Markdown语法实时渲染~~
- [x]   将模块集成到可以拉伸改变大小的窗口中(lmw)
- [x]   训练编写SOTA模型实现手写汉字识别，能识别常见字体(wd)
- [x]   为手写汉字识别提供web demo
- [x]   嵌入手写板插件，并通过手写板输入(wxx)

- [x]	程序运行logo(wxx)
- [ ]   ~~小键盘插件~~
- [x]   打赏界面(lmw)
- [x]   启动界面(wyq)

#### 已知bug
* 潜在的内存泄漏
* 通过打开文件夹方式打开文件会导致跳转功能无法响应（响应慢），且鼠标右键的粘贴等功能也无法响应（响应慢）

#### 目录格式

```
.
├── AST.py
├── LICENSE
├── README.md
├── RunWindow
│   ├── __init__.py
│   └── run_window.py
├── SplashCall.py
├── UI
│   ├── Find.ui
│   ├── MainWindow.ui
│   ├── Preference.ui
│   ├── Reward.ui
│   └── ui_Splash.ui
├── UI_forms
│   ├── Find.py
│   ├── MainWindow.py
│   ├── Reward.py
│   ├── __init__.py
│   └── ui_Splash.py
├── all_windows
│   ├── Find_win.py
│   ├── Find_win_ide.py
│   └── __init__.py
├── config.ini
├── hd_board
│   ├── PaintBoard.py
│   ├── __init__.py
│   ├── board.py
│   ├── model_best.pth.tar
│   ├── nets.py
│   ├── new_char_dict.txt
│   ├── paint.ui
│   ├── temp.png
│   ├── test_img
│   │   ├── 1.png
│   │   └── 2.png
│   ├── train.py
│   ├── ui_paint.py
│   └── utils.py
├── ide_edit.py
├── image.py
├── imgs
│   ├── image.qrc
│   ├── qrcode.PNG
│   ├── run.jpg
│   └── test.png
├── main.py
├── preference.py
├── requirements.txt
├── reward_handler.py
├── style.qss
├── temp.png
└── textedit.py

```









