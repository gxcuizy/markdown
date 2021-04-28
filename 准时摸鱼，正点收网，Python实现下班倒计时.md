---
title: 准时摸鱼，正点收网，Python实现下班倒计时
date: 2021-04-27 13:33:18
tags: [Python, time, tkinter]
---

![](https://image-static.segmentfault.com/133/066/1330665599-6087ad58e3dab_fix732)

### 你有过摸鱼时间吗

在互联网圈子里，常常说996上班制，但是也不乏965的，更甚有007的，而007则就有点ICU的感觉了，所以，大家都会忙里偷闲，偶尔摸摸鱼，摸鱼的方式多种多样的，你有过上班摸鱼吗？你的摸鱼时间都干了些什么呢？如果你早早的完成了当天的任务，坐等下班的感觉是不是很爽呢？我想说这时间还是很难熬的，还不如找点事情做来得快呢，那做点什么呢？写个下班倒计时吧，就这么愉快的决定了……

### 实现思路

倒计时的时间刷新，肯定得需要图形界面，也就是需要GUI编程，这里我用的是`tkinter`实现本地窗口的界面，使用`tkinter`可以实现页面布局以及时间的定时刷新显示，而涉及到时间的操作，肯定少不了要用到`time`模块，这里我还加入了倒计时结束自动关机的功能（注释了的，有需要可以打开），所以还用到了`os`模块的`system`实现定时关机功能。

<!--more-->

### 运行环境

Python运行环境：Windows + python3.8  
用到的模块：`tkinter、time、os`  
如未安装的模块，请使用`pip instatll xxxxxx`进行安装，例如：`pip install tkinter`

### 界面布局

先来看一下实现后的界面

![](https://image-static.segmentfault.com/290/230/2902306930-6087a759b7406_fix732)

从截图中可以看到，主要有三个信息：

- 当前时间：这个是实时显示当前时间，格式为格式化的年月日时分秒
- 下班时间：这个可以修改的，默认是`18:00:00`，可以根据自己的下班时间来修改
- 剩余时间：这里是倒计时的剩余时间，点`START`后每秒刷新

```python
# 设置页面数据
tk_obj = Tk()
tk_obj.geometry('400x280')
tk_obj.resizable(0, 0)
tk_obj.config(bg='white')
tk_obj.title('倒计时应用')
Label(tk_obj, text='下班倒计时', font='宋体 20 bold', bg='white').pack()
# 设置当前时间
Label(tk_obj, font='宋体 15 bold', text='当前时间：', bg='white').place(x=50, y=60)
curr_time = Label(tk_obj, font='宋体 15', text='', fg='gray25', bg='white')
curr_time.place(x=160, y=60)
refresh_current_time()
# 设置下班时间
Label(tk_obj, font='宋体 15 bold', text='下班时间：', bg='white').place(x=50, y=110)
# 下班时间-小时
work_hour = StringVar()
Entry(tk_obj, textvariable=work_hour, width=2, font='宋体 12').place(x=160, y=115)
work_hour.set('18')
# 下班时间-分钟
work_minute = StringVar()
Entry(tk_obj, textvariable=work_minute, width=2, font='宋体 12').place(x=185, y=115)
work_minute.set('00')
# 下班时间-秒数
work_second = StringVar()
Entry(tk_obj, textvariable=work_second, width=2, font='宋体 12').place(x=210, y=115)
work_second.set('00')
# 设置剩余时间
Label(tk_obj, font='宋体 15 bold', text='剩余时间：', bg='white').place(x=50, y=160)
down_label = Label(tk_obj, font='宋体 23', text='', fg='gray25', bg='white')
down_label.place(x=160, y=155)
down_label.config(text='00时00分00秒')
# 开始计时按钮
Button(tk_obj, text='START', bd='5', command=refresh_down_time, bg='green', font='宋体 10 bold').place(x=150, y=220)
tk_obj.mainloop()
```

### 定时刷新剩余时间

通过获取设置的下班时间，对比当前时间的时间差，从而得到剩余时间，再用`while`每秒循环处理剩余时间，并实时刷新到界面上，直至剩余时间为0程序才会结束，甚至操作电脑自动关机的功能。

```python
def refresh_down_time():
    """刷新倒计时时间"""
    # 当前时间戳
    now_time = int(time.time())
    # 下班时间时分秒数据过滤
    work_hour_val = int(work_hour.get())
    if work_hour_val > 23:
        down_label.config(text='小时的区间为（00-23）')
        return
    work_minute_val = int(work_minute.get())
    if work_minute_val > 59:
        down_label.config(text='分钟的区间为（00-59）')
        return
    work_second_val = int(work_second.get())
    if work_second_val > 59:
        down_label.config(text='秒数的区间为（00-59）')
        return
    # 下班时间转为时间戳
    work_date = str(work_hour_val) + ':' + str(work_minute_val) + ':' + str(work_second_val)
    work_str_time = time.strftime('%Y-%m-%d ') + work_date
    time_array = time.strptime(work_str_time, "%Y-%m-%d %H:%M:%S")
    work_time = time.mktime(time_array)
    if now_time > work_time:
        down_label.config(text='已过下班时间')
        return
    # 距离下班时间剩余秒数
    diff_time = int(work_time - now_time)
    while diff_time > -1:
        # 获取倒计时-时分秒
        down_minute = diff_time // 60
        down_second = diff_time % 60
        down_hour = 0
        if down_minute > 60:
            down_hour = down_minute // 60
            down_minute = down_minute % 60
        # 刷新倒计时时间
        down_time = str(down_hour).zfill(2) + '时' + str(down_minute).zfill(2) + '分' + str(down_second).zfill(2) + '秒'
        down_label.config(text=down_time)
        tk_obj.update()
        time.sleep(1)
        if diff_time == 0:
            # 倒计时结束
            down_label.config(text='已到下班时间')
            # 自动关机，定时一分钟关机，可以取消
            # down_label.config(text='下一分钟将自动关机')
            # os.system('shutdown -s -f -t 60')
            break
        diff_time -= 1
```

### 完整代码

为了方便大家测试和顺利摸鱼，我把完整的倒计时程序也贴出来，大家有什么问题也可以及时反馈，想要了解更多的可以去交友网站[https://github.com/gxcuizy](https://github.com/gxcuizy/Python/tree/master/%E4%B8%8B%E7%8F%AD%E5%80%92%E8%AE%A1%E6%97%B6)上面找我哦

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
距离下班时间倒计时
author: gxcuizy
date: 2021-04-27
"""

from tkinter import *
import time
import os


def refresh_current_time():
    """刷新当前时间"""
    clock_time = time.strftime('%Y-%m-%d %H:%M:%S')
    curr_time.config(text=clock_time)
    curr_time.after(1000, refresh_current_time)


def refresh_down_time():
    """刷新倒计时时间"""
    # 当前时间戳
    now_time = int(time.time())
    # 下班时间时分秒数据过滤
    work_hour_val = int(work_hour.get())
    if work_hour_val > 23:
        down_label.config(text='小时的区间为（00-23）')
        return
    work_minute_val = int(work_minute.get())
    if work_minute_val > 59:
        down_label.config(text='分钟的区间为（00-59）')
        return
    work_second_val = int(work_second.get())
    if work_second_val > 59:
        down_label.config(text='秒数的区间为（00-59）')
        return
    # 下班时间转为时间戳
    work_date = str(work_hour_val) + ':' + str(work_minute_val) + ':' + str(work_second_val)
    work_str_time = time.strftime('%Y-%m-%d ') + work_date
    time_array = time.strptime(work_str_time, "%Y-%m-%d %H:%M:%S")
    work_time = time.mktime(time_array)
    if now_time > work_time:
        down_label.config(text='已过下班时间')
        return
    # 距离下班时间剩余秒数
    diff_time = int(work_time - now_time)
    while diff_time > -1:
        # 获取倒计时-时分秒
        down_minute = diff_time // 60
        down_second = diff_time % 60
        down_hour = 0
        if down_minute > 60:
            down_hour = down_minute // 60
            down_minute = down_minute % 60
        # 刷新倒计时时间
        down_time = str(down_hour).zfill(2) + '时' + str(down_minute).zfill(2) + '分' + str(down_second).zfill(2) + '秒'
        down_label.config(text=down_time)
        tk_obj.update()
        time.sleep(1)
        if diff_time == 0:
            # 倒计时结束
            down_label.config(text='已到下班时间')
            # 自动关机，定时一分钟关机，可以取消
            # down_label.config(text='下一分钟将自动关机')
            # os.system('shutdown -s -f -t 60')
            break
        diff_time -= 1


# 程序主入口
if __name__ == "__main__":
    # 设置页面数据
    tk_obj = Tk()
    tk_obj.geometry('400x280')
    tk_obj.resizable(0, 0)
    tk_obj.config(bg='white')
    tk_obj.title('倒计时应用')
    Label(tk_obj, text='下班倒计时', font='宋体 20 bold', bg='white').pack()
    # 设置当前时间
    Label(tk_obj, font='宋体 15 bold', text='当前时间：', bg='white').place(x=50, y=60)
    curr_time = Label(tk_obj, font='宋体 15', text='', fg='gray25', bg='white')
    curr_time.place(x=160, y=60)
    refresh_current_time()
    # 设置下班时间
    Label(tk_obj, font='宋体 15 bold', text='下班时间：', bg='white').place(x=50, y=110)
    # 下班时间-小时
    work_hour = StringVar()
    Entry(tk_obj, textvariable=work_hour, width=2, font='宋体 12').place(x=160, y=115)
    work_hour.set('18')
    # 下班时间-分钟
    work_minute = StringVar()
    Entry(tk_obj, textvariable=work_minute, width=2, font='宋体 12').place(x=185, y=115)
    work_minute.set('00')
    # 下班时间-秒数
    work_second = StringVar()
    Entry(tk_obj, textvariable=work_second, width=2, font='宋体 12').place(x=210, y=115)
    work_second.set('00')
    # 设置剩余时间
    Label(tk_obj, font='宋体 15 bold', text='剩余时间：', bg='white').place(x=50, y=160)
    down_label = Label(tk_obj, font='宋体 23', text='', fg='gray25', bg='white')
    down_label.place(x=160, y=155)
    down_label.config(text='00时00分00秒')
    # 开始计时按钮
    Button(tk_obj, text='START', bd='5', command=refresh_down_time, bg='green', font='宋体 10 bold').place(x=150, y=220)
    tk_obj.mainloop()
```

### 最后

大家有任何问题，都可以给我留言给我，我会及时回复，如有说的不对的地方，还请大家帮忙纠正。如果大家有什么好玩的摸鱼办法，也可以底部留言给我哈，大家一起愉快的摸鱼！