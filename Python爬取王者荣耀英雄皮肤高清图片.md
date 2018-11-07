---
title: Python爬取王者荣耀英雄皮肤高清图片
date: 2018-11-07 14:55:42
tags: [Python, requests, bs4, 王者荣耀]
---
### 前言

临下班前，看到群里有人在讨论用王者农药的一些皮肤作为电脑的壁纸，什么高清的，什么像素稍低的，网上查了一手，也有，但像素都不一样，所以，我就想着，自己去官网直接爬他的高清皮肤就好了，然后就有了这边文章说的主题了。

### 爬图思路

#### 找到英雄列表

进入官网，然后进入英雄介绍，查看更多英雄，就能看到全部的英雄了，也就是下面的这个链接

英雄列表：[https://pvp.qq.com/web201605/herolist.shtml](https://pvp.qq.com/web201605/herolist.shtml)

<!--more-->

![hero-img](https://raw.githubusercontent.com/gxcuizy/markdown/master/images/wzry-1.jpg)

#### 英雄详情

点击每个英雄进来，就可以看到每个英雄的详细信息，基本介绍以及皮肤展示，而我们需要爬取的皮肤，就在右下角那里，鼠标放上去，就可以逐个展示该皮肤了

小鲁班的详细信息：[https://pvp.qq.com/web201605/herodetail/112.shtml](https://pvp.qq.com/web201605/herodetail/112.shtml)

![detail-img](https://raw.githubusercontent.com/gxcuizy/markdown/master/images/wzry-2.jpg)

#### 分析皮肤图片URL

从上面的这张鲁班的图片中我们可以看到，通过F12定位到皮肤的小图片位置，li元素里有一个img的元素，其中img的src和data-imgname这两个属性，查看一下，就不难知道，src的属性值是小图，而data-imgname则是我们需要的大图URL，但是查看源码，就会发现，在html中，并没有这个属性，所以，需要我们分析这个URL的规律来得到其他英雄的皮肤图片，分析也不难发现，112就是英雄的id，而bigskin-2里面的2即表示这个英雄的第几张皮肤图片

### 开始编写爬虫脚本

第一步：定义一些常用变量

第二步：抓取所有英雄列表

第三步：循环遍历，分析每个英雄皮肤节点

第四步：下载图片

第五步：爬虫结束

### 完整源码

感觉上面七七八八的，说了些啥呀，真是墨迹，还不如直接上代码实在，好吧，我错了，马上交出源码，请各位看官饶恕，同时，代码我也上传了交友网站[GitHub](https://github.com/gxcuizy/Python/blob/master/%E7%8E%8B%E8%80%85%E8%8D%A3%E8%80%80%E7%9A%AE%E8%82%A4%E7%88%AC%E5%9B%BE/wzry.py)。

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
抓取王者荣耀皮肤
author: gxcuizy
date: 2018-11-06
"""

import requests
from bs4 import BeautifulSoup
from urllib import parse
import os


class Skin(object):
    def __init__(self):
        # 英雄的json数据
        self.hero_url = 'https://pvp.qq.com/web201605/js/herolist.json'
        # 英雄详细页的通用url前缀信息
        self.base_url = 'https://pvp.qq.com/web201605/herodetail/'
        # 英雄详细页url后缀信息
        self.detail_url = ''
        # 图片存储文件夹
        self.img_folder = 'skin'
        # 图片url的通用前缀
        self.skin_url = 'https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/'
        # 图片url的后缀信息
        self.skin_detail_url = ''

    def get_hero(self):
        """获取英雄的json数据"""
        request = requests.get(self.hero_url)
        hero_list = request.json()
        return hero_list

    def get_hero_skin(self, hero_name, hero_no):
        """获取详细页英雄皮肤展示的信息，并爬图"""
        url = parse.urljoin(self.base_url, self.detail_url)
        request = requests.get(url)
        request.encoding = 'gbk'
        html = request.text
        # 获取皮肤信息的节点
        soup = BeautifulSoup(html, 'lxml')
        skip_list = soup.select('.pic-pf-list3')
        for skin_info in skip_list:
            # 获取皮肤名称
            img_names = skin_info.attrs['data-imgname']
            name_list = img_names.split('|')
            skin_no = len(name_list)
            # 循环下载皮肤图片
            for skin_name in name_list:
                self.skin_detail_url = '%s/%s-bigskin-%s.jpg' % (hero_no, hero_no, skin_no)
                skin_no -= 1
                img_name = hero_name + '-' + skin_name + '.jpg'
                self.download_skin(img_name)

    def download_skin(self, img_name):
        """下载皮肤图片"""
        img_url = parse.urljoin(self.skin_url, self.skin_detail_url)
        request = requests.get(img_url)
        if request.status_code == 200:
            print('download-%s' % img_name)
            img_path = os.path.join(self.img_folder, img_name)
            with open(img_path, 'wb') as img:
                img.write(request.content)
        else:
            print('img error!')

    def make_folder(self):
        """创建图片存储文件夹"""
        if not os.path.exists(self.img_folder):
            os.mkdir(self.img_folder)

    def run(self):
        """脚本执行入口"""
        self.make_folder()
        hero_list = self.get_hero()
        for hero in hero_list:
            hero_no = str(hero['ename'])
            self.detail_url = hero_no + '.shtml'
            hero_name = hero['cname']
            self.get_hero_skin(hero_name, hero_no)


# 程序执行入口
if __name__ == '__main__':
    skin = Skin()
    skin.run()

```

### 最后

其实思路就是这么简单，当然了，如果有其他思路以及想法的，欢迎留言交流。额，差点忘了，大家有兴趣的，可以尝试一下爬取英雄联盟的所有英雄皮肤高清图片，有其他任何问题，也欢迎留言和交流。

