---
title: Python分析BOSS直聘的某个招聘岗位数据
date: 2020-06-24 14:56:08
tags: [Python, 爬虫, 招聘, 求职]
---

![](https://image-static.segmentfault.com/522/250/522250456-5ef2f1389257d_articlex)

### 前言

毕业找工作，在职人员换工作，离职人员找工作……不管什么人群，应聘求职，都需要先分析对应的招聘岗位，岗位需求是否和自己匹配，常见的招聘平台有：BOSS直聘、拉钩招聘、智联招聘等，我们通常的方法都是，打开招聘网站，搜索职位关键字，然后一页一页的逐个查看，觉得还不错的岗位就投递一下简历，或者和招聘负责人聊一下，那么有没有办法，能一次性把相关的招聘岗位列出来，方便快速的分析，答案当然有的……

<!--more-->

### 我想做什么

最近我也在考虑新的工作机会，所以，为了方便才这么做的；下面给大家看个东西，打开后面的链接[BOSS直聘的100个PHP招聘岗位](http://note.youdao.com/noteshare?id=0b992488918ed30835ad1e406a4fd4d7)

可以看到，这是表格的形式展示了100个PHP的招聘岗位，没错，这就是我爬取的BOSS直聘网的PHP招聘岗位，为啥是100个呢，我也不敢问啊，毕竟BOSS直聘官网限制了10页，通过爬取数据，然后生成`markdown`表格文件，最后展示在有道分享中，就是上面大家看到的那个了，话不多说，开搞。

### 运行环境

Python运行环境：Windows + python3.6  
用到的模块：`requests、bs4`  
如未安装的模块，请使用`pip instatll xxxxxx`进行安装，例如：`pip install requests`

### 爬取Boss直聘数据

在这里，非常不建议大家使用自己的IP去爬取BOSS直聘的数据，因为分分钟就会进小黑屋了，所以，这里，我们走的代理IP，关于代理IP的，我在上篇文章，已经有说到过，大家不明白的可以回头看看；还有在`header`头传的`cookie`值是必传的，大家可以在浏览器中刷新BOSS直聘网站，然后打开`F12`的`Network`中找到，复制过来就能用，而且需要更换，不要一直用同个`cookie`去爬取全部数据，多尝试都懂的……

```python
def get_url_html(self, url, cookie):
    """请求页面html"""
    ip_url = self.proxies_ip + ':' + str(self.proxies_port)
    proxies = {'http': 'http://' + ip_url, 'https': 'https://' + ip_url}
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'cookie': cookie
    }
    request = requests.get(url=url, headers=header, proxies=proxies, timeout=3)
    html = False
    if request.status_code == 200:
        html = request.content
    return html
```

### 完整源码

老规矩，代码我已经上传了GitHub（[GitHub源码地址](https://github.com/gxcuizy/Python/tree/master/%E7%88%AC%E5%8F%96Boss%E7%9B%B4%E8%81%98%E6%95%B0%E6%8D%AE)），但是呢，作为一个热心的搬瓦工，为了方便部分人想偷懒，不直接去交友网站查看，我在这里也贴一下源码出来吧，如果有啥问题，最好还是去交友网站找我，请接码……

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
利用requests+bs4爬取Boss直聘数据
author: gxcuizy
date: 2020-06-18
"""

import requests
from bs4 import BeautifulSoup


class GetBossData(object):
    """爬取10页的Boss直聘职位数据"""
    domain = 'https://www.zhipin.com'
    base_url = 'https://www.zhipin.com/c101280600/?query='
    position = ''
    # 代理IP地址
    proxies_ip = '58.220.95.30'
    proxies_port = '10174'

    def __init__(self, position):
        self.position = position

    def get_url_html(self, url, cookie):
        """请求页面html"""
        ip_url = self.proxies_ip + ':' + str(self.proxies_port)
        proxies = {'http': 'http://' + ip_url, 'https': 'https://' + ip_url}
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'cookie': cookie
        }
        request = requests.get(url=url, headers=header, proxies=proxies, timeout=3)
        html = False
        if request.status_code == 200:
            html = request.content
        return html

    def run(self):
        """执行入口"""
        page_list = range(1, 11)
        # 打开文件，准备写入
        dict_file = open('job.md', 'a', encoding='UTF-8')
        # 清空文件内容
        dict_file.seek(0)
        dict_file.truncate()
        dict_file.write('| 岗位 | 区域 | 薪资 | 年限信息 | 公司名称 | 公司信息 | 链接 |')
        dict_file.write('\n| --- | --- | --- | --- | --- | --- | --- |')
        # 分页爬取数据
        for page in page_list:
            print('开始爬取第' + str(page) + '页数据')
            boss_url = self.base_url + str(self.position) + '&page=' + str(page) + '&ka=page-' + str(page)
            # F12打开调试模式，手动刷新网页获取cookie，然后替换
            if page < 4:
                cookie_val = 'lastCity=101280600; __zp_seo_uuid__=d59649f5-bc8a-4263-b4e1-d5fb1526ebbe; __c=1592469667; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1592469673; __l=l=%2Fwww.zhipin.com%2Fshenzhen%2F&r=https%3A%2F%2Fwww.google.com%2F&friend_source=0&friend_source=0; toUrl=https%3A%2F%2Fwww.zhipin.com%2F%2Fjob_detail%2F3f35305467e161991nJ429i4GA%7E%7E.html; __a=43955211.1592469667..1592469667.39.1.39.39; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1592530438; __zp_stoken__=7f3aaPCVBFktLe0xkP21%2BJSFCLWILSwx7NEw4bVJkRx8pdBE3JGNmWjVwdx5PXC8rHmN%2BJB0hX1UvTz5VPyMmOhIVHBglVzoxJQIdLQtKR3ZFBFIeazwOByVndHwXBAN%2FXFo7W2BffFxtXSU%3D; __zp_sseed__=Ykg0aQ3ow1dZqyi9KmeVnWrqZXcZ32a4psiagwqme3M=; __zp_sname__=93bf4835; __zp_sts__=1592530479301'
            elif page < 7:
                cookie_val = 'lastCity=101280600; __zp_seo_uuid__=d59649f5-bc8a-4263-b4e1-d5fb1526ebbe; __c=1592469667; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1592469673; __l=l=%2Fwww.zhipin.com%2Fshenzhen%2F&r=https%3A%2F%2Fwww.google.com%2F&friend_source=0&friend_source=0; toUrl=https%3A%2F%2Fwww.zhipin.com%2F%2Fjob_detail%2F3f35305467e161991nJ429i4GA%7E%7E.html; __a=43955211.1592469667..1592469667.39.1.39.39; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1592530438; __zp_stoken__=7f3aaPCVBFktLe0xkP21%2BJSFCLWILSwx7NEw4bVJkRx8pdBE3JGNmWjVwdx5PXC8rHmN%2BJB0hX1UvTz5VPyMmOhIVHBglVzoxJQIdLQtKR3ZFBFIeazwOByVndHwXBAN%2FXFo7W2BffFxtXSU%3D; __zp_sseed__=Ykg0aQ3ow1dZqyi9KmeVnWrqZXcZ32a4psiagwqme3M=; __zp_sname__=93bf4835; __zp_sts__=1592530514188'
            elif page < 10:
                cookie_val = 'lastCity=101280600; __zp_seo_uuid__=d59649f5-bc8a-4263-b4e1-d5fb1526ebbe; __c=1592469667; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1592469673; __l=l=%2Fwww.zhipin.com%2Fshenzhen%2F&r=https%3A%2F%2Fwww.google.com%2F&friend_source=0&friend_source=0; toUrl=https%3A%2F%2Fwww.zhipin.com%2F%2Fjob_detail%2F3f35305467e161991nJ429i4GA%7E%7E.html; __a=43955211.1592469667..1592469667.40.1.40.40; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1592530479; __zp_stoken__=7f3aaPCVBFktLCT4uVVV%2BJSFCLWIVPWZyNUk4bVJkR25XXHVeZWNmWjVwd286Sm83HmN%2BJB0hX1UvBiBVRyt9IWQOcRtWSk83fAsfJAtKR3ZFBE5efUl%2FByVndHwXRQN%2FXFo7W2BffFxtXSU%3D; __zp_sseed__=Ykg0aQ3ow1dZqyi9KmeVnd/9vyiSRHrJFoMai+azsb8=; __zp_sname__=93bf4835; __zp_sts__=1592530496863'
            else:
                cookie_val = 'lastCity=101280600; __zp_seo_uuid__=d59649f5-bc8a-4263-b4e1-d5fb1526ebbe; __c=1592469667; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1592469673; __l=l=%2Fwww.zhipin.com%2Fshenzhen%2F&r=https%3A%2F%2Fwww.google.com%2F&friend_source=0&friend_source=0; toUrl=https%3A%2F%2Fwww.zhipin.com%2F%2Fjob_detail%2F3f35305467e161991nJ429i4GA%7E%7E.html; __a=43955211.1592469667..1592469667.41.1.41.41; __zp_stoken__=7f3aaPCVBFktLc1t4VTp%2BJSFCLWJscnlxSgw4bVJkRw9tLB4pb2NmWjVwdwwgc2l7HmN%2BJB0hX1UvGFZVTH0OdhQQfwxfOyoieW8cOgtKR3ZFBAJYRFMcByVndHwXTwN%2FXFo7W2BffFxtXSU%3D; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1592530497; __zp_sseed__=Ykg0aQ3ow1dZqyi9KmeVnSZKsrhFUU/CYntJcRoFki4=; __zp_sname__=93bf4835; __zp_sts__=1592530514188'
            html = self.get_url_html(boss_url, cookie_val)
            soup = BeautifulSoup(html, 'html.parser')
            # 招聘职位列表
            job_list = soup.select('.job-list ul li')
            for job_li in job_list:
                # 单条职位信息
                url = self.domain + job_li.select('.job-title a')[0].attrs['href']
                title = job_li.select('.job-title a')[0].get_text()
                area = job_li.select('.job-title .job-area')[0].get_text()
                salary = job_li.select('.job-limit .red')[0].get_text()
                year = job_li.select('.job-limit p')[0].get_text()
                company = job_li.select('.info-company h3')[0].get_text()
                industry = job_li.select('.info-company p')[0].get_text()
                info = {
                    'title': title,
                    'area': area,
                    'salary': salary,
                    'year': year,
                    'company': company,
                    'industry': industry,
                    'url': url
                }
                print(info)
                # 写入职位信息
                info_demo = '\n| %s | %s | %s | %s | %s | %s | %s |'
                dict_file.write(info_demo % (title, area, salary, year, company, industry, url))
        dict_file.close()


# 程序主入口
if __name__ == '__main__':
    # 实例化
    job_name = input('请输入职位关键字：').strip()
    if job_name == '':
        print('关键字为空，请重新尝试')
        exit(0)
    gl = GetBossData(job_name)
    # 执行脚本
    gl.run()
```

### 最后

![](https://image-static.segmentfault.com/160/802/1608021049-5ef2f75cf209a_articlex)

如果大家有任何问题，都可以留言给我，大家相互学习……

希望所有正在找工作的小伙伴们都能马上收到满意的Offer，多薪少活那种！

哦对了，在线求职，本人在深圳拍(P)簧(H)片(P)，如果大家觉得有适合我的工作，可以推荐给我的，不胜感谢。