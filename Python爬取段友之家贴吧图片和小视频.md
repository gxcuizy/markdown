由于最新的视频整顿风波，内涵段子APP被迫关闭，广大段友无家可归，但是最近发现了一个“段友”的app，版本更新也挺快，正在号召广大段友回家，如下图，有兴趣的可以下载看看（ps：我不是打广告的，没收广告费的）
![图片描述][1]

同时，之前同事也发了一个贴吧的段子聚居地，客官稍等，马上奉上连接：
[段友之家][2]   https://tieba.baidu.com/f?ie=utf-8&kw=段友之家

然后呢，看到上面，确实好多段友在上面，于是乎，我就想爬取他们的图片和小视频，就有了这篇文章的主题：

其实吧，用Python爬取网站数据是最基础的东西，也不难，但是我还想分享给大家，一起学习和交流。

爬取这些网站里的数据主要用的模块是bs4、requests以及os，都是常用模块

大概思路就是通过requests模块请求网页html数据，然后通过bs4模块下的BeautifulSoup分析请求的网页，然后通过css查找器查找内涵段子的图片以及小视频的地址，主要实现代码如下：

```
def download_file(web_url):
    """获取资源的url"""
    # 下载网页
    print('正在下载网页： %s...' % web_url)
    result = requests.get(web_url)
    soup = bs4.BeautifulSoup(result.text, "html.parser")
    # 查找图片资源
    img_list = soup.select('.vpic_wrap img')
    if img_list == []:
        print('未发现图片资源！')
    else:
        # 找到资源，开始写入
        for img_info in img_list:
            file_url = img_info.get('bpic')
            write_file(file_url, 1)
    # 查找视频资源
    video_list = soup.select('.threadlist_video a')
    if video_list == []:
        print('未发现视频资源！')
    else:
        # 找到资源，开始写入
        for video_info in video_list:
            file_url = video_info.get('data-video')
            write_file(file_url, 2)
    print('下载资源结束：', web_url)
    next_link = soup.select('#frs_list_pager .next')
    if next_link == []:
        print('下载资料结束！')
    else:
        url = next_link[0].get('href')
        download_file('https:' + url)
```

得到图片以及视频的地址之后，肯定还不够，还得把这些资源写入到本地，方式是通过二进制的方式来读取远程文件资源，然后分类写入到本地，实现的主要代码如下：

```
def write_file(file_url, file_type):
    """写入文件"""
    res = requests.get(file_url)
    res.raise_for_status()
    # 文件类型分文件夹写入
    if file_type == 1:
        file_folder = 'nhdz\\jpg'
    elif file_type == 2:
        file_folder = 'nhdz\\mp4'
    else:
        file_folder = 'nhdz\\other'
    folder = os.path.exists(file_folder)
    # 文件夹不存在，则创建文件夹
    if not folder:
        os.makedirs(file_folder)
    # 打开文件资源，并写入
    file_name = os.path.basename(file_url)
    str_index = file_name.find('?')
    if str_index > 0:
        file_name = file_name[:str_index]
    file_path = os.path.join(file_folder, file_name)
    print('正在写入资源文件：', file_path)
    image_file = open(file_path, 'wb')
    for chunk in res.iter_content(100000):
        image_file.write(chunk)
    image_file.close()
    print('写入完成！')
```

最后，再奉上完整的代码吧。要不然，会被人说的，说话说一半，说福利，也不给全，这就太不够意思了。客官别急，马上奉上……

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
爬取百度贴吧，段友之家的图片和视频
author: cuizy
time：2018-05-19
"""

import requests
import bs4
import os


def write_file(file_url, file_type):
    """写入文件"""
    res = requests.get(file_url)
    res.raise_for_status()
    # 文件类型分文件夹写入
    if file_type == 1:
        file_folder = 'nhdz\\jpg'
    elif file_type == 2:
        file_folder = 'nhdz\\mp4'
    else:
        file_folder = 'nhdz\\other'
    folder = os.path.exists(file_folder)
    # 文件夹不存在，则创建文件夹
    if not folder:
        os.makedirs(file_folder)
    # 打开文件资源，并写入
    file_name = os.path.basename(file_url)
    str_index = file_name.find('?')
    if str_index > 0:
        file_name = file_name[:str_index]
    file_path = os.path.join(file_folder, file_name)
    print('正在写入资源文件：', file_path)
    image_file = open(file_path, 'wb')
    for chunk in res.iter_content(100000):
        image_file.write(chunk)
    image_file.close()
    print('写入完成！')


def download_file(web_url):
    """获取资源的url"""
    # 下载网页
    print('正在下载网页： %s...' % web_url)
    result = requests.get(web_url)
    soup = bs4.BeautifulSoup(result.text, "html.parser")
    # 查找图片资源
    img_list = soup.select('.vpic_wrap img')
    if img_list == []:
        print('未发现图片资源！')
    else:
        # 找到资源，开始写入
        for img_info in img_list:
            file_url = img_info.get('bpic')
            write_file(file_url, 1)
    # 查找视频资源
    video_list = soup.select('.threadlist_video a')
    if video_list == []:
        print('未发现视频资源！')
    else:
        # 找到资源，开始写入
        for video_info in video_list:
            file_url = video_info.get('data-video')
            write_file(file_url, 2)
    print('下载资源结束：', web_url)
    next_link = soup.select('#frs_list_pager .next')
    if next_link == []:
        print('下载资料结束！')
    else:
        url = next_link[0].get('href')
        download_file('https:' + url)


# 主程序入口
if __name__ == '__main__':
    web_url = 'https://tieba.baidu.com/f?ie=utf-8&kw=段友之家'
    download_file(web_url)
```

  [1]: https://image-static.segmentfault.com/165/096/1650966636-5b110d6698ba6_articlex
  [2]: https://tieba.baidu.com/f?ie=utf-8&kw=%E6%AE%B5%E5%8F%8B%E4%B9%8B%E5%AE%B6
