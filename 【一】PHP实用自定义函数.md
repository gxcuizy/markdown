---
title: 【一】PHP实用自定义函数
date: 2020-05-12 13:52:17
tags: [PHP, 函数]
---

![](https://image-static.segmentfault.com/107/996/1079965234-5eba3b4e75aa3_articlex)

### 前言

我清楚的记得，是谁在我耳边说：“PHP是世界上最好的语言”，反正我可没说哈（理不直气还壮），我就听过这种言论，毕竟我胆小，哪里敢在公众场合说这种话，关于“谁是最好语言的言论”，很早之前，就在IT界掀起过多场血雨腥风的争论都无果，咱们就不要再搞事了，老老实实搬砖……

好了，虾扯蛋完毕，开始说点正事，我后续会陆续写一些PHP开发中实用的一些自定义函数，方便用到的朋友，能够快速开发和使用。

<!--more-->

### 返回格式化时间

我们在开发过程中，总会遇到一些显示时间的问题，有的时候需要显示`年-月-日`，有的时候需要显示`年-月-日 时.分.秒`，在每次遇到使用的时候，都会重复的写着一行类似`date($time, 'Y-m-d H:i:s')`的代码，想不想有一个更加优雅的写法呢，那就是自定义一个函数，就是下面定义的函数，使用的时候，如果时间格式是默认的，那么直接调用函数`time_format($time)`传入时间戳就可以了，是不是感觉这种看着就舒服一点呢？

```
/**
 * 返回格式化时间
 * @param int $time 时间戳
 * @param string $format 时间格式
 * @return bool|string
 */
function time_format($time = 0, $format = '')
{
    // 默认时间格式
    if (empty($format)) {
        $format = 'Y-m-d H:i:s';
    }
    $format_time = date($format, $time);
    return $format_time;
}
```

### 格式化数字

关于数字的格式处理的时候，我想大家都没少遇到，甚至还因为某数据显示的数字没有格式化而被测试提过bug呢？反正我是被测试抓到过，还不得不改的那种，比如：没有保留两位小数了等，然后就老老实实修改代码，把原来没处理的数字格式化一下，写法为`number_format($number, 2, '.', ',')`，发现一口气传了4个参数，而且，假如，`$number`不是数字，那么这个函数就会报错了，所以，还不如自定义一个，方便快捷，直接使用`number_format_plus($number)`就搞定了！

```
/**
 * 返回格式化数字
 * @param int $number 待格式化数字
 * @param int $decimals 保留小数位数，默认2位
 * @param string $dec_point 整数和小数分隔符号
 * @param string $thousands_sep 整数部分每三位数读分隔符号
 * @return string
 */
function number_format_plus($number = 0, $decimals = 2, $dec_point = '.', $thousands_sep = ',')
{
    $format_num = '0.00';
    if (is_numeric($number)) {
        $format_num = number_format($number, $decimals, $dec_point, $thousands_sep);
    }
    return $format_num;
}
```

### 人民币数字小写转大写

人民币转大写，这种一般在合同类的文件中会遇到的比较多，因为我之前工作中都接触到一些合同类的文件处理，所以，这个函数我一直用着，好的东西当然得拿出来分享了，万一你也刚好有需要呢

```
/**
 * 人民币数字小写转大写
 * @param string $number 人民币数值
 * @param string $int_unit 币种单位，默认"元"，有的需求可能为"圆"
 * @param bool $is_round 是否对小数进行四舍五入
 * @param bool $is_extra_zero 是否对整数部分以0结尾，小数存在的数字附加0,比如1960.30
 * @return string
 */
function rmb_format($money = 0, $int_unit = '元', $is_round = true, $is_extra_zero = false)
{
    // 非数字，原样返回
    if (!is_numeric($money)) {
        return $money;
    }
    // 将数字切分成两段
    $parts = explode('.', $money, 2);
    $int = isset($parts[0]) ? strval($parts[0]) : '0';
    $dec = isset($parts[1]) ? strval($parts[1]) : '';
    // 如果小数点后多于2位，不四舍五入就直接截，否则就处理
    $dec_len = strlen($dec);
    if (isset($parts[1]) && $dec_len > 2) {
        $dec = $is_round ? substr(strrchr(strval(round(floatval("0." . $dec), 2)), '.'), 1) : substr($parts [1], 0, 2);
    }
    // 当number为0.001时，小数点后的金额为0元
    if (empty($int) && empty($dec)) {
        return '零';
    }
    // 定义
    $chs = ['0', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖'];
    $uni = ['', '拾', '佰', '仟'];
    $dec_uni = ['角', '分'];
    $exp = ['', '万'];
    $res = '';
    // 整数部分从右向左找
    for ($i = strlen($int) - 1, $k = 0; $i >= 0; $k++) {
        $str = '';
        // 按照中文读写习惯，每4个字为一段进行转化，i一直在减
        for ($j = 0; $j < 4 && $i >= 0; $j++, $i--) {
            // 非0的数字后面添加单位
            $u = $int{$i} > 0 ? $uni [$j] : '';
            $str = $chs [$int{$i}] . $u . $str;
        }
        // 去掉末尾的0
        $str = rtrim($str, '0');
        // 替换多个连续的0
        $str = preg_replace("/0+/", "零", $str);
        if (!isset($exp [$k])) {
            // 构建单位
            $exp [$k] = $exp [$k - 2] . '亿';
        }
        $u2 = $str != '' ? $exp [$k] : '';
        $res = $str . $u2 . $res;
    }
    // 如果小数部分处理完之后是00，需要处理下
    $dec = rtrim($dec, '0');
    // 小数部分从左向右找
    if (!empty($dec)) {
        $res .= $int_unit;
        // 是否要在整数部分以0结尾的数字后附加0，有的系统有这要求
        if ($is_extra_zero) {
            if (substr($int, -1) === '0') {
                $res .= '零';
            }
        }
        for ($i = 0, $cnt = strlen($dec); $i < $cnt; $i++) {
            // 非0的数字后面添加单位
            $u = $dec{$i} > 0 ? $dec_uni [$i] : '';
            $res .= $chs [$dec{$i}] . $u;
            if ($cnt == 1)
                $res .= '整';
        }
        // 去掉末尾的0
        $res = rtrim($res, '0');
        // 替换多个连续的0
        $res = preg_replace("/0+/", "零", $res);
    } else {
        $res .= $int_unit . '整';
    }
    return $res;
}
```

### 生成短网址

国内也有好多短网址生成接口，但是发现国外的`tinyurl.com`的提供的短网址接口很方便使用，直接需要传入一个网址就能生成一个短链接了，至于安全性和速度性能啥的，就再说了，我之前，也有写过一篇文章，关于新浪短网址的生成，有兴趣的话可以查看一下，文章入口-[新浪微博API生成短链接](https://juejin.im/post/5b72766b51882560f53c6e03)

```
/**
 * 获取短网址链接
 * @param string $url 原始网址
 * @return string
 */
function get_short_url($url = '')
{
    // 直接请求第三方接口地址，获取短URL
    $api_url = 'http://tinyurl.com/api-create.php?url=';
    $short_url = file_get_contents($api_url . $url);
    return $short_url;
}
```

### 获取用户真实的IP地址

在需要分析用户的行为和操作日志的时候，肯定会遇到需要获取用户的IP地址的需求，因为在互联网中，能定位用户的，最有效最直接的就是IP地址，当然，也有人使用代理或者其他方式修改IP地址，导致这样获取的IP地址可能不准确，但是正常情况，这个方法获取用户的IP地址完全够用了。

```
/**
 * 获取用户真实的IP地址
 * @return mixed
 */
function get_real_ip()
{
    if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
        $ip = $_SERVER['HTTP_CLIENT_IP'];
    } elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
        $ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
    } else {
        $ip = $_SERVER['REMOTE_ADDR'];
    }
    return $ip;
}
```

### 导出excel表格数据

我们常用的导出Excel表格的库类有`PHPExcel`等，但是，想不想不借助任何库类，能直接导出Excel表格数据呢，当然是有办法的，那就是直接利用`html`的`table`表格来生成表格数据并导出。

```
/**
 * 导出excel表格数据
 * @param array $data 表格数据，一个二维数组
 * @param array $title 第一行标题，一维数组
 * @param string $filename 下载的文件名
 */
function export_excel($data = [], $title = [], $filename = '')
{
    // 默认文件名为时间戳
    if (empty($filename)) {
        $filename = time();
    }
    // 定义输出header信息
    header("Content-type:application/octet-stream;charset=GBK");
    header("Accept-Ranges:bytes");
    header("Content-type:application/vnd.ms-excel");
    header("Content-Disposition:attachment;filename=" . $filename . ".xls");
    header("Pragma: no-cache");
    header("Expires: 0");
    ob_start();
    echo "<head><meta http-equiv='Content-type' content='text/html;charset=GBK' /></head> <table border=1 style='text-align:center'>\n";
    // 导出xls开始，先写表头
    if (!empty($title)) {
        foreach ($title as $k => $v) {
            $title[$k] = iconv("UTF-8", "GBK//IGNORE", $v);
        }
        $title = "<td>" . implode("</td>\t<td>", $title) . "</td>";
        echo "<tr>$title</tr>\n";
    }
    // 再写表数据
    if (!empty($data)) {
        foreach ($data as $key => $val) {
            foreach ($val as $ck => $cv) {
                if (is_numeric($cv) && strlen($cv) < 12) {
                    $data[$key][$ck] = '<td>' . mb_convert_encoding($cv, "GBK", "UTF-8") . "</td>";
                } else {
                    $data[$key][$ck] = '<td style="vnd.ms-excel.numberformat:@;">' . iconv("UTF-8", "GBK//IGNORE", $cv) . "</td>";
                }
            }
            $data[$key] = "<tr>" . implode("\t", $data[$key]) . "</tr>";
        }
        echo implode("\n", $data);
    }
    echo "</table>";
    ob_flush();
    exit;
}
```

### 下载文件（支持断点续传）

有的时候，我们从网上下载文件，但是有的时候下载一个大文件，突然下载到一半或者即将完成的时候，突然来了个网络失败，导致下载暂停中断了，如果等会网络恢复了，你又要重新开始下载，是不是得骂娘那种，但是呢，如果网络恢复了，你能够继续从网络中断之前的位置继续下载，是不是又开心了，当然，我们都希望是这样，但是有些黑心开发者，就可能不会让你开心，所以，你是想当不让人开心的黑心开发者还是做个好人呢，奉劝大家都做个善良的人吧，哈哈哈

```
/**
 * 支持断点续传，下载文件
 * @param string $file 下载文件完整路径
 */
function download_file_resume($file)
{
    // 检测文件是否存在
    if (!is_file($file)) {
        die("非法文件下载！");
    }
    // 打开文件
    $fp = fopen("$file", "rb");
    // 获取文件大小
    $size = filesize($file);
    // 获取文件名称
    $filename = basename($file);
    // 获取文件扩展名
    $file_extension = strtolower(substr(strrchr($filename, "."), 1));
    // 根据扩展名 指出输出浏览器格式
    switch ($file_extension) {
        case "exe":
            $ctype = "application/octet-stream";
            break;
        case "zip":
            $ctype = "application/zip";
            break;
        case "mp3":
            $ctype = "audio/mpeg";
            break;
        case "mpg":
            $ctype = "video/mpeg";
            break;
        case "avi":
            $ctype = "video/x-msvideo";
            break;
        default:
            $ctype = "application/force-download";
    }
    // 通用header头信息
    header("Cache-Control:");
    header("Cache-Control: public");
    header("Content-Type: $ctype");
    header("Content-Disposition: attachment; filename=$filename");
    header("Accept-Ranges: bytes");
    // 如果有$_SERVER['HTTP_RANGE']参数
    if (isset($_SERVER['HTTP_RANGE'])) {
        // 断点后再次连接$_SERVER['HTTP_RANGE']的值
        list($a, $range) = explode("=", $_SERVER['HTTP_RANGE']);
        str_replace($range, "-", $range);
        // 文件总字节数
        $size2 = $size - 1;
        // 获取下次下载的长度
        $new_length = $size2 - $range;
        header("HTTP/1.1 206 Partial Content");
        // 输入总长
        header("Content-Length: $new_length");
        header("Content-Range: bytes $range$size2/$size");
        // 设置指针位置
        fseek($fp, $range);
    } else {
        // 第一次连接下载
        $size2 = $size - 1;
        header("Content-Range: bytes 0-$size2/$size");
        // 输出总长
        header("Content-Length: " . $size);
    }
    // 虚幻输出
    while (!feof($fp)) {
        // 设置文件最长执行时间
        set_time_limit(0);
        // 输出文件
        print(fread($fp, 1024 * 8));
        // 输出缓冲
        flush();
        ob_flush();
    }
    fclose($fp);
    exit;
}
```

### 最后

好了，第一篇我就先大概分享这几个函数，后续会慢慢更新其他的实用函数，如果大家有其他好玩的、好用的欢迎分享出来，大家一起学习和交流。对了，如果有说的不对的或者错误的地方，请大家指出来，我会努力改进，谢谢。