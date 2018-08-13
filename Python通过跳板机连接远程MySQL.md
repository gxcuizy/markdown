---
title: Python通过跳板机连接远程MySQL
date: 2018-08-10 10:35:09
tags: [python, mysql]
---

### 工具直接跳板机连接远程MySQL数据库
一般公司的数据库在一个远程服务器里，而这个服务器需要链接跳板机才可以访问，而通过远程桌面或云桌面才可以链接跳板机，说明访问数据库是需要一定的权限的（很多公司也不会让你通过本机就可以获取内部数据）这就有个问题了，也就是你不可能在本机直接去访问数据库，这个时候，就需要一些数据库管理工具，例如常用的Navicat、SQLyog等，都是可以的，下面是我Navicat的一些配置（打码部分为配置信息）：

<!-- more -->

SSH连接配置信息

![ssh连接信息][mysql_attr]

MySQL连接属性常规信息

![连接常规信息][mysql_common]

### Python连接

#### 安装sshtunnel

Python连接的话，得借助sshtunnel模块，这个模块是第三方的模块，所以得先安装，安装方式如下，直接命令行安装就行。

```
pip insall sshtunnel
```

#### 基本配置说明

```
# 跳板机SSH连接
with SSHTunnelForwarder(
        ('192.168.0.1', 22),
        ssh_username="test",
        ssh_pkey="test.pem",
        remote_bind_address=('*************mysql.rds.aliyuncs.com', 3306)
) as tunnel:
    # 数据库连接配置，host默认127.0.0.1不用修改
    conn = pymysql.connect(
        host='127.0.0.1',
        port=tunnel.local_bind_port,
        user='root',
        password='root',
        db='test',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
```
从上面代码可以看到，跳板机的SSH配置信息，192.168.0.1为服务器IP地址，ssh_username为用户名，ssh_pkey为本机私钥存放位置，remote_bind_address为跳板机地址，user为mysql连接用户名，passport为密码，db就是连接的数据库名了，其他的不用配置了，发现连接不对的，就再核对一些配置信息，连接完毕，一定记得关闭连接。

### 完整源码分享

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
通过跳板机，连接远程mysql数据库
author: gxcuizy
time: 2018-08-10
"""

import pymysql
from sshtunnel import SSHTunnelForwarder

# 程序主入口
if __name__ == "__main__":
    # 跳板机SSH连接
    with SSHTunnelForwarder(
            ('192.168.0.1', 22),
            ssh_username="test",
            ssh_pkey="test.pem",
            remote_bind_address=('*************mysql.rds.aliyuncs.com', 3306)
    ) as tunnel:
        # 数据库连接配置，host默认127.0.0.1不用修改
        conn = pymysql.connect(
            host='127.0.0.1',
            port=tunnel.local_bind_port,
            user='root',
            password='root',
            db='test',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )
        # 获取游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 查询数据库，查询一条数据，其他CURD操作类似
        sql = "SELECT name FROM table_name WHERE id = '%s'"
        prams = ('1',)
        cursor.execute(sql % prams)
        info = cursor.fetchone()
        print(info)
        # 关闭连接
        cursor.close()
        conn.close()
```

### 结束语

Python可以做很多事情，大家有兴趣的话，可以一起研究和讨论，如有疑问，可以留言或者直接联系我，谢谢。

[mysql_attr]: /images/mysql_attr.png
[mysql_common]: /images/mysql_common.png