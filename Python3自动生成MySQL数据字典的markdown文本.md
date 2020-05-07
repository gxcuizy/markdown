---
title: Python3自动生成MySQL数据字典的markdown文本
date: 2020-05-06 15:09:16
tags: [MySQL, 数据库, markdown, 工具]
---

![](https://image-static.segmentfault.com/200/857/200857007-5eb233d633819_articlex)

### 为啥要写这个脚本

五一前的准备下班的时候，看到同事为了做数据库的某个表的数据字典，在做一个复杂的人工操作，就是一个字段一个字段的纯手撸，那速度可想而知是多么的折磨和锻炼人的意志和耐心，反正就是很耗时又费力的活，关键是工作效率太低了，于是就网上查了一下，能否有在线工具可用，但是并没有找到理想和如意的，于是吧，就干脆自己撸一个，一劳永逸，说干就干的那种……

<!--more-->

### 先屡一下脚本思路

第一步：输入或修改数据库连接配置信息，以及输入数据表名

第二步：利用pymysql模块连接数据库，并判断数据表是否存在

第三步：获取数据表的注释

第四步：存储文件夹和文件处理，删除已存在的文件避免重复写入

第五步：先写入Markdown的表头部信息

第六步：从information_schema中查询表结构和相关信息

第七步：依次拼装每个字段的Markdown文本写入，结束并关闭相关连接

### 运行环境

Python运行环境：Windows + python3.6  
用到的模块：`pymysql、os、time、pyinstaller`  
如未安装的模块，请使用`pip instatll xxxxxx`进行安装，例如：`pip install pyinstaller`

### 获取数据库连接信息的两种方式

既然是要做数据字典，那么肯定就需要先连接数据库，而连接数据库，自然就需要先知道数据库的基本信息：IP地址、用户名、登录密码、数据库名等……

为了方便，我这里写了两种配置MySQL连接的方法：第一种是直接配置在代码里，直接修改代码里的连接信息就可以了；另外一种就是通过手动输入链接信息，不用修改代码，方便快速多用。具体的完整源码，我都上传到同性交友网站[GitHub](https://github.com/gxcuizy/Python/tree/master/%E8%87%AA%E5%8A%A8%E7%94%9F%E6%88%90%E6%95%B0%E6%8D%AE%E5%BA%93%E8%A1%A8%E5%AD%97%E5%85%B8%E7%9A%84markdown%E6%96%87%E6%9C%AC)了，可以点下面的链接查看……

- 修改代码的完整源码：[data_dict_config.py](https://github.com/gxcuizy/Python/blob/master/%E8%87%AA%E5%8A%A8%E7%94%9F%E6%88%90%E6%95%B0%E6%8D%AE%E5%BA%93%E8%A1%A8%E5%AD%97%E5%85%B8%E7%9A%84markdown%E6%96%87%E6%9C%AC/data_dict_config.py)
- 手动输入的完整源码：[data_dict_input.py](https://github.com/gxcuizy/Python/blob/master/%E8%87%AA%E5%8A%A8%E7%94%9F%E6%88%90%E6%95%B0%E6%8D%AE%E5%BA%93%E8%A1%A8%E5%AD%97%E5%85%B8%E7%9A%84markdown%E6%96%87%E6%9C%AC/data_dict_input.py)

### 执行效果图

执行**data_dict_config.py**脚本的时候，交互效果如下

![](https://image-static.segmentfault.com/248/369/2483698320-5eb3674e73ae9_articlex)

执行**data_dict_input.py**脚本的时候，交互效果如下

![](https://image-static.segmentfault.com/546/830/546830567-5eb36718e03d5_articlex)

执行完脚本后，会在当前目录下，生成一个`mysql_dict`文件夹，打开文件夹，里面的`.md`格式的文件就是每个表的`markdown`文本的表格写法，拷贝里面的文本到任何支持`mardkwon`地方就可以使用和查看，例如我放到有道云笔记上，部分效果如下

![](https://image-static.segmentfault.com/298/884/2988844002-5eb367ebd5f05_articlex)

### 生成可执行文件

为了方便不同的人群方便快速的使用，可以不用安装Python环境来执行py脚本文件，我把相关脚本打包成Windows可直接执行的exe文件，下载双击运行即可（可能有的系统需要管理员权限运行），打包的方式很简单，就是利用`pyinstaller`模块进行快速打包，省时省力，具体更多用法大家可以网上查一下。

打包命令为：` pyinstaller -F -i favicon.ico data_dict_input.py`

执行这个命令后，就会在当前目录下生成一个`dict`和其他的文件夹和相关文件，其中，打开`dict`，下面会生成一个文件名相同的exe文件`data_dict_input.exe`，双击这个文件就可以打开了，拷贝到其他地方一样可以使用。

下面我把两种方式的脚本，都生成了exe可执行文件，大家可以直接点击下载试用，如果下载不了，请直接去[GitHub仓库](https://github.com/gxcuizy/Python/tree/master/%E8%87%AA%E5%8A%A8%E7%94%9F%E6%88%90%E6%95%B0%E6%8D%AE%E5%BA%93%E8%A1%A8%E5%AD%97%E5%85%B8%E7%9A%84markdown%E6%96%87%E6%9C%AC)下载或者自己生成

- 修改代码的可执行文件：[data_dict_config.exe](https://raw.githubusercontent.com/gxcuizy/Python/master/%E8%87%AA%E5%8A%A8%E7%94%9F%E6%88%90%E6%95%B0%E6%8D%AE%E5%BA%93%E8%A1%A8%E5%AD%97%E5%85%B8%E7%9A%84markdown%E6%96%87%E6%9C%AC/data_dict_config.exe)

- 手动输入的可执行文件：[data_dict_input.exe](https://raw.githubusercontent.com/gxcuizy/Python/master/%E8%87%AA%E5%8A%A8%E7%94%9F%E6%88%90%E6%95%B0%E6%8D%AE%E5%BA%93%E8%A1%A8%E5%AD%97%E5%85%B8%E7%9A%84markdown%E6%96%87%E6%9C%AC/data_dict_input.exe)

### 完整代码

为了方便部分人想偷懒，不直接去交友网站查看，我在这里也贴一下其中的一个源码出来吧（其实吧，我是觉得文章篇幅有点短，来凑字数的，大家明白就好，看透不说透）。

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
自动生成MySQL数据表的数据字典支持多个
自动获取数据库连接信息，方便多用
author: gxcuizy
date: 2020-04-30
"""

import pymysql
import os
import time


class DataDict(object):
    def __init__(self, connect_info):
        # 数据库连接配置
        self.host_name = connect_info[0]
        self.user_name = connect_info[1]
        self.pwd = connect_info[2]
        self.db_name = connect_info[3]
        self.folder_name = 'mysql_dict'

    def run(self, table_str):
        """脚本执行入口"""
        try:
            # 创建一个连接
            conn = pymysql.connect(self.host_name, self.user_name, self.pwd, self.db_name)
            # 用cursor()创建一个游标对象
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        except Exception:
            print('数据库连接失败，请检查连接信息！')
            exit(1)
        table_list = table_str.split(',')
        for table_name in table_list:
            # 判断表是否存在
            sql = "SHOW TABLES LIKE '%s'" % (table_name,)
            cursor.execute(sql)
            result_count = cursor.rowcount
            if result_count == 0:
                print('%s数据库中%s表名不存在，无法生成……' % (self.db_name, table_name))
                continue
            # 表注释获取
            print('开始生成表%s的数据字典' % (table_name,))
            sql = "show table status WHERE Name = '%s'" % (table_name,)
            cursor.execute(sql)
            result = cursor.fetchone()
            table_comment = result['Comment']
            # 文件夹和文件处理
            file_path = self.folder_name + os.sep + table_name + '.md'
            self.deal_file(file_path)
            # 打开文件，准备写入
            dict_file = open(file_path, 'a', encoding='UTF-8')
            dict_file.write('#### %s %s' % (table_name, table_comment))
            dict_file.write('\n | 字段名称 | 字段类型 | 默认值 | 字段注释 |')
            dict_file.write('\n | --- | --- | --- | --- |')
            # 表结构查询
            field_str = "COLUMN_NAME,COLUMN_TYPE,COLUMN_DEFAULT,COLUMN_COMMENT"
            sql = "select %s from information_schema.COLUMNS where table_schema='%s' and table_name='%s'" % (field_str, self.db_name, table_name)
            cursor.execute(sql)
            fields = cursor.fetchall()
            for field in fields:
                column_name = field['COLUMN_NAME']
                column_type = field['COLUMN_TYPE']
                column_default = str(field['COLUMN_DEFAULT'])
                column_comment = field['COLUMN_COMMENT']
                info = ' | ' + column_name + ' | ' + column_type + ' | ' + column_default + ' | ' + column_comment + ' | '
                dict_file.write('\n ' + info)
            # 关闭连接
            print('完成表%s的数据字典' % (table_name,))
            dict_file.close()
        cursor.close()
        conn.close()

    def deal_file(self, file_name):
        """处理存储文件夹和文件"""
        # 不存在则创建文件夹
        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)
        # 删除已存在的文件
        if os.path.isfile(file_name):
            os.unlink(file_name)

    def test_conn(self, conn_info):
        """测试数据库连接"""
        try:
            # 创建一个连接
            pymysql.connect(conn_info[0], conn_info[1], conn_info[2], conn_info[3])
            return True
        except Exception:
            return False


# 程序执行入口
if __name__ == '__main__':
    # 数据数据连接信息
    conn_info = input('请输入mysql数据库连接信息(格式为：主机IP,用户名,登录密码,数据库名)，逗号分隔且输入顺序不能乱，例如：192.168.0.1,root,root,test_db：')
    conn_list = conn_info.split(',')
    while conn_info == '' or len(conn_list) != 4:
        conn_info = input('请正确输入mysql数据库连接信息(格式为：主机IP,用户名,登录密码,数据库名)，逗号分隔且输入顺序不能乱，例如：192.168.0.1,root,root,test_db：')
        conn_list = conn_info.split(',')
    # 测试数据库连接问题
    dd_test = DataDict(conn_list)
    db_conn = dd_test.test_conn(conn_list)
    while db_conn == False:
        conn_info = input('请正确输入mysql数据库连接信息(格式为：主机IP,用户名,登录密码,数据库名)，逗号分隔且输入顺序不能乱，例如：192.168.0.1,root,root,test_db：')
        conn_list = conn_info.split(',')
        if len(conn_list) != 4:
            continue
        dd_test = DataDict(conn_list)
        db_conn = dd_test.test_conn(conn_list)
    # 输入数据表名称
    table_s = input('请输入数据库表名(例如：t_order)，如需输入多个表名请用英文逗号分隔(例如：t_order,t_goods)，结束使用请输入q：')
    dd = DataDict(conn_list)
    while table_s != 'q':
        dd.run(table_s)
        table_s = input('继续使用请输入数据库表名（例如t_order），如需输入多个表名请用英文逗号分隔（例如t_order,t_goods），结束使用请输入q）：')
    else:
        print('谢谢使用，再见……')
        time.sleep(1)
```

### 最后

老规矩，大家有任何问题，都可以留言或者各种渠道告诉我，虽然我可能也不会去修改。方法和思路万千，如果你有其他思路以及想法的，欢迎留言分享和交流……