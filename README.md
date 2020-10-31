### Python 大作业

作者：吴栋、廖满文、汪潇翔、文一晴、吴雨暄、张维天

#### 项目简介

PyQt实现一个NotePad 文本编辑器，支持手写输入

#### 功能需求

- [x]   基础UI界面
- [x]   基本功能，包括打开、关闭、新建、保存、复制粘贴等
- [x]   支持同时打开多个窗口，并且能在窗口间进行切换
- [x]   修改文件之后在Tab中文件名最后前显示'*'
- [x]   关闭文件若没有保存，提示是否保存
- [x]   支持编程语言选择及切换
- [ ]   查找关键词，定位上一个、下一个
- [x]   打开文件夹，并在左侧显示文件夹目录树，点击文件可以打开浏览
- [ ]   支持关闭之后缓存上一次留下的tab
- [ ]   添加偏好设置
- [ ]   代码高亮、自动补全
- [ ]   显示代码行数
- [ ]   支持调用命令行工具
- [ ]   支持编译、运行（调用命令行进行）
- [ ]   Markdown语法渲染
- [ ]   像Typora那样进行Markdown语法实时渲染
- [ ]   手写板插件，并通过手写板输入
- [ ]   小键盘插件
- [x]   打赏

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






