---
title: 【五】PHP实用自定义函数-功能篇
date: 2020-05-26 13:45:51
tags: [PHP, 函数]
---

![](https://image-static.segmentfault.com/148/898/1488986830-5eccae75463ca_articlex)

### 前言

这篇文章的自定义函数，主要说几个功能篇的函数，比较实用，再次申明一下，这些函数，每个我都是自己亲自执行并且测过过了的，所以，不会存在那种执行会报错的情况。

好了，就不虾扯蛋了，直接说正事，我后续会陆续写一些PHP开发中实用的一些自定义函数，方便用到的朋友，能够快速开发和使用。

<!--more-->

### 获取指定长度的随机字符串

我相信，我们都遇到过那种生成指定长度的随机字符串的需求，比如：登录密码校验的密码盐、给用户随机生成的密码以及用户昵称等等，虽然可能会有一些自己的规则在里面，但是大概思路基本都差不多，大同小异。

```php
/**
 * 获取指定长度的随机字符串
 * @param int $length 随机字符串的长度
 * @return string
 */
function get_random_str($length = 9)
{
    // 字符串集合，全部大小写字母和数字
    $chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    $str = '';
    // 循环多次，随机逐次获取
    for ($i = 0; $i < $length; $i++) {
        $str .= $chars[mt_rand(0, strlen($chars) - 1)];
    }
    return $str;
}
```

### 统计文章中文字和图片的数量

一篇文章，主要就是文字和图片组成的，当然了还有一些表单符号啥的，如果全都是文字，感觉有点太枯燥了，所以，好多文章都强调要图文并茂，那么，到了这，你是否有种要统计一篇文章有多少张图片和多少个文字的冲动呢，别撒谎老实说，你肯定有的，那么该怎么统计呢，自然有个热心的网友来帮你的了，看下面，当当当当……

```php
/**
 * 统计文章中文字和图片的数量
 * @param string $html 文章html字符串
 * @return array
 */
function count_word_img($html = '')
{
    // 匹配img标签的数量
    preg_match_all('/<img /i', $html, $match_arr);
    $img_count = count($match_arr[0]);
    // 统计非img标签的数量，可根据实际情况进行调整表达式
    $pattern = '/\[#img_[0-9]+_[a-z]*_[0-9]+_[a-zA-Z]*/i';
    preg_match_all($pattern, $html, $match_arr);
    $img_count += count($match_arr[0]);
    // 去掉图片img标签
    $html = preg_replace("/<img([^>].+)>/iU", "", $html);
    // 去掉非标签的图片
    $html = preg_replace($pattern, "", $html);
    // 去掉全部空格
    $html = str_replace(' ', '', $html);
    // 先去除HTML和PHP标记，再统计字数
    $word_count = mb_strlen(trim(strip_tags($html)), 'UTF-8');
    return ['word_count' => $word_count, 'img_count' => $img_count];
}
```

### 格式化打印输出内容

在我们日常开发和调试的过程中，你是否希望能有一个函数，能让你快速的打印出数据，很多框架都封装有这些辅助函数，比如`ThinkPHP5`框架中有`dump()`和`halt()`，`Laravel`框架中也有`dump()`和`dd()`等，但是，如果遇到没有这类辅助函数的时候，你应该怎么办呢，可能有的开发者的打印调试是这样的：`print_r($a);die();`或者`echo '<pre>';print_r($a);exit();`，有的时候，调试完毕了，还是直接就注释掉而并没有直接删除，这种习惯可不好；继续，遇到框架中没有或者自己不爽框架的函数的时候，你是不是想着，自己手撸一个呢，那必须的嘛，马上动手安排……

```php
/**
 * 格式化打印输出内容
 * @param void $data 需要打印的内容
 * @param bool $exit
 */
function dump_plus($data, $exit = true)
{
    // 自定义样式，方便美观查看
    $output = '<pre style="display: block;background-color: #f5f5f5;border: 1px solid #cccccc;padding: 10px;margin: 45px 0 0 0;font-size: 13px;line-height: 1.5;border-radius: 4px;">';
    // boolean或者null类型直接文字输出，其他print_r格式化输出
    if (is_bool($data)) {
        $show = $data ? 'true' : 'false';
    } else if (is_null($data)) {
        $show = 'null';
    } else {
        $show = var_export($data, true);
    }
    // 拼接文本输出
    $output .= $show;
    $output .= '</pre>';
    echo $output;
    // 是否中断执行
    if ($exit) {
        exit();
    }
}
```

### 通过IP地址获取位置信息

说到这个，大家先来看看下面的这一张图：

![](https://tool.lu/netcard/)

图片上竟然可以定位显示出你的位置，是不是会感觉到很神奇呢，别惊讶，在万能的程序员小哥眼里，啥都不是事，要有，那就是给他介绍个对象，实在不行，再请他撸个铁啥的（这个铁是烤肉串哈，别搞错把事办砸了）……

```php
/**
 * 通过IP地址获取位置信息
 * markdown快速使用 
 * @param string $ip IP地址
 * @return mixed
 */
function get_ip_info($ip = '')
{
    $api = 'http://www.geoplugin.net/json.gp?ip=';
    $res_data = file_get_contents($api . $ip);
    $res = json_decode($res_data, true);
    $data = [];
    if ($res['geoplugin_status'] == '200') {
        // 国家
        $data['country'] = $res['geoplugin_countryName'];
        // 省份
        $data['province'] = $res['geoplugin_regionName'];
        // 城市
        $data['city'] = $res['geoplugin_city'];
        // 经度
        $data['latitude'] = $res['geoplugin_latitude'];
        // 纬度
        $data['longitude'] = $res['geoplugin_longitude'];
        // 其他值，根据需要自定义
    }
    return $data;
}
```

### 发红包，金额随机

逢年过节的，在微信群里各种红包，你发了多少，你又抢了多少呢，一般群里的红包，都是拼手气的红包，作为一个程序员小哥哥小姐姐，是否甘心只抢红包而不想一下这个红包是怎么肥四的吗？我知道，你肯定有想的，只不过抢红包太忙了，没顾得过来而已，大家都懂的，那这种粗活，还是让我来就好了。

```php
/**
 * 发红包，金额随机
 * @param int $total 红包金额
 * @param int $num 红包个数
 * @param float $min 红包最小金额
 * @@return array
 */
function get_red_packet($total = 0, $num = 1, $min = 0.01)
{
    $data = [];
    for ($i = 1; $i < $num; $i++) {
        // 随机金额安全上限控制
        $safe_total = ($total - ($num - $i) * $min) / ($num - $i);
        $money = mt_rand($min * 100, $safe_total * 100) / 100;
        $total -= $money;
        // sort为领取顺序，money为红包金额，balance为领取后的余额
        $data[] = [
            'sort' => $i,
            'money' => $money,
            'balance' => $total
        ];
    }
    // 最后一个红包
    $data[] = [
        'sort' => $num,
        'money' => $total,
        'balance' => 0
    ];
    return $data;
}
```

### 获取文字的首字母

获取文字的首字母，一般什么情况下会遇到这种需求呢，我之前做过一个需求，就是城市名称定位，直接根据首字母定位到所有以这个首字母开头的城市，节省了很大的搜索时间，我们的手机通讯录，也是有这个搜索的，大家可以看一下，那么这类是怎么获取首字母的呢，我们一起来讨论一下吧……

```php
/**
 * 获取文字的首字母
 * @param string $str 文字字符串
 * @return string
 */
function get_first_char($str = '')
{
    $first_char = $str[0];
    // 判断是否为字符串
    if (ord($first_char) >= ord("A") && ord($first_char) <= ord("z")) {
        return strtoupper($first_char);
    }
    $str = iconv("UTF-8", "gb2312", $str);
    $asc = ord($str[0]) * 256 + ord($str[1]) - 65536;
    $first_char = '';
    if ($asc >= -20319 and $asc <= -20284) $first_char = "A";
    else if ($asc >= -20283 and $asc <= -19776) $first_char = "B";
    else if ($asc >= -19775 and $asc <= -19219) $first_char = "C";
    else if ($asc >= -19218 and $asc <= -18711) $first_char = "D";
    else if ($asc >= -18710 and $asc <= -18527) $first_char = "E";
    else if ($asc >= -18526 and $asc <= -18240) $first_char = "F";
    else if ($asc >= -18239 and $asc <= -17923) $first_char = "G";
    else if ($asc >= -17922 and $asc <= -17418) $first_char = "H";
    else if ($asc >= -17417 and $asc <= -16475) $first_char = "J";
    else if ($asc >= -16474 and $asc <= -16213) $first_char = "K";
    else if ($asc >= -16212 and $asc <= -15641) $first_char = "L";
    else if ($asc >= -15640 and $asc <= -15166) $first_char = "M";
    else if ($asc >= -15165 and $asc <= -14923) $first_char = "N";
    else if ($asc >= -14922 and $asc <= -14915) $first_char = "O";
    else if ($asc >= -14914 and $asc <= -14631) $first_char = "P";
    else if ($asc >= -14630 and $asc <= -14150) $first_char = "Q";
    else if ($asc >= -14149 and $asc <= -14091) $first_char = "R";
    else if ($asc >= -14090 and $asc <= -13319) $first_char = "S";
    else if ($asc >= -13318 and $asc <= -12839) $first_char = "T";
    else if ($asc >= -12838 and $asc <= -12557) $first_char = "W";
    else if ($asc >= -12556 and $asc <= -11848) $first_char = "X";
    else if ($asc >= -11847 and $asc <= -11056) $first_char = "Y";
    else if ($asc >= -11055 and $asc <= -10247) $first_char = "Z";
    return $first_char;
}
```

### 删除指定目录下的文件夹和文件

有一天，领导给你一个小任务，说让你写一个定时任务，在固定时间清除一下某个文件夹下的全部文件和空文件夹，这种小需求，对于你来说当然是洒洒水啦，但是呢，此时此刻，你正在陪女票聊天，正火热那种，超过一分钟不回信息回家就要跪键盘那种，哪里走得开去分心干这些小事啊，不过呢，幸好有我在，这种小事，我肯定帮你做好了，你拿去就可以交差了。

```php
/**
 * 删除指定目录下的文件夹和文件
 * @param string $path 目录路径
 */
function delete_dir($path = '')
{
    // 为空默认当前目录
    if ($path == '') {
        $path = realpath('.');
    }
    // 判断目录是否存在
    if (!is_dir($path)) {
        exit('目录【' . $path . '】不存在');
    }
    // 删除path目录最后的/
    if (substr($path, -1, 1) == '/') {
        $path = substr_replace($path, '', -1, 1);
    }
    // 扫描一个文件夹内的所有文件夹和文件
    $file_arr = scandir($path);
    foreach ($file_arr as $file) {
        // 排除当前目录.与父级目录..
        if ($file != "." && $file != "..") {
            // 如果是目录则递归子目录
            $this_file = $path . DIRECTORY_SEPARATOR . $file;
            if (is_dir($this_file)) {
                // 继续循环遍历子目录
                delete_dir($this_file);
                // 删除空文件夹
                @rmdir($this_file);
            } else if (is_file($this_file)) {
                // 文件类型直接删除
                unlink($this_file);
            }
        }
    }
}
```

### 自定义函数源码

为了方便，我把我整理的全部自定义函数，都放到一个文件中，并且上传到同性交友网站GitHub上了，方便交流和使用，也方便大家帮我排错，需要的同学自取即可，我会不定时更新，地址如下：

函数源码地址：[https://github.com/gxcuizy/Blog/blob/master/code/common.php](https://github.com/gxcuizy/Blog/blob/master/code/common.php)

### 最后

我后续会慢慢更新其他的实用自定义函数，如果大家有其他好玩的、好用的欢迎分享出来，大家一起学习和交流。对了，如果有说的不对的或者错误的地方，请大家指出来，我会努力改进，谢谢。