---
title: PHP算法之二分查找
date: 2018-09-20 11:34:42
tags: [PHP, 算法]
---

![page_img_url](http://www.ituring.com.cn/figures/2017/CalPic/06.d01z.008.png)

### 二分查找的定义

> 二分查找也称折半查找（Binary Search），它是一种效率较高的查找方法。但是，折半查找要求线性表必须采用顺序存储结构，而且表中元素按关键字有序排列。

### 算法的要求

从上面的定义我们可以知道，满足该算法的要求必须如下两点：
1. 必须采用顺序存储结构。
2. 必须按关键字大小有序排列。

<!--more-->

### 算法的步骤

其实，二分查找也还是比较容易理解的，大概就是一分为二，然后两边比较，保留有效区间，继续一分为二查找，直到找到或者超出区间则结束，所以二分查找的基本步骤是：
1. 确定要查找的区间
2. 确定要二分时的参照点
3. 区间内选取二分点
4. 根据二分点的值，综合左右区间情况以及求解的目的，舍去一半无用的区间
5. 继续在有效区间重复上面的步骤

### 算法源码

这里，我主要采用递归和非递归两种方法实现，具体如下：

首先第一种是非递归的算法实现，算法如下：

```
/**
 * 二分查找算法
 * @param array $arr 待查找区间
 * @param int $number 查找数
 * @return int        返回找到的键
 */
function binary_search($arr, $number) {
    // 非数组或者数组为空，直接返回-1
    if (!is_array($arr) || empty($arr)) {
        return -1;
    }
    // 初始变量值
    $len = count($arr);
    $lower = 0;
    $high = $len - 1;
    // 最低点比最高点大就退出
    while ($lower <= $high) {
        // 以中间点作为参照点比较
        $middle = intval(($lower + $high) / 2);
        if ($arr[$middle] > $number) {
            // 查找数比参照点小，舍去右边
            $high = $middle - 1;
        } else if ($arr[$middle] < $number) {
            // 查找数比参照点大，舍去左边
            $lower = $middle + 1;
        } else {
            // 查找数与参照点相等，则找到返回
            return $middle;
        }
    }
    // 未找到，返回-1
    return -1;
}
```

然后第二种是递归的算法实现，算法如下：

```
/**
 * @param array $arr 待查找区间
 * @param int $number 查找数
 * @param int $lower 区间最低点
 * @param int $high 区间最高点
 * @return int
 */
function binary_search_recursion(&$arr, $number, $lower, $high) {
    // 以区间的中间点作为参照点比较
    $middle = intval(($lower + $high) / 2);
    // 最低点比最高点大就退出
    if ($lower > $high) {
        return -1;
    }
    if ($number > $arr[$middle]) {
        // 查找数比参照点大，舍去左边继续查找
        return binary_search_recursion($arr, $number, $middle + 1, $high);
    } elseif ($number < $arr[$middle]) {
        // 查找数比参照点小，舍去右边继续查找
        return binary_search_recursion($arr, $number, $lower, $middle - 1);
    } else {
        return $middle;
    }
}
```

### 算法的使用

需求是在一个排列好的区间（$arr）中，查找一个数（$number）的所在位置，所以，调用算法查找如下：

```
// 待查找区间
$arr = [1, 3, 7, 9, 11, 57, 63, 99];
// 非递归查找57所在的位置
$find_key = binary_search($arr, 57);
// 递归查找57所在的位置
$find_key_r = binary_search_recursion($arr, 57, 0, count($arr));
// 输出打印
print_r($find_key);
print_r($find_key_r);
```


### 时间复杂度分析

在有序数组中如果用暴力的算法去查找，也就是逐个遍历比较，那么时间复杂度是O(n)；但是，用二分查找后，因为每次可以舍去一半查找区间，所以会将时间复杂度减少到O(logn)，算法更优。

### 最后

又到了无聊的客套话时间，老规律，有问题直接留言，有想法直接说，有错误直接提出来，我都会及时回复的，谢谢。