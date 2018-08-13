---
title: Python下载网易云歌曲（版权限制的怎么播放和下载呢？）
date: 2018-08-08 17:19:13
tags: [Python, requests, 网易云音乐]
---

### 为什么要这样下载
[网易云音乐][yinyue]，我相信大多数人都用过，我个人觉得非常好用，也一直在用，有的时候，我们搜索一些网易歌曲，发现播放不了，甚至下载不了，因为提示“版权方要求，当前歌曲仅限开通音乐包使用”（见下图），也就是，需要购买才能够下载以及播放，有没有办法不花钱就能播放和下载这首歌曲呢？我研究了一下，还没发现呢，哈哈哈哈，往下看，你会发现惊喜的……

![网易云歌曲][wangyiyun]

<!-- more -->

### 怎么查找版权限制不让下载和播放的音乐

#### 初探network请求信息

首先，我想到的是打开F12，查看所有的network请求，一个一个的查看请求返回信息，突然发现了惊喜，如下图所示：

![网易云音乐F12请求][wangyiyun_request]

那个请求返回的url，我想应该就是音乐的URL源地址，但是，我通过Python脚本下载这个音乐下来后发现，和我想象的有点不一样，因为这个url确实是音乐的源地址，但是并不是我需要的，因为这个url是当前播放音乐的源地址，然后，我继续点击其他按钮，当我点击播放音乐按钮的时候，有一个detail的请求，里面返回了很多信息，如下图所示：

![网易云音乐播放请求][wangyiyun_play]

#### 深入查看network请求信息

我研究了一下这些返回信息，发现并没有找到需要的音乐url源地址，然后只能继续在network里面找，刚开始，我只是找的XHR的请求，然后我想着，查找All的请求试试，因为，All请求里，可以包含所有的资源请求，包括图片以及文件资源等，也许会有惊喜，果然，不出所料，让我找到了一个好东西，如下图这样的：

![网易云音乐资源请求][wangyiun_download]

#### 发现惊喜

因为通过前面拿到当前播放的音乐的url源地址，猜想着所有的音乐的url应该都包含着mp3的后缀，所以，我就Ctrl+F，进行mp3的搜索，果然，看到包含mp3的请求就那几个，然后逐一分析，发现，有一个请求信息，也就是上图中的第一个请求，是一个MP3文件资源，所以，我猜想，这个应该就是我需要的音乐URL了吧，然后我拿到这个URL继续去下载文件资源，果然，这就是我需要的音乐URL源地址，到这里，也就是找到了这个因为版权受限不让播放和下载的音乐了，惊不惊喜？意不意外？

### Python下载MP3文件源码

最后，分享一波Python下载MP3资源的源码，使用的时候，得先进行几个配置，首先是url，url就是需要下载的音乐URL地址，folder就是音乐需要保存的位置，话不多说，直接上源码

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
下载MP3文件
author: gxcuizy
time：2018-08-08
"""

import requests
import os


def download_file(mp3_url, file_folder):
    """下载MP3文件"""
    # 文件夹不存在，则创建文件夹
    folder = os.path.exists(file_folder)
    if not folder:
        os.makedirs(file_folder)
    # 读取远程MP3资源
    res = requests.get(mp3_url)
    res.raise_for_status()
    # 获取文件名
    file_name = os.path.basename(mp3_url)
    file_path = os.path.join(file_folder, file_name)
    print('正在写入资源文件：', file_path)
    # 保存到本地
    image_file = open(file_path, 'wb')
    for chunk in res.iter_content(100000):
        image_file.write(chunk)
    image_file.close()
    print('写入文件结束！')


# 程序主入口
if __name__ == "__main__":
    # MP3源地址url
    url = 'http://m10.music.126.net/20180808172234/4446d41c850238c25cdcff1fe43249a4/ymusic/3686/b5b4/961c/39c9a20e7db813ea3290e1b1580cfa70.mp3'
    # MP3保存文件夹
    folder = 'mp3/'
    # 调用下载方法
    download_file(url, folder)

```

### 结束语

大家有什么不理解或者不明白的的，可以联系我，或者给我留言，我会及时回复的，欢迎沟通和交流，谢谢。


[yinyue]: https://music.163.com/
[wangyiyun]: /images/wangyiyun.png
[wangyiyun_request]: /images/wangyiyun_request.png
[wangyiyun_play]: /images/wangyiyun_play.png
[wangyiun_download]: /images/wangyiun_download.png
