### 前言

上篇文章，说到了，爬取LOL英雄皮肤的高清图片，最近有事，也没怎么去研究，所以，现在才去看了下，并且写了Python脚本来抓取皮肤图片。需要说明一下，这个脚本有部分英雄没有抓取到，但是具体原因，我目前还没搞懂，我是相当纳闷的。大家有兴趣的，可以看看后面遗留问题，一起研究下。

### 爬虫思路

#### 初步尝试

我先查看了network，并没有发现有可用的API；然后又用bs4去分析[英雄列表](https://lol.qq.com/data/info-heros.shtml)页，但是请求到html里面，并没有英雄列表，在英雄列表的节点上，只有“正在加载中”这样的字样；同样的方法，分析[英雄详情](https://lol.qq.com/data/info-defail.shtml?id=Aatrox)也是这种情况，所以我猜测，这些数据应该是Javascript负责加载的。

![step-1](https://raw.githubusercontent.com/gxcuizy/markdown/master/images/lol-step-1.png)

#### 继续尝试

然后我就查看了[英雄列表的源代码](view-source:https://lol.qq.com/data/info-heros.shtml)，查看外部引入的js文件，以及行内的js脚本，大概在368行，发现了有处理英雄列表的js注释，然后继续往下读这些代码，发现了第一个彩蛋，也就是他引入了一个[champion.js](http://lol.qq.com/biz/hero/champion.js)的文件，我猜测，这个应该就是英雄列表大全了，然后我打开了这个链接的js，一眼看过去，黑麻麻一片，然后格式化了一下压缩的js，确定这就是英雄列表的js数据文件了。

![step-2](https://raw.githubusercontent.com/gxcuizy/markdown/master/images/lol-step=2.png)

#### 接着尝试

前面通过查看列表的源代码，找到了英雄列表的js数据文件，那么，我继续随机点开了一个英雄的详情，然后查看[英雄详情源代码](view-source:https://lol.qq.com/data/info-defail.shtml?id=Aatrox)，然后大概在568行看到有一个showSkin的js方法，通过这里，发现了第二个彩蛋，也就是皮肤图片的URL地址拼接方法。

![step-3](https://raw.githubusercontent.com/gxcuizy/markdown/master/images/lol-step=3.jpg)

#### 最后尝试

上面找到了皮肤图片URL的拼接方法，并且发现了一行很关键的代码`var skin =LOLherojs.champion[heroid].data.skins`，也就是，这个skin变量，就是英雄皮肤的所有图片数组，但是这个文件内，并没有LOLherojs这个变量，也就是外部引入的，所以，需要继续查看下面的源代码，找到引入这个变量的位置，果不其然，在757行，发现了最后一个彩蛋，也就是，英雄皮肤的js文件，通过这里可以知道，每个英雄都有一个单独的js文件，并且知道了这个js文件的URL拼接方法。

![step-4](https://raw.githubusercontent.com/gxcuizy/markdown/master/images/lol-step-4.jpg)

### 思路总结

通过上面的分析，我们就得到了爬取LOL皮肤图片的所有数据准备了，也就是，直接，只需要提取js中的英雄列表以及英雄详情数据，就可实现我们的需求了。下面是运行后抓取到的图片……

![step-5](https://raw.githubusercontent.com/gxcuizy/markdown/master/images/lol-step-5.jpg)

### 运行环境

Python运行环境：python3.6  
用到的模块：requests、json、urllib、os、lxml  
未安装的模块，请使用pip instatll进行安装，例如：pip install requests

### 完整代码

其他啥的废话就不多说了，直接上完整代码，有问题，直接留言给我就行，另外，代码已上传[GitHub](https://github.com/gxcuizy/Python/blob/master/英雄联盟皮肤爬图/get_lol_skin.py)。再说明一下，那些有问题的英雄详情的js文件，大家有时间也可以琢磨下，或者有其他的更加快捷的爬取这些图片的方法，也可以拿出来交流和讨论，谢谢。

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
抓取英雄联盟英雄全皮肤
author: gxcuizy
date: 2018-11-13
"""

import requests
import json
from urllib import parse
import os


class GetLolSkin(object):
    """抓取LOL英雄皮肤"""

    def __init__(self):
        """初始化变量"""
        self.hero_url = 'https://lol.qq.com/biz/hero/champion.js'
        self.hero_detail_url = 'http://lol.qq.com/biz/hero/'
        self.skin_folder = 'skin'
        self.skin_url = 'https://ossweb-img.qq.com/images/lol/web201310/skin/big'

    @staticmethod
    def get_html(url):
        """下载html"""
        request = requests.get(url)
        request.encoding = 'gbk'
        if request.status_code == 200:
            return request.text
        else:
            return "{}"

    def get_hero_list(self):
        """获取英雄的完整信息列表"""
        hero_js = self.get_html(self.hero_url)
        # 删除左右的多余信息，得到json数据
        out_left = "if(!LOLherojs)var LOLherojs={};LOLherojs.champion="
        out_right = ';'
        hero_list = hero_js.replace(out_left, '').rstrip(out_right)
        return json.loads(hero_list)

    def get_hero_info(self, hero_id):
        """获取英雄的详细信息"""
        # 获取js详情
        detail_url = parse.urljoin(self.hero_detail_url, hero_id + '.js')
        detail_js = self.get_html(detail_url)
        # 删除左右的多余信息，得到json数据
        out_left = "if(!herojs)var herojs={champion:{}};herojs['champion'][%s]=" % hero_id
        out_right = ';'
        hero_info = detail_js.replace(out_left, '').rstrip(out_right)
        return json.loads(hero_info)

    def download_skin_list(self, skin_list, hero_name):
        """下载皮肤列表"""
        # 循环下载皮肤
        for skin_info in skin_list:
            # 拼接图片名字
            if skin_info['name'] == 'default':
                skin_name = '默认皮肤'
            else:
                if ' ' in skin_info['name']:
                    name_info = skin_info['name'].split(' ')
                    skin_name = name_info[0]
                else:
                    skin_name = skin_info['name']
            hero_skin_name = hero_name + '-' + skin_name + '.jpg'
            self.download_skin(skin_info['id'], hero_skin_name)

    def download_skin(self, skin_id, skin_name):
        """下载皮肤图片"""
        # 下载图片
        img_url = self.skin_url + skin_id + '.jpg'
        request = requests.get(img_url)
        if request.status_code == 200:
            print('downloading……%s' % skin_name)
            img_path = os.path.join(self.skin_folder, skin_name)
            with open(img_path, 'wb') as img:
                img.write(request.content)
        else:
            print('img error!')

    def make_folder(self):
        """初始化，创建图片文件夹"""
        if not os.path.exists(self.skin_folder):
            os.mkdir(self.skin_folder)

    def run(self):
        # 获取英雄列表信息
        hero_json = self.get_hero_list()
        hero_keys = hero_json['keys']
        # 循环遍历英雄
        for hero_id, hero_code in hero_keys.items():
            hero_name = hero_json['data'][hero_code]['name']
            hero_info = self.get_hero_info(hero_id)
            if hero_info:
                skin_list = hero_info['result'][hero_id]['skins']
                # 下载皮肤
                self.download_skin_list(skin_list, hero_name)
            else:
                print('英雄【%s】的皮肤获取有问题……' % hero_name)


# 程序执行入口
if __name__ == '__main__':
    lol = GetLolSkin()
    # 创建图片存储文件
    lol.make_folder()
    # 执行脚本
    lol.run()

```