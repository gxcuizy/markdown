---
title: Python如何生成windows可执行的exe文件
date: 2018-08-21 10:11:17
tags: [Python, pyinstaller]
---

### 为什么要生成可执行文件

- 不需要安装对应的编程环境
- 可以将你的应用闭源
- 用户可以方便、快捷的直接使用

### 打包工具
- pyinstaller

#### 安装pyinstaller

如果你的网络稳定，通常直接使用下面的命令安装即可：
```
pip install pyinstaller
```

当然了，你也可以下载pyinstaller源码包，然后进入包目录执行下面的命令，同样可以安装（前提是需要安装setuptools）：
```
python setup.py install
```
安装过程如下图所示  
![pyinstaller安装][pyinstaller_install]

#### 检查pyinstaller安装成功与否：

只需要执行如下命令其中一个即可：

```
pyinstaller --version
pyinstaller -v
```

如果出现如下界面，就说明是安装成功了

![pyinstaller安装结果][pyinstaller_result]

### pyinstaller参数作用

- \-F 表示生成单个可执行文件
- \-D  –onedir 创建一个目录，包含exe文件，但会依赖很多文件（默认选项）
- \-w 表示去掉控制台窗口，这在GUI界面时非常有用。不过如果是命令行程序的话那就把这个选项删除吧
- \-c  –console, –nowindowed 使用控制台，无界面(默认)
- \-p 表示你自己自定义需要加载的类路径，一般情况下用不到
- \-i 表示可执行文件的图标
- 其他参数，可以通过`pyinstaller --help`查看

### 开始打包

进入python需要打包的脚本所在目录，然后执行下面的命令即可：

```
python -F -i favicon.ico nhdz.py
```

执行过程如下图所示：

![pyinstaller执行过程][pyinstaller_excute]

### 打包结果

打包完成后，进入到当前目录下，会发现多了\_\_pycache\_\_、build、dist、nhdz.spec这四个文件夹或者文件，其中打包好的exe应用在dist目录下面，进入即可看到，可以把他拷贝到其他地方直接使用，如下图所示，是打包完成后的目录：

![pyinstaller打包结果][exe_file]

### 执行exe应用

因为是exe应用，是可执行文件了，所以直接双击运行即可，运行效果如下图所示：

![pyinstaller运行结果][nhdz_exe_download]

到这里，exe文件就已经生算是打包完成，并且可以运行了，如果你想在其他平台运行，只需要拷贝dist下面的文件即可

### ICO图标制作

前面需要用到ICO图标，大家可以网上搜索“ICO 在线生成”，可以直接点击[ICO图标制作][duduxuexi_url]在上面制作、然后保存也行

### 最后

大家有什么疑问或者想法，都可以直接和我交流，谢谢！

[pyinstaller_result]: /images/pyinstaller_result.png
[pyinstaller_install]: /images/pyinstaller_install.png
[pyinstaller_excute]: /images/pyinstaller_excute.png
[exe_file]: /images/exe_file.png
[nhdz_exe_download]: /images/nhdz_exe_download.png
[duduxuexi_url]: http://ico.duduxuexi.com/