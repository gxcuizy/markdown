---
title: 代码片段之jQuery控制input只能输入数字和两位小数
date: 2019-05-16 11:27:18
tags: [代码片段, jQuery, 正则]
---

![page_img](https://images.unsplash.com/photo-1552661014-41c6afdfb259?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80)

### 前言

做为一个PHPER，难免会遇到那种表单中jQuery限制输入的问题，比如，限制空格的输入，只允许输入数字，以及小数点的控制等等，这里，我们就说一下数字的限制。

### jquery代码

话不多说，直接先上jQuery函数，具体的可以看注释说明，在使用这个之前，请务必保证已经提前引入了jQuery库，大家可以自己下载一个jQuery文件，然后引入，也可以查找CDN地址引入，比如在[https://www.bootcdn.cn/jquery/](https://www.bootcdn.cn/jquery/)可以查找到很多版本的引入地址，直接找到你想要的引入就行。

```
<script>
    // 格式化限制数字文本框输入，只能数字或者两位小数
    function format_input_num(obj){
        // 清除"数字"和"."以外的字符
        obj.value = obj.value.replace(/[^\d.]/g,"");
        // 验证第一个字符是数字
        obj.value = obj.value.replace(/^\./g,"");
        // 只保留第一个, 清除多余的
        obj.value = obj.value.replace(/\.{2,}/g,".");
        obj.value = obj.value.replace(".","$#$").replace(/\./g,"").replace("$#$",".");
        // 只能输入两个小数
        obj.value = obj.value.replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3');
    }
</script>
```

### 函数的直接用法之onkeyup

在input表单输入中，限制最多只能保留两位小数点，其他自动抹掉；这里会用到onkeyup事件，也就是onkeyup事件会在键盘按键被松开时发生，也就是，这个时候调用我们的函数，来处理已输入的内容。

```
<input type="text" onkeyup="format_input_num(this)" value="" size="10" />元
```

### 函数的直接用法之blur

除了上面的监控键盘事件外，还可以通过监控表单的焦点事件来实现，也就是，表单都有获得焦点事件focus和失去焦点事件blur，我们只需要在失去焦点的时候，调用我们的format_input_num函数就可以了，具体如下：

```
<input type="text" onblur="format_input_num(this)" value="" size="10" />元
```

或者不在表单中直接绑定方法，而是去jQuery中通过查找元素节点，然后单独绑定相应的事件，并执行相关函数

```
<input type="text" value="" size="10" id="money" />元
<script>
    $("#money").off('blur').on('blur', function(){
        format_input_num(this);
    });
</script>
```

### 其他输入限制

限制只能输入数字的写法，也就是，只能输入0-9的数字

```
<input type="text" onkeyup='this.value=this.value.replace(/\D/gi,"")' />
```

限制只能输入数字、字母和横线"-"，其中字母包括大小写

```
<input type="text" onkeyup='value=value.replace(/[^A-Za-z0-9\-]+/g,"")' />
```

当然了，还有其他很多校验规则，可以自己根据实际需求进行修改和尝试一下

### 最后

这就是我分享CODING过程中的一些代码片段，有不对或者需要优化的地方，大家可以给我留言。

感谢[http://www.cnblogs.com/angto64/p/5459496.html](http://www.cnblogs.com/angto64/p/5459496.html)