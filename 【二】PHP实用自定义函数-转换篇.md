---
title: 【二】PHP实用自定义函数-转换篇
date: 2020-05-15 11:20:52
tags: [PHP, 函数]
---

![](https://image-static.segmentfault.com/186/012/1860120273-5ebe0bccde575_articlex)

### 前言

这篇文章的自定义函数，主要说一些数据转换的，就不虾扯蛋了，直接说正事，我后续会陆续写一些PHP开发中实用的一些自定义函数，方便用到的朋友，能够快速开发和使用。

<!--more-->

### 将xml格式转换为数组

在我们请求一些第三方接口的时候，要么返回给你json类型的数据格式，要么就是xml或者其他的，如果是json的话，很方便能直接使用，当遇到xml格式的时候，就需要转换为数组格式的，方便使用。

```php
/**
 * 将xml格式转换为数组
 * @param string $xml xml字符串
 * @return mixed
 */
function xml_to_array($xml = '')
{
    // 利用函数simplexml_load_string()把xml字符串载入对象中
    $obj = simplexml_load_string($xml, 'SimpleXMLElement', LIBXML_NOCDATA);
    // 编码对象后，再解码即可得到数组
    $arr = json_decode(json_encode($obj), true);
    return $arr;
}
```

### 隐藏手机号中间四位数

通常，为了安全和保护用户隐私，用户手机号等关键信息，是不能完全暴露在界面上公开显示的，就需要处理一下，比如通常是隐藏中间四位数……

```php
/**
 * 隐藏手机号中间四位数为****
 * @param string $mobile 正常手机号
 * @return mixed
 */
function replace_phone($mobile = '')
{
    $new_mobile = substr_replace($mobile, '****', 3, 4);
    return $new_mobile;
}
```

### 最简单的API请求通用返回数据格式

这里，我就最简单的说明一下，一般API请求，最基础要求返回的数据格式，通常呢，可以细分为成功返回和失败返回，大家可以根据实际情况处理，在很多框架中，都有直接封装好的方法，大家也可以去看看框架里是怎么处理的。

```php
/**
 * 最简单的Ajax请求返回数据格式
 * @param string $msg 返回提示信息
 * @param int $code 返回标识符号
 * @param array $data 返回数据
 */
function ajax_return($msg = '', $code = 0, $data = [])
{
    $return['code'] = $code;
    $return['msg'] = $msg;
    $return['data'] = $data;
    exit(json_encode($return, JSON_UNESCAPED_UNICODE));
}
```

### 截取字符串

通常，在一些列表或者固定范围内，显示一定长度的字符串的时候，如果我们不控制范围的话，很可能会导致超出界面显示，或者溢出显示，导致页面布局不美观等，这个时候，就需要我们控制显示字符串的长度，超出部分截取掉……

```php
/**
 * 截取字符串，超出部分用省略符号显示
 * @param string $text 待截取字符串
 * @param int $length 截取长度，默认全部截取
 * @param string $rep 截取超出替换的字符串，默认为省略号
 * @return string
 */
function cut_string($text = '', $length = 0, $rep = '…')
{
    if (!empty($length) && mb_strlen($text, 'utf8') > $length) {
        $text = mb_substr($text, 0, $length, 'utf8') . $rep;
    }
    return $text;
}
```

### 根据生日计算年龄

在一些论坛或者交友类平台中，经常会看到，某某年龄18岁，如果当你遇到这类开发需求的时候，是不是也得处理一下，我是个善良的开发者嘛，这种事情，我肯定帮想到了，让我来就行了，安排上，已经写好了，可以直接拿来用。

```php
/**
 * 根据生日计算年龄
 * @param string $date 生日的年月日
 * @return int
 */
function get_age($date = '')
{
    $age = 0;
    $time = strtotime($date);
    // 日期非法，则不处理
    if (!$time) {
        return $age;
    }
    // 计算时间年月日差
    $date = date('Y-m-d', $time);
    list($year, $month, $day) = explode("-", $date);
    $age = date("Y", time()) - $year;
    $diff_month = date("m") - $month;
    $diff_day = date("d") - $day;
    // 不满周岁年龄减1
    if ($age < 0 || $diff_month < 0 || $diff_day < 0) {
        $age--;
    }
    return $age;
}
```

### 日期时间显示格式转换

最常见的，我们每天刷微信朋友圈的生活，左下角的那个时间，比如：10分钟前、2小时前、昨天等，你是否也遇到过这类的时间显示转换的需求，这类开发需求找我啊，我都给安排好了，拿来即用的那种哦……

```php
/**
 * 日期时间显示格式转换
 * @param int $time 时间戳
 * @return bool|string
 */
function transfer_show_time($time = 0)
{
    // 时间显示格式
    $day_time = date("m-d H:i", $time);
    $hour_time = date("H:i", $time);
    // 时间差
    $diff_time = time() - $time;
    $date = $day_time;
    if ($diff_time < 60) {
        $date = '刚刚';
    } else if ($diff_time < 60 * 60) {
        $min = floor($diff_time / 60);
        $date = $min . '分钟前';
    } else if ($diff_time < 60 * 60 * 24) {
        $h = floor($diff_time / (60 * 60));
        $date = $h . '小时前 ' . $hour_time;
    } else if ($diff_time < 60 * 60 * 24 * 3) {
        $day = floor($diff_time / (60 * 60 * 24));
        if ($day == 1) {
            $date = '昨天 ' . $day_time;
        } else {
            $date = '前天 ' . $day_time;
        }
    }
    return $date;
}
```

### 获取毫秒数

日常开发中，我们一般都是通过`time()`直接获取时间戳秒数，很少会遇到获取毫秒数的需求，但是呢，有备无患，万一啥时候一个坑比需求有这个要求呢，那怎么也得满足吧，作为一个职业的开发者，一般都是有求必应的……

```php
/**
 * 获取毫秒数
 * @return string
 */
function get_millisecond()
{
    list($t1, $t2) = explode(' ', microtime());
    $ms = sprintf('%.0f', (floatval($t1) + floatval($t2)) * 1000);
    return $ms;
}
```

### CURL请求之GET方式

通常，我们都会遇到需要请求第三方接口的，而且一般也都会封装自己的接口请求方法，大同小异，这是最基础的GET请求封装

```php
/**
 * CURL请求之GET方式
 * @param string $url 请求接口地址
 * @return bool|mixed
 */
function curl_get($url = '')
{
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    // 不验证SSL证书。
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    $res = curl_exec($ch);
    curl_close($ch);
    return $res;
}
```

### CURL请求之POST方式

很多第三方接口，一般都是POST方式的比较多，所以，我也给大家封装了一个基础的请求方法，大家可以根据自己的实际情况，进行修改和完善。

```php
/**
 * CURL请求之POST方式
 * @param string $url 请求接口地址
 * @param array $data 请求参数
 * @param int $timeout 超时时间
 * @return mixed
 */
function curl_post($url = '', $data = [], $timeout = 3000)
{
    $post_data = http_build_query($data, '', '&');
    header("Content-type:text/html;charset=utf-8");
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, $timeout);
    curl_setopt($ch, CURLOPT_HEADER, false);
    $res = curl_exec($ch);
    curl_close($ch);
    return $res;
}
```

### 最后

我后续会慢慢更新其他的实用函数，如果大家有其他好玩的、好用的欢迎分享出来，大家一起学习和交流。对了，如果有说的不对的或者错误的地方，请大家指出来，我会努力改进，谢谢。