---
title: 通过Python爬取国家统计局省市区三级地址库（支持MySQL和JSON格式）
date: 2018-08-27 10:09:29
tags: [Python, MySQL, JSON]
---

![Python][page_img_url]

### 数据来源

通过Python脚本，自动抓取[国家统计局][stats_url]最新的中国省市区三级城市信息，目前抓取的最新数据为[2017年统计用区划代码和城乡划分代码(截止2017年10月31日)][origin_area_url]，我会关注，时刻保持更新。

### 数据格式

目前支持MySQL格式和JSON格式，其中MySQL的有两个版本，分别为三张表和一张表的，即三张表的为省市区三张表，而一张表的则把省市区三级城市通过关联关系都存在一张表中，可以根据自己的需求进行选择，如果有其他格式需求，可以联系我或者自己修改脚本。

### 脚本目录结构

```
├── json                     # 存储JSON数据格式
├── mysql                    # 存储三张表的数据格式
├── mysql_v2                 # 存储一张表的数据格式
├── city_to_json.py          # 抓取JSON数据格式的脚本
├── city_mysql.py            # 抓取三张表的数据格式的脚本
├── city_to_mysql_v2.py      # 抓取一张表的数据格式的考平贝母
├── mysql_init.sql           # 存储三张表的数据的表结构
├── mysql_v2_init            # 存储一张表的数据的表结构
```
如有需要，直接下载后缀为json或者sql的文件即可直接使用，也可以根据对应的python脚本重新生成相应的省市区三级地址库数据。

### 抓取数据方法

这里主要使用[requests][requests_url]、[beautifulsoup4][bs4_url]以及[json][json_url]这三个模块，通过requests发送url页面请求，然后BeautifulSoup分析请求到的页面信息，抓取有效数据，通过json模块，读取以及存储json格式的数据，而mysql的数据则直接通过文件的读写操作即可。

### 源码分享

这个爬虫脚本比较易读，而且碍于文章篇幅问题，所以，我这里就不贴源码了，直接放到交友网站GitHub上了，有兴趣的可以前往查看。

源码以及数据地址：[https://github.com/gxcuizy/Python/tree/master/area][code_url]

[page_img_url]: https://images.unsplash.com/photo-1526379095098-d400fd0bf935?ixlib=rb-0.3.5&s=1cca0d0544f25ab7c6e171d80692ed62&auto=format&fit=crop&w=1189&q=80
[stats_url]: http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/
[origin_area_url]: http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html
[requests_url]: http://docs.python-requests.org/zh_CN/latest/user/quickstart.html
[bs4_url]: https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html
[json_url]: https://docs.python.org/3.6/library/json.html
[code_url]: https://github.com/gxcuizy/Python/tree/master/area