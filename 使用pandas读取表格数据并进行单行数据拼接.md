---
title: 使用pandas读取表格数据并进行单行数据拼接
date: 2021-03-02 13:18:36
tags: [Python, pandas, 文本拼接]
---

![](https://image-static.segmentfault.com/220/090/2200901345-603dd975d6797_articlex)

### 业务需求

一个几十万条数据的Excel表格，现在需要拼接其中某一列的全部数据为一个字符串，例如下面简短的几行表格数据：

| id | code | price | num |
| --- | --- | --- | --- |
| 11 | 22 | 33 | 44 |
| 22 | 33 | 44 | 55 |
| 33 | 44 | 55 | 66 |
| 44 | 55 | 66 | 77 |
| 55 | 66 | 77 | 88 |
| 66 | 77 | 88 | 99 |

现在需要将`code`的这一列用逗号`,`拼接为字符串，并且每个单元格数据都用单引号包含，需要拼接成字符串`'22','33','44','55','66','77'`，这样的情况，我们需要怎么处理呢？当然方式有很多……

### 多行文本批量处理

有的时候，我们会遇到需要同时处理多行文本的情况，很多文本编辑器都支持批量操作多行文本，这里我主要说一下`Sublime Text`，下面是操作的快捷键，有需要的可以尝试用一下，确实挺方便的。

1. 选中需要操作的多行，按下`Ctr+Shift+L`即可同时编辑这些行
2. 鼠标选中文本，反复按`CTRL+D`即可继续向下同时选中下一个相同的文本进行同时编辑
3. 鼠标选中文本，按下`Alt+F3`即可一次性选择全部的相同文本进行同时编辑

### 如何节省效率

在工作中，可能会存在一些表格数据处理的情况，比如运营给你一个表格，表格里有类似：订单号呀、产品ID啊、商品SKU等，需要你协助导出这些数据里的明细数据以便他们做分析用，一两次，我们可以快速用上面的方式处理，但是这种方式对于大文本的处理可能会存在卡顿的情况，操作效率较低，如果小文本的话，那么还是很方便的。

如果多次遇到这种情况，是否想要做成一个工具来快速处理呢，也就是，这种批量拼接同样格式的数据，我们可以写一个小工具来实现，即快速又省事，可以大大减少重复的工作消耗。

### pandas读取表格数据并处理

这我们使用`Python`的`pandas`模块来读取表格指定某列的数据，再按照我们的拼接格式进行循环处理，最终把拼接的字符串写入文本文件中，方便保留和使用拼接的数据。

```
sheet = pandas.read_excel(io=file_name, usecols=[line_num])
data = sheet.values.tolist()
str_data = ''
# 循环处理数据
print_msg('已获取列数据条数[' + str(len(data)) + ']，开始处理数据……')
for x in range(len(data)):
    if str(data[x][0]) != 'nan':
        str_data += "'" + str(data[x][0]) + "',"
```

### 完整源码

因为脚本需要多次使用，并且针对不同文件的不同列，所以，我们采用接受关键参数的形式，可以不改动任何代码，就可以直接使用此脚本来完整我们的数据拼接，同时，我们还可以使用`pyinstaller`模块来将脚本进行打包成`exe`的window可执行文件，使其在无`Python`的运行环境中也可以使用，打包命令为：`pyinstaller -F -i favicon.ico join_excel_data.py`，我已有打包的上传到交友网站`Github`上，大家有兴趣的话，可以点击查看哦，交个朋友地址：[https://github.com/gxcuizy](https://github.com/gxcuizy/Python/tree/master/%E6%8B%BC%E6%8E%A5%E8%A1%A8%E6%A0%BC%E5%8D%95%E8%A1%8C%E6%95%B0%E6%8D%AE%E4%B8%BA%E5%AD%97%E7%AC%A6%E4%B8%B2)

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
拼接Excel表格单行数据，并写入文本
author: gxcuizy
time: 2021-03-01
"""

import pandas
import random
import os
import time


def print_msg(msg=''):
    """打印信息"""
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print('[' + now_time + '] ' + msg)


# 程序主入口
if __name__ == "__main__":
    # 获取传入参数
    file_name = input('请输入当前目录下的表格文件名（例如“01.xlsx”）：')
    line_num = input('请输入要拼装的数据第几列（例如“1”）：')
    # 判断文件是否存在
    if os.path.exists(file_name) == False:
        print_msg('文件不存在')
        os.system("pause")
        exit(0)
    # 判断输入的行数是否为数字
    if line_num.isdigit() == False:
        print_msg('请输入列数的数字')
        os.system("pause")
        exit(0)
    try:
        # 获取表格数据
        print_msg('开始获取文件[' + file_name + ']的第[' + str(line_num) + ']列数据')
        line_num = int(line_num) - 1
        sheet = pandas.read_excel(io=file_name, usecols=[line_num])
        data = sheet.values.tolist()
        str_data = ''
        # 循环处理数据
        print_msg('已获取列数据条数[' + str(len(data)) + ']，开始处理数据……')
        for x in range(len(data)):
            if str(data[x][0]) != 'nan':
                str_data += "'" + str(data[x][0]) + "',"
        # 写入文本文件
        print_msg('数据处理完毕，开始写入……')
        random_num = random.randint(1000, 9999)
        with open('str_' + str(random_num) + '.txt', 'w') as f:
            f.write(str_data.strip(','))
        print_msg('数据写入完毕.')
    except Exception as err_info:
        # 异常信息
        print_msg(str(err_info))
    # 防止exe程序执行结束闪退
    os.system("pause")

```

### 最后

如果大家有其他好玩的、好用的欢迎分享出来，大家一起学习和交流。对了，如果有说的不对的或者错误的地方，请大家指出来，我会加倍学习，力争改进，期望和大家一起进步，谢谢。