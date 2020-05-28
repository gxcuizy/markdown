---
title: 【完整版】在Windows系统上安装Cygwin搭建Swoole测试环境
date: 2020-05-28 09:56:08
tags: [PHP, Swoole, Cygwin]
---

![](https://image-static.segmentfault.com/250/045/2500453365-5ecf1d31a1550_articlex)

### 前言

昨天，在本地安装`Swoole`调试环境的时候，遇到好几个坑，因为我的电脑是`Windows`系统，所以安装的是`cygwin`，但是过程并不顺利，接连出现安装终端的问题，并一步步查资料排坑，最终也顺利安装成功了，为了让其他人也能一次性就安装成功，省掉很多麻烦闹心事，我特地写了这边文章，希望对有需要的人有所帮助。

### 下载Swoole

Swoole下载地址：[https://github.com/swoole/swoole-src/releases](https://github.com/swoole/swoole-src/releases)

<!--more-->

![](https://image-static.segmentfault.com/114/161/1141615996-5ece24cbb3990_articlex)

在浏览器中打开下载地址，滑动到下载位置，可以下载`zip`文件包或者`tar.gz`文件包，下载完成等着后面备用。

### 下载cygwin

cygwin下载地址：[https://www.cygwin.com/](https://www.cygwin.com/)

![](https://image-static.segmentfault.com/261/448/2614483268-5ece254f6eefc_articlex)

在浏览器中打开`cygwin`官网，下滑到`Installing Cygwin`部分，点击`setup-x86_64.exe`下载`exe`文件即可

### 安装cygwin

找到刚才下载的`setup-x86_64.exe`文件，双击打开，就开始安装cygwin

* 第一步：打开安装界面，直接点击下一步

![](https://image-static.segmentfault.com/251/387/2513874148-5ece26ac45f2a_articlex)


* 第二步：选择下载源，我们直接默认选择`Install from Internet`，然后点击下一步

![](https://image-static.segmentfault.com/185/933/1859332603-5ece2717719ac_articlex)

* 第三步：选择安装目录，可以在输入框中直接修改安装目录，或者点击`Browse`选择目录，点击下一步

![](https://image-static.segmentfault.com/511/612/511612212-5ece27d10dc34_articlex)

* 第四步：选择包下载的目录，可以在输入框中直接修改目录，或者点击`Browse`选择目录，点击下一步

![](https://image-static.segmentfault.com/124/955/1249553303-5ece28347bbf9_articlex)

* 第五步：选择网络服务器，直接默认就行了，点击继续下一步

![](https://image-static.segmentfault.com/388/344/3883441440-5ece28be5c566_articlex)

* 第六步：选择一个下载服务器网址，我们选择`http://mirrors.metapeer.com`，在这里，我们也可以自己添加163的下载服务器，地址为`http://mirrors.163.com/cygwin/`，选定继续下一步

![](https://image-static.segmentfault.com/232/577/232577193-5ece295ac415e_articlex)

* 第七步：选择需要安装的软件包界面，`View`下拉选择`Category`选项

![](https://image-static.segmentfault.com/215/182/2151824634-5ece2c195f8c3_articlex)

* 第八步：搜索并选择需要安装的软件包

gcc-core，在`Search`中搜索`gcc-core`，展开`Devel`，找到下图中的蓝色选中项，在`New`栏，双击选择即可

![](https://image-static.segmentfault.com/346/735/346735380-5ece2d250f771_articlex)

php和php-devel，在`Search`中搜索`php`，展开`Interpreters`，找到下图中的蓝色选中项，在`New`栏，双击选择即可，切记`php`和`php-devel`两项都要选择

![](https://image-static.segmentfault.com/223/758/2237586392-5ece2ec0ee72b_articlex)

libpcre-devel，在`Search`中搜索`libpcre-devel`，展开`Libs`，找到下图中的蓝色选中项，在`New`栏，双击选择即可

![](https://image-static.segmentfault.com/357/754/3577547791-5ece30e05878c_articlex)

autoconf-archive，在`Search`中搜索`autoconf-archive`，展开`Devel`，找到下图中的蓝色选中项，在`New`栏，双击选择即可

![](https://image-static.segmentfault.com/287/332/2873325843-5ece30915f2f3_articlex)

gcc-objc++，在`Search`中搜索`gcc-objc++`，展开`Devel`，找到下图中的蓝色选中项，在`New`栏，双击选择即可

![](https://image-static.segmentfault.com/369/961/3699611256-5ece313e71c1b_articlex)

libc++-devel，在`Search`中搜索`libc++-devel`，展开`Devel`，找到下图中的蓝色选中项，在`New`栏，双击选择即可

![](https://image-static.segmentfault.com/388/483/3884839399-5ece31d25e1f8_articlex)

libc++1，在`Search`中搜索`libc++1`，展开`Devel`，找到下图中的蓝色选中项，在`New`栏，双击选择即可

![](https://image-static.segmentfault.com/171/121/1711215636-5ece325beca06_articlex)

php-json，在`Search`中搜索`php-json`，展开`PHP`，找到下图中的蓝色选中项，在`New`栏，双击选择即可

![](https://image-static.segmentfault.com/105/041/1050417720-5ece329c0726d_articlex)

pcre2，在`Search`中搜索`pcre2`，展开`Text`，找到下图中的蓝色选中项，在`New`栏，双击选择即可

![](https://image-static.segmentfault.com/328/246/3282466629-5ece3505b23b7_articlex)

libpcre2-devel，在`Search`中搜索`libpcre2-devel`，展开`Libs`，找到下图中的蓝色选中项，在`New`栏，双击选择即可

![](https://image-static.segmentfault.com/390/744/3907447418-5ece33393b1a1_articlex)

* 最后一步，选择完全部的软件包，点击下一步，直到安装完成，时间可能有点久，耐心等一下

![](https://image-static.segmentfault.com/378/566/3785662233-5ece357372ebd_articlex)

### 编译安装Swoole

* 解压并放到home目录

解压上面下载的`Swoole`压缩包，放到`cygwin`的安装目录下的`home`目录中，为了方便，并改名为`Swoole`，当然可以不改

![](https://image-static.segmentfault.com/759/821/759821391-5ece365fb3e45_articlex)

*  打开cygwin并且进入Swoole目录

双击运行Cygwin软件，然后通过命令`cd /home/swool/`，进入`Swoole`解压的源程序代码

![](https://image-static.segmentfault.com/231/656/2316566083-5ece388f00fc4_articlex)

* 生成编译的配置文件

在`Swoole`的根目录下，执行命令`phpize`，可以生成编译的配置文件configure

![](https://image-static.segmentfault.com/385/623/3856230176-5ece3a1b5effd_articlex)

* 编译配置并检测环境且编译安装

上面生成编译的配置文件后，再输入命令`./configure && make && make install`，然后就是等待编译安装`Swoole`完成

![](https://image-static.segmentfault.com/370/054/3700541166-5ecf102faffcf_articlex)

### 检测Swoole安装是否成功

* 查看Swoole扩展是否开启

安装完成后，我们输入命令`php --ini`，可以查找到`php.ini`配置文件的目录位置，可以发现，配置文件的目录在`/etc/php.ini`，然后通过`vi`编辑查看命令`vi /etc/php.ini`，并且进入到文件的最后一行，然后发现，已经有了一行`extension=swoole.dll`的扩展配置，这是因为在编译安装的时候，已经把这个模块编译进了`php`。

![](https://image-static.segmentfault.com/409/346/4093461782-5ecf121983431_articlex)

然后我们再通过命令`php -m`查看一下是否真的有这个扩展了呢，从下图可以发现，确实已经有了`swoole`的扩展

![](https://image-static.segmentfault.com/269/446/2694463883-5ecf1340b2d8d_articlex)

### 测试Swoole环境

* 选择并进入测试目录

在我们下载的`Swoole`源代码中，有很多示例，我们可以直接运行进行测试，进入到`examples`目录，里面的全都是示例代码，我们选择`http/server.php`进行测试，然后`cd http/`进入到`http`目录

![](https://image-static.segmentfault.com/183/507/1835071155-5ecf14e6a7a00_articlex)

* 执行php程序

上面已经进入到`http`目录，并且发现，当前目录下有一个`server.php`的文件，我们可以通过命令`php server.php`执行

![](https://image-static.segmentfault.com/158/032/1580328822-5ecf160775578_articlex)

* 浏览器运行测试

我们打开`server.php`文件，有一行代码`$http = new swoole_http_server("0.0.0.0", 9501);`，开启`swoole`服务的端口为`9501`，那么我们可以直接在浏览器地址栏输入`127.0.0.1:9501`或者`localhost:9501`并访问，显示`Hello Swoole.`，则说明`Swoole`安装成功了！

![](https://image-static.segmentfault.com/398/139/3981397264-5ecf1726287b3_articlex)

### 总结

只要按照文章一步一步的安装，应该能一次性安装成功，因为我是一步一个坑踩过来的，并且已经把坑填上了，不要夸我，会骄傲的。大家在安装过程中，如有任何问题可以直接留言给我，我看到会及时回复并帮助解决的，大家如果有其他更好的想法，也环境分析出来和大家交流，谢谢！