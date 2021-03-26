---
title: 活动链接再也不用转发朋友圈集赞了-python刷赞
date: 2021-03-26 15:28:19
tags: [Python, requests, bs4]
---

![](https://image-static.segmentfault.com/756/069/756069993-605d8c625e967_fix732)

### 你有没有让人帮忙点过赞呢

我们的微信朋友圈，可能会经常遇到有朋友转发链接让进入帮忙点赞的，有的需要微信登陆点赞，有的直接无需登录即可点赞，有的活动链接可能还只限在微信内打开等等，类似这种集赞的活动，其实我们都是可以刷的，不用费半天劲每天各种转发朋友圈和微信群求赞了，轻轻松松可以搞定。

### 刷赞思路

活动肯定都是以网页的形式去分享转发的，那么我们就可以拿到活动地址，以及通过`fildder`工具抓取点赞的相关接口，然后通过代理IP请求点赞接口即可，具体的还得看活动的接口规则，大概稍加调整即可。

<!--more-->

### 运行环境

Python运行环境：Windows + python3.8   
用到的模块：`requests、bs4、time、multiprocessing`  
如未安装的模块，请使用`pip instatll xxxxxx`进行安装，例如：`pip install requests`

### 抓取

通过电脑端在`fillder`工具上抓取到点赞接口，然后拿到接口地址、请求参数以及一些header头信息，下面是我抓取的一个活动的点赞接口相关信息（为了隐私信息，地址和参数信息都是虚假的，大家主要看这个思路就可以了）

```python
def __init__(self):
    # 继承Process类
    super(XiaoHuanProcess, self).__init__()
    # 点赞接口地址
    self.api_url = 'http://www.xxxxxx.com/topfirst.php?g=Wap&m=Vote&a=ticket'
    # 点赞请求参数
    self.post_param = {'zid': '111', 'vid': '111', 'token': '111'}
    # 接口请求头信息
    self.header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1320.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63010200)',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # 代理IP地址
    self.proxies = {}
    # 超时时间
    self.time_out = 20
```

### 抓取代理IP

因为总是用同一个用户去请求，肯定是不行的，所以，我们就得需要用代理IP去请求，那么就得抓取网上一些可用的IP地址，这里，我随便例举一个代理网站（[https://ip.jiangxianli.com](https://ip.jiangxianli.com)），因为我测试过，这个网站的IP有效性比较高，而且IP地址更新也比较快，具体抓取代码如下：

```python
def get_proxies_ip(self, ip_url):
    """获取代理IP"""
    ip_request = requests.get(url=ip_url)
    html_content = ip_request.content
    soup = BeautifulSoup(html_content, 'html.parser')
    # IP列表
    link_list = soup.select('link')
    is_start = False
    ip_list = []
    for link in link_list:
        url_info = link.get('href')
        if url_info == '//github.com':
            is_start = True
        if url_info == '//www.baidu.com':
            break
        if is_start and url_info != '//github.com':
            ip_list.append(url_info)
    return ip_list
```

### 执行循环刷赞请求

![](https://image-static.segmentfault.com/422/337/4223378182-605d87eb89575_fix732)

已经有了点赞接口地址，而且代理IP也抓取到了，那么就可以利用代理IP去请求点赞接口，从而实现刷赞的目的。

```python
def run(self):
    """执行程序"""
    while True:
        # 获取前11页
        page_list = range(1, 11)
        for page in page_list:
            request_url = 'https://ip.jiangxianli.com/?page=' + str(page)
            # 获取IP地址
            ip_list = self.get_proxies_ip(request_url)
            for ip_info in ip_list:
                self.proxies = {
                    'http': 'http:' + ip_info,
                    'https': 'https:' + ip_info
                }
                try:
                    # 发送post请求
                    request = requests.post(url=self.api_url, data=self.post_param, headers=self.header,
                                            proxies=self.proxies, timeout=self.time_out)
                    response_text = request.text
                    self.print_msg(response_text)
                except Exception as err_info:
                    # 异常信息
                    self.print_msg(str(err_info))
```

### 完整代码

因为刷赞的过程就是多请求，所以，我们可以利用`multiprocessing`多进程去刷，从而更有效的达到目的，具体的可以看下完整代码即可，更多的可以去交友网站[https://github.com/gxcuizy](https://github.com/gxcuizy/Python/tree/master/%E5%BE%AE%E4%BF%A1%E7%82%B9%E8%B5%9E%E5%88%B7%E7%A5%A8)上面找我哦，我也写了其他代理网站的更多示例，走过路过去看看哦，不会吃亏的。

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
利用代理IP刷点赞票（jiangxianli-多线程）
author: gxcuizy
date: 2021-03-25
"""

import requests
import time
from bs4 import BeautifulSoup
from multiprocessing import Process


class JiangXianLiProcess(Process):
    def __init__(self):
        # 继承Process类
        super(JiangXianLiProcess, self).__init__()
        # 点赞接口地址
	    self.api_url = 'http://www.xxxxxx.com/topfirst.php?g=Wap&m=Vote&a=ticket'
	    # 点赞请求参数
	    self.post_param = {'zid': '111', 'vid': '111', 'token': '111'}
        # 接口请求头信息
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1320.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63010200)',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        # 代理IP地址
        self.proxies = {}
        # 超时时间
        self.time_out = 20

    def get_proxies_ip(self, ip_url):
        """获取代理IP"""
        ip_request = requests.get(url=ip_url)
        html_content = ip_request.content
        soup = BeautifulSoup(html_content, 'html.parser')
        # IP列表
        link_list = soup.select('link')
        is_start = False
        ip_list = []
        for link in link_list:
            url_info = link.get('href')
            if url_info == '//github.com':
                is_start = True
            if url_info == '//www.baidu.com':
                break
            if is_start and url_info != '//github.com':
                ip_list.append(url_info)
        return ip_list

    def print_msg(self, msg=''):
        """打印信息"""
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print('[' + now_time + '] ' + msg)

    def run(self):
        """执行程序"""
        while True:
            # 获取前11页
            page_list = range(1, 11)
            for page in page_list:
                request_url = 'https://ip.jiangxianli.com/?page=' + str(page)
                # 获取IP地址
                ip_list = self.get_proxies_ip(request_url)
                for ip_info in ip_list:
                    self.proxies = {
                        'http': 'http:' + ip_info,
                        'https': 'https:' + ip_info
                    }
                    try:
                        # 发送post请求
                        request = requests.post(url=self.api_url, data=self.post_param, headers=self.header,
                                                proxies=self.proxies, timeout=self.time_out)
                        response_text = request.text
                        self.print_msg(response_text)
                    except Exception as err_info:
                        # 异常信息
                        self.print_msg(str(err_info))


# 程序主入口
if __name__ == '__main__':
    # 获取运行的进程数
    process_num = input('请输入运行进程数：')
    process_list = []
    for i in range(int(process_num)):
        p = JiangXianLiProcess()
        # star默认执行run()方法
        p.start()
        process_list.append(p)
    # 循环执行多进程
    for process in process_list:
        process.join()
        # 每个进程间隔10秒执行
        time.sleep(10)

```

### 最后

大家有任何问题，都可以给我留言给我，我会及时回复，如有说的不对的地方，还请大家帮忙纠正。如果大家有什么好的想法或者建议，也可以底部留言给我哈，感谢哦！