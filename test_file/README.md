### Monkey Editor (Python 大作业)

#### 作者

吴栋、廖满文、汪潇翔、文一晴、吴雨暄、张维天

#### 项目简介

Python+PyQt5实现一个NotePad 文本编辑器，支持手写输入

#### 功能需求

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

#### 已知bug
* 潜在的内存泄漏
* 通过打开文件夹方式打开文件会导致跳转功能无法响应（响应慢），且鼠标右键的粘贴等功能也无法响应（响应慢）

#### 目录格式

```
.
├── README.md  // README
├── UI  // 存放Designer 生成的UI文件
│   ├── MainWindow.ui  // 主界面
│   └── Reward.ui  // 打赏界面
├── UI_forms  // 存放UI导出的py文件
│   ├── MainWindow.py
│   ├── Reward.py
│   ├── __init__.py  // 导入py文件里的类
├── imgs  // 存放图片
│   └── qrcode.PNG  // 打赏二维码
├── main.py  // 运行notepad的主程序
└── reward_handler.py  // 打赏函数
```









