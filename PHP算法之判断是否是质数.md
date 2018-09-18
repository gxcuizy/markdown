---
title: PHP算法之判断是否是质数
date: 2018-09-18 16:44:17
tags: [PHP, 算法]
---

![page_img_url](https://farm5.staticflickr.com/4256/35315926115_fcde5c8234_c.jpg)

### 质数的定义

> 质数又称素数。一个大于1的自然数，除了1和它自身外，不能整除其他自然数的数叫做质数；否则称为合数。

### 实现思路

循环所有可能的备选数字，然后和中间数以下且大于等于2的整数进行整除比较，如果能够被整数，则肯定不是质数，相反，就是质数。

<!--more-->

### 第一种算法

这也是最可能先想到的，也就是直接和备选数的中间数去比较，算法源码如下：

```
/**
 * 获取所有的质数
 * @param array $arr
 * @return array
 */
function get_prime_number($arr = []) {
    // 质数数组
    $primeArr = [];
    // 循环所有备选数
    foreach ($arr as $value) {
        // 备选数和备选数的中间数以下的数字整除比较
        for ($i = 2; $i <= floor($value / 2); $i++) {
            // 能够整除，则不是质数，退出循环
            if ($value % $i == 0) {
                break;
            }
        }
        // 被除数$j比备选数的中间数大的则为质数
        // 这样判断的依据：
        // 假如备选数为质数，则内层的for循环不会break退出，则执行完毕，$i会继续+1，即最后$i = floor($value / 2) + 1
        // 假如备选数不为质数，则内层的for循环遇到整除就会break退出，$i不会继续+1，即最后$i <= floor($value / 2)
        if ($value != 1 && $i > floor($value / 2)) {
            $primeArr[] = $value;
        }
    }
    return $primeArr;
}
```

 ### 第二种算法

认真的来说的话，这也不算是另外一种算法，只是对于第一种的稍微点点优化，及中间最大数的优化，缩小比较范围，算法源码如下：

```
/**
 * 获取所有的质数
 * @param array $arr
 * @return array
 */
function get_prime_number($arr = []) {
    // 质数数组
    $primeArr = [];
    // 循环所有备选数
    foreach ($arr as $value) {
        // 备选数和备选数的中间数以下的数字整除比较
        for ($i = 2; $i <= floor($value / $i); $i++) {
            // 能够整除，则不是质数，退出循环
            if ($value % $i == 0) {
                break;
            }
        }
        // 被除数$j比备选数的中间数大的则为质数
        // 这样判断的依据：
        // 假如备选数为质数，则内层的for循环不会break退出，则执行完毕，$i会继续+1，即最后$i = floor($value / $i) + 1
        // 假如备选数不为质数，则内层的for循环遇到整除就会break退出且$i不会继续+1，即最后$i <= floor($value / $i)
        if ($value != 1 && $i > floor($value / $i)) {
            $primeArr[] = $value;
        }
    }
    return $primeArr;
}
```

### 第三种算法

这个的话也是对于第二种的优化，即，直接从完整数组中删除所有不是质数的数即可，算法源码如下：

```
/**
 * 获取所有的质数
 * @param array $arr
 * @return array
 */
function get_prime_number_three($arr = []) {
    // 质数数组
    $primeArr = $arr;
    // 循环所有备选数
    foreach ($primeArr as $key => $value) {
        if ($value == 1) {
            unset($primeArr[$key]);
            continue;
        }
        // 备选数和备选数的中间数以下的数字整除比较
        for ($i = 2; $i <= floor($value / $i); $i++) {
            // 能够整除，则不是质数，从数组中删除且退出循环
            if ($value % $i == 0) {
                unset($primeArr[$key]);
                break;
            }
        }
    }
    // 重置数组索引返回
    return array_values($primeArr);
}
```

### 使用方法

比如，求1-100的所有质数
```
// 所有备选数数组
$numberArr = range(1, 100, 1);
// 获取备选数中的所有质数
$primeNumberArr = get_prime_number($numberArr);
// 输出打印
print_r($primeNumberArr);
```

又比如，求指定数组中的所有质数
```
// 所有备选数数组
$numberArr = [11, 22, 33, 66, 77, 3, 8, 10, 99];
// 获取备选数中的所有质数
$primeNumberArr = get_prime_number($numberArr);
// 输出打印
print_r($primeNumberArr);
```

### 最后

如有说的不对的地方，请大家多多谅解，欢迎留言和我沟通、交流，谢谢！