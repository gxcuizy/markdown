有的时候，你可能有这种需求，需要将一个数字分为N等份，多余的自动分配给其中一个数字。

实现方法有如下两种，当然还有其他的，比如截取substr等，有兴趣的可以自己尝试：

第一种方法，采用bc函数，即PHP的数学扩展库bcmath，具体可以点击如下链接查看更多了解

[BC数学函数][1]     http://php.net/manual/zh/ref.bc.php

不多说了，直接上代码：

```
* 一个数字平分为N等份
* @param int $number 待平分的数字
* @param int $taotl 平分总个数
* @param int $index 保留小数位
*/
function getDivideNumber($number, $total, $index = 2) {
    // 除法取平均数
    $divide_number  = bcdiv($number, $total, $index);
    // 减法获取最后一个数
    $last_number = bcsub($number, $divide_number*($total-1), $index);
    // 拼装平分后的数据返回
    $number_str = str_repeat($divide_number.'+', $total-1).$last_number;
    return explode(',', $number_str);
}
```

第二种方法，是我自定义的一种方法，大概思路是将待平分的数字乘以10的N次方，然后平分floor舍去取整，再除以10的N次方得到平分数，再用减法获取最后一个数，并格式化小数位，具体实现方法如下：

```
/**
* 一个数字平分为N等份
* @param int $number 待平分的数字
* @param int $taotl 平分总个数
* @param int $index 保留小数位
*/
function getDivideNumber($number, $total, $index = 2) {
    // 取平均数
    $divide_number = floor($number / $total * pow(10, $index)) / pow(10, $index);
    $divide_number = number_format($divide_number, $index, '.', '');
    // 获取最后一个数字
    $last_number = $number - $divide_number * ($total - 1);
    $last_number = number_format_plus($last_number, $index, '.', '');
    // 拼装平分后的数据返回
    $number_str = str_repeat($divide_number . ',', $total - 1) . $last_number;
    return explode(',', $number_str);
}
```

有说的不对的地方，请大家理解，欢迎留言，相互交流。

  [1]: http://php.net/manual/zh/ref.bc.php
