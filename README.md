### Python 大作业

作者：吴栋、廖满文、汪潇翔、文一晴、吴雨暄、张维天

#### 项目简介

PyQt实现一个NotePad 文本编辑器，支持手写输入

#### 功能需求

- [x]   基础UI界面(lmw)
- [x]   基本功能，包括打开、关闭、新建、保存、复制粘贴等以及提示信息(lmw)
- [x]   支持同时打开多个窗口，并且能在窗口间进行切换(lmw)
- [x]   修改文件之后在Tab中文件名最后前显示'*'(lmw)
- [x]   支持编程语言选择及切换(lmw)
- [x]   添加偏好设置，支持设置字体大小、样式(lmw)
- [x]   在textEdit中查找关键词(wd)
- [x]   在QsciScintilla支持查找关键词(wd)
- [x]   打开文件夹，并在左侧显示文件夹目录树，点击文件可以打开浏览(wyx)
- [x]   支持关闭之后缓存上一次留下的tab(lmw)
- [x]   不同语言的代码高亮(支持不同语言的高亮规则)(zwt)
- [x]   不同语言的代码自动补全规则(wyq)
- [x]   显示代码行数(wyq)
- [ ]   支持调用命令行工具(wyx)
- [x]   支持编译、运行(wyx)
- [x]   Markdown语法渲染(zwt)
- [x]   Markdown分窗口渲染(zwt)
- [ ]   函数查找和跳转(zwt)
- [ ]   ~~像Typora那样进行Markdown语法实时渲染~~
- [x]   将模块集成到可以拉伸改变大小的窗口中(lmw)
- [x]   手写板插件，并通过手写板输入(wxx)
- [ ]   小键盘插件
- [x]   打赏界面(lmw)

#### 已知bug
* 潜在的内存泄漏
* 在IDE editor里面点击右键的事件可能不响应，且出现段错误
* 在当前目录保存文件后，文件夹内容不会更新

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







