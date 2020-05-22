---
title: 【四】PHP实用自定义函数-校验篇
date: 2020-05-22 14:57:26
tags: [PHP, 函数]
---

![](https://image-static.segmentfault.com/341/275/3412751768-5ec76cab48e7f_articlex)

### 前言

这篇文章的自定义函数，主要说关于常见的数据校验的问题，有句话怎么说来着：“很多事不问对错，但求无愧于心。”，这句话也许在其他方面可行，但是对于我们开发过程中，是肯定不能这么干的，必须有严格的校验规则，否则就很容易出问题。

好了，就不虾扯蛋了，直接说正事，我后续会陆续写一些PHP开发中实用的一些自定义函数，方便用到的朋友，能够快速开发和使用。

<!--more-->

### 校验是否为合法格式的手机号

我们都知道，手机号是11位数字，都是1开头，比如我的手机号码是`19988886666`，最基础的可以直接校验1开头的11位数字，那么正则表达式为`/^1\d{10}$/`，这样的话，任何1开头的11位数字都能够校验通过，这是最简单的，当然，这种粗活，我们肯定不能干，必须得把活干细致了，马上安排……

```php
/**
 * 校验是否为合法格式的手机号
 * @param string $mobile 手机号码
 * @return bool
 */
function check_mobile($mobile = '')
{
    // 非数字直接false
    if (!is_numeric($mobile)) {
        return false;
    }
    $pattern = '/^13[\d]{9}$|^14[5,7]{1}\d{8}$|^15[^4]{1}\d{8}$|^17[0,6,3,7,8]{1}\d{8}$|^18[\d]{9}$|^19[9]{1}\d{8}$/';
    $res = preg_match($pattern, $mobile) ? true : false;
    return $res;
}
```

### 校验是否为合法格式的邮箱

邮箱，也是常作为标识用户的信息，因为一个邮箱号码，都是唯一属于一个人的，当需要手机用户的邮箱号码的时候，就需要校验用户输入的是否是正确格式的邮箱，否则就容易闹笑话或者出错，比如你本来想要一个邮箱，结果人家给了你一个QQ号，完全对不上啊，这不就尴尬了吗，所以，必须严格校验，不符合规则的一律不接收，必须做一个有原则的人，你懂的……

```php
/**
 * 校验是否为合法格式的邮箱
 * @param string $email 邮箱
 * @return bool
 */
function check_email($email = '')
{
    $pattern = '/([\w\-]+\@[\w\-]+\.[\w\-]+)/';
    $res = preg_match($pattern, $email) ? true : false;
    return $res;
}
```

### 校验是否为合法格式的电话号码

现在手机流行的年代，固话已经很少了，基本都是公司或者单位用，那么固话的格式又是怎么样的呢，一般分为`[区号]-[号码]`，区号一般为3-4个数字，第一位都是0，比如北京的区号是`010`，而深圳的区号是`0755`,那么号码一般也是7-8位数字，比如深圳某房地产开发商电话为`88886666`，那么实际电话号码就是`0755-88886666`，这就好办了。

```php
/**
 * 校验是否为合法格式的电话号码
 * @param string $telephone 电话号码
 * @return bool
 */
function check_telephone($telephone = '')
{
    $pattern = '/^(0[0-9]{2,3})?[-]?\d{7,8}$/';
    $res = preg_match($pattern, $telephone) ? true : false;
    return $res;
}
```

### 校验是否为合法的邮政编码

上面刚说了区号，怎么能忘了邮政编码呢，比如：广东省深圳市福田区邮编是`518000`，而全国邮政编码都是6位数字，那就简单了，话不多说，直接开干……

```php
/**
 * 校验是否为合法的邮政编码
 * @param string $code 邮政编码
 * @return bool
 */
function check_post_code($code = '')
{
    $pattern = '/\d{6}/';
    $res = preg_match($pattern, $code) ? true : false;
    return $res;
}
```

### 校验是否为合法的IP地址

IP地址作为标识一台电脑的地址，比如局域网内，分配给你的IP地址可能是`192.168.1.20`，而每台机器或者设备，都会有一个IP地址，通过这个实际的IP地址，能够查到地址定位信息，很多公安办案，就是这么来的，只要绑定了你的IP地址，就能够定位并且实施抓捕工作的；有点扯远了，IP地址的格式都是四段数字，通过三个点`.`来连接，具体的校验方法如下：

```php
/**
 *  校验是否为合法的IP地址
 * @param string $ip IP地址
 * @return bool
 */
function check_ip($ip = '')
{
    $pattern = '/^(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])$/';
    $res = preg_match($pattern, $ip) ? true : false;
    return $res;
}
```

### 校验是否为合法的身份证号

我们现在的身份证号，都是18位的，以前15位的，我就说了，大家开发过程中有这需求的话，可以单独网上查资料看一下，话不多说，直接coding……

```php
/**
 * 校验是否为合法的身份证号
 * @param string $id_card 身份证号
 * @return bool
 */
function check_id_card($id_card = '')
{
    $pattern = '/^\d{6}((1[89])|(2\d))\d{2}((0\d)|(1[0-2]))((3[01])|([0-2]\d))\d{3}(\d|X)$/i';
    $res = preg_match($pattern, $id_card) ? true : false;
    return $res;
}
```

### 校验指定范围长度的字符串名称

经常在表单录入的时候，需要录入例如用户名称、信息介绍等字符串类的文字说明，一般都是限制输入多少个字符的，有可能是中文，有可能是英文，也有可能是中英文混合的那种，我是个善良的人，当然替大家考虑到位了，伺候舒服了才行。

```php
/**
 * 校验指定范围长度的字符串名称
 * @param string $name 名称
 * @param int $min 最小长度
 * @param int $max 最大长度
 * @param string $char 字符串类型：EN英文，CN中文，ALL全部字符
 * @return bool
 */
function check_name($name = '', $min = 2, $max = 20, $char = 'ALL')
{
    switch ($char) {
        case 'EN':
            $pattern = '/^[a-zA-Z]{' . $min . ',' . $max . '}$/iu';
            break;
        case 'CN':
            $pattern = '/^[_\x{4e00}-\x{9fa5}]{' . $min . ',' . $max . '}$/iu';
            break;
        default:
            $pattern = '/^[_\w\d\x{4e00}-\x{9fa5}]{' . $min . ',' . $max . '}$/iu';
    }
    $res = preg_match($pattern, $name) ? true : false;
    return $res;
}
```

### 校验是否为合法格式的日期

所谓的日期，通常来说都是指的`年-月-日`，比如，我要获取当前时间的年月日，可以通过`date('Y-m-d', time())`拿到，如果这个日期是外部其他用户传入的值呢，你怎么知道他是否会老老实实的传递一个年月日的合法数据给你呢，也许他传递给你个`2020-99-80`，你看看这个日期，是不是很别扭很吓人，所以，有必要的时候，还是要校验一下日期的合理性。

```php
/**
 * 校验是否为合法格式的日期
 * @param string $date 日期
 * @param string $sep 分隔符，默认为横线-
 * @return bool
 */
function check_date($date = '', $sep = '-')
{
    $date_arr = explode($sep, $date);
    $res = false;
    // 校验日期是否为合法数字
    if (count($date_arr) == 3 && is_numeric($date_arr[0]) && is_numeric($date_arr[1]) && is_numeric($date_arr[2])) {
        $res = checkdate($date_arr[1], $date_arr[2], $date_arr[0]);
    }
    return $res;
}
```

### 校验是否为合法格式的时间

校验完了日期，肯定不会落下时间啊，时间即`时:分:秒`，我就不多BB了，免得被嫌弃，直接安排就完事。

```php
/**
 * 校验是否为合法格式的时间
 * @param string $time 时分秒时间
 * @param string $sep 分隔符，默认为冒号:
 * @return bool
 */
function check_time($time = '', $sep = ":")
{
    $time_arr = explode($sep, $time);
    $res = false;
    // 校验时间的时分秒是否在合理范围内
    if (count($time_arr) == 3 && is_numeric($time_arr[0]) && is_numeric($time_arr[1]) && is_numeric($time_arr[2])) {
        if (($time_arr[0] >= 0 && $time_arr[0] <= 23) && ($time_arr[1] >= 0 && $time_arr[1] <= 59) && ($time_arr[2] >= 0 && $time_arr[2] <= 59)) {
            $res = true;
        }
    }
    return $res;
}
```

### 自定义函数源码

为了方便，我把我整理的全部自定义函数，都放到一个文件中，并且上传到同性交友网站GitHub上了，方便交流和使用，也方便大家帮我排错，需要的同学自取即可，我会不定时更新，地址如下：

函数源码地址：[https://github.com/gxcuizy/Blog/blob/master/code/common.php](https://github.com/gxcuizy/Blog/blob/master/code/common.php)

### 最后

我后续会慢慢更新其他的实用自定义函数，如果大家有其他好玩的、好用的欢迎分享出来，大家一起学习和交流。对了，如果有说的不对的或者错误的地方，请大家指出来，我会努力改进，谢谢。