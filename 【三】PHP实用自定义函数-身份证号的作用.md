---
title: 【三】PHP实用自定义函数-身份证号包含的信息
date: 2020-05-19 16:25:19
tags: [PHP, 函数]
---

![](https://image-static.segmentfault.com/220/657/2206575456-5ec37e0d93645_articlex)

### 前言

这篇文章的自定义函数，主要说一些关于身份证号的信息，因为我们的身份证号的18位数字里，包含了我们的地址和出生年月日以及性别等关键信息，就不虾扯蛋了，直接说正事，我后续会陆续写一些PHP开发中实用的一些自定义函数，方便用到的朋友，能够快速开发和使用。

### 身份证号包含的基本信息

- **省市区三级地址**：身份证号的前六位数字
- **出生的年月日**：身份证号的第七位到第十四位数字
- **性别是男是女**：身份证号的第十七位数字

<!--more-->

比如韦小宝的身份证号为`11204416541220243X`，那么涵盖如下信息：

- `112044`为韦小宝的户籍地址的省市区的政府代码，即北京市东城区
- `16541220`为韦小宝的出生年月日，即1654年12月20日
- 第17位数字`3`标识韦小宝为男性
- 其他……

为了方便大家使用，我还特别查找了省市区的政府代码，整理成数组的格式，其中数组的键`key`为政府代码的六位数，数组的值`value`为三级省市区地址，且上传到GitHub中，大家有需要的，可以点击下面的两个链接查看。

六位数代码：[https://github.com/gxcuizy/Blog/blob/master/code/area_code.php](https://github.com/gxcuizy/Blog/blob/master/code/area_code.php)

省份代码：[https://github.com/gxcuizy/Blog/blob/master/code/province_code.php](https://github.com/gxcuizy/Blog/blob/master/code/province_code.php)

**此外**，为了方便大家能够快速的识别到身份证的相关信息，我还写了几个函数，只要传入身份证号，就能获取其中的奥秘信息，是不是很激动，很刺激，很惊喜呢……

### 校验是否为合法的身份证号

这里，我们就用最简单的正则表达式来校验身份证的基本格式，并不是十分的严密，但是基本够用了，如果想最有效的校验身份证号的准确性，就需要借助省市区政府代码等的校验，这里不做这个处理了。

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

### 通过身份证号获取省市区地址信息

前面也说过了，身份证号的前六位数字标识省市区三级地址信息，其中两个数字一级，那么，前两个数就标识省份，中间两个数就标识城市，最后两个数标识地区，所以，我们可以通过这个关联，来获取我们想要的信息，比如下面的方法，可以获取用户的三级地址信息和所属省份……

```php
/**
 * 通过身份证号获取省市区地址信息
 * @param string $id_card
 * @return array
 */
function get_address_by_id_card($id_card = '')
{
    // 先引入政府代码数组数据文件
    require 'area_code.php';
    require 'province_code.php';
    // 获取政府代码前两位和前六位
    $two_code = substr($id_card, 0, 2);
    $six_code = substr($id_card, 0, 6);
    // 获取城市信息
    $province = $province_code[$two_code];
    $address = $area_code[$six_code];
    $res = [
        'province' => $province,
        'area' => $address
    ];
    return $res;
}

```

### 通过身份证号计算年龄

身份证号的第七位数到第十四位数，标识出生年月日，也就是，7-10位数表示出生年份，10-12位数表示出生月份，13-14位数表示出生日期，知道了这个，我们可以可以很快速的计算出年龄，方法如下：

```php
/**
 * 通过身份证号计算年龄
 * @param string $id_card 身份证号
 * @return int
 */
function get_age_by_id_card($id_card = '')
{
    // 获取出生年月日
    $year = substr($id_card, 6, 4);
    $month = substr($id_card, 10, 2);
    $day = substr($id_card, 12, 2);
    // 计算时间年月日差
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

### 通过身份证判断是否成年

同样的，在中国，法定年满18周岁就算成年人了，就需要担负法律责任了；那么知道了出生年月日，那么就可以判断出是否成年了，不知不觉，曾经口头常常提起的`90后`慢慢变老油条，而`00后`都已经成年了，时光飞逝啊……

```php
/**
 * 通过身份证判断是否成年
 * @param string $id_card 身份证号
 * @return bool
 */
function check_adult($id_card = '')
{
    // 获取出生年月日
    $year = substr($id_card, 6, 4);
    $month = substr($id_card, 10, 2);
    $day = substr($id_card, 12, 2);
    // 18年的秒数
    $adult_time = 18 * 365 * 24 * 60 * 60;
    // 出生年月日的时间戳
    $birthday_time = mktime(0, 0, 0, $month, $day, $year);
    // 是否成年，默认未成年
    $is_adult = false;
    // 超过18岁则成年
    if ((time() - $birthday_time) > $adult_time) {
        $is_adult = true;
    }
    return $is_adult;
}
```

### 通过身份证获取所属生肖

十二生肖包含：`鼠牛虎兔龙蛇，马羊猴鸡狗猪`。计算所属生肖，我们只需要出生年份就可以了，我们以1901年作为起点来计算，查一下都知道，1901年是属牛的，以这作为一个周期的起点计算往后的年份所属生肖。

```php
/**
 * 通过身份证获取所属生肖
 * @param string $id_card 身份证号
 * @return string
 */
function get_animal_by_card($id_card = '')
{
    // 获取出生年份
    $start = 1901;
    $end = substr($id_card, 6, 4);
    $remainder = ($start - $end) % 12;
    // 计算所属生肖
    $animal = "";
    if ($remainder == 1 || $remainder == -11) $animal = "鼠";
    else if ($remainder == 0) $animal = "牛";
    else if ($remainder == 11 || $remainder == -1) $animal = "虎";
    else if ($remainder == 10 || $remainder == -2) $animal = "兔";
    else if ($remainder == 9 || $remainder == -3) $animal = "龙";
    else if ($remainder == 8 || $remainder == -4) $animal = "蛇";
    else if ($remainder == 7 || $remainder == -5) $animal = "马";
    else if ($remainder == 6 || $remainder == -6) $animal = "羊";
    else if ($remainder == 5 || $remainder == -7) $animal = "猴";
    else if ($remainder == 4 || $remainder == -8) $animal = "鸡";
    else if ($remainder == 3 || $remainder == -9) $animal = "狗";
    else if ($remainder == 2 || $remainder == -10) $animal = "猪";
    return $animal;
}
```

### 通过身份证获取所属星座

上面刚说了，年份可以计算生肖，那么月份和日期可以计算什么呢，当然是所属星座了；那么星座是怎么划分的呢，我[百度百科](https://baike.baidu.com/item/%E6%98%9F%E5%BA%A7%E6%9F%A5%E8%AF%A2)查了一下，具体划分规则如下：
```
白羊座
每年3月21日～每年4月20日
金牛座
每年4月21日～每年5月20日
双子座
每年5月21日～每年6月21日
巨蟹座
每年6月22日～每年7月22日
狮子座
每年7月23日～每年8月22日
处女座
每年8月23日～每年9月22日
天秤座
每年9月23日～每年10月23日
天蝎座
每年10月24日～每年11月22日
射手座
每年11月23日～每年12月21日
摩羯座
每年12月22日～每年1月19日
水瓶座
每年1月20日～每年2月18日
双鱼座
每年2月19日～每年3月20日
```

有了计算的规则，那么就可以很快速的获取所属星座了，方法如下：

```php
/**
 * 通过身份证获取所属星座
 * @param string $id_card 身份证号
 * @return string
 */
function get_constellation_by_card($id_card = '')
{
    // 截取生日的时间
    $birthday = substr($id_card, 10, 4);
    $month = substr($birthday, 0, 2);
    $day = substr($birthday, 2);
    // 判断时间范围获取星座
    $constellation = "";
    if (($month == 1 && $day >= 21) || ($month == 2 && $day <= 19)) $constellation = "水瓶座";
    else if (($month == 2 && $day >= 20) || ($month == 3 && $day <= 20)) $constellation = "双鱼座";
    else if (($month == 3 && $day >= 21) || ($month == 4 && $day <= 20)) $constellation = "白羊座";
    else if (($month == 4 && $day >= 21) || ($month == 5 && $day <= 21)) $constellation = "金牛座";
    else if (($month == 5 && $day >= 22) || ($month == 6 && $day <= 21)) $constellation = "双子座";
    else if (($month == 6 && $day >= 22) || ($month == 7 && $day <= 22)) $constellation = "巨蟹座";
    else if (($month == 7 && $day >= 23) || ($month == 8 && $day <= 23)) $constellation = "狮子座";
    else if (($month == 8 && $day >= 24) || ($month == 9 && $day <= 23)) $constellation = "处女座";
    else if (($month == 9 && $day >= 24) || ($month == 10 && $day <= 23)) $constellation = "天秤座";
    else if (($month == 10 && $day >= 24) || ($month == 11 && $day <= 22)) $constellation = "天蝎座";
    else if (($month == 11 && $day >= 23) || ($month == 12 && $day <= 21)) $constellation = "射手座";
    else if (($month == 12 && $day >= 22) || ($month == 1 && $day <= 20)) $constellation = "魔羯座";
    return $constellation;
}
```

### 通过身份证获取性别

上面知道了身份证的地址和出生年月日，那么，世界这么大，其实只有两种人，那就是男人和女人，当然了，网上说还有一种人，叫做`女博士`，这我就不太懂了，也不敢深究，暂不讨论，只分男女就行了。在身份证号中，第十七位数字表示性别，即：偶数为女性，奇数为男性。

```php
/**
 * 通过身份证获取性别
 * @param string $id_card 身份证号
 * @return string
 */
function get_sex($id_card = '')
{
    // 第十七位数字，偶数标识女性，奇数标识男性
    $sex_num = substr($id_card, 16, 1);
    $sex = $sex_num % 2 === 0 ? '女' : '男';
    return $sex;
}
```

### 自定义函数源码

为了方便，我把我整理的全部自定义函数，都放到一个文件中，并且上传到同性交友网站GitHub上了，方便交流和使用，也方便大家帮我排错，需要的同学自取即可，我会不定时更新，地址如下：

函数源码地址：[https://github.com/gxcuizy/Blog/blob/master/code/common.php](https://github.com/gxcuizy/Blog/blob/master/code/common.php)

### 最后

我后续会慢慢更新其他的实用自定义函数，如果大家有其他好玩的、好用的欢迎分享出来，大家一起学习和交流。对了，如果有说的不对的或者错误的地方，请大家指出来，我会努力改进，谢谢。