## 通过新浪微博API，生成短链接，支持一次性转多个长链接

### 什么是短链接

> 短链接，通俗来说，就是将长的URL网址，通过程序计算等方式，转换为简短的网址字符串。

### 短链接服务

国内各大微博都推出了自己的短链接服务。例如新浪微博、腾讯微博等。

### 为什么选用新浪微博API

1. 新浪微博短链接API是开放的
2. 新浪微博短链接API不需要用户登录

### 文档查询链接

- [short_url/shorten接口地址][short_url]
- [网上的一些公开的AppKey][appkey_list]
- [新浪微博短链接在线生成][short_online_url]

[short_url]:http://open.weibo.com/wiki/2/short_url/shorten
[appkey_list]:https://fengmk2.com/blog/appkey.html
[short_online_url]:http://dwz.wailian.work/

### 使用方法

拿到自己的AppKey后，替换类的成员属性$appKey的值即可，如下这样的，$shortUrl是API请求地址

```
// APPkey，我在网上找的（https://fengmk2.com/blog/appkey.html），可以自己申请
protected $appKey = '569452181';
// 转短连接API地址
protected $shortUrl = 'https://api.weibo.com/2/short_url/shorten.json?';
```

其他的，基本不需要配置，直接实例化类ShortLink，然后调用方法getShortUrl即可，需要说明的是长链接URL数组$longUrl里的值可以传多个值

当然了，为了方便，我写为一个类，可以根据自己的需要，进行调整，满足自己的需求即可。

### 源码

```
<?php

/**
 * 通过新浪微博API，生成短链接，支持一次性转多个长链接
 * Class shortClass
 * @time 2018-08-14
 * @author gxcuizy
 */
Class ShortLink {
    // APPkey，我在网上找的（https://fengmk2.com/blog/appkey.html），可以自己申请
    protected $appKey = '569452181';
    // 转短连接API地址
    protected $shortUrl = 'https://api.weibo.com/2/short_url/shorten.json?';

    /**
     * 生成短链接
     * @param array $longUrl 长链接数组
     * @return array 返回短连接数据
     */
    public function getShortUrl($longUrl = []) {
        $code = true;
        $msg = '请求成功！';
        $result = [];
        // 长链接数组为空，不处理
        if (empty($longUrl)) {
            $code = false;
            $msg = '长链接数据不能为空';
            return ['code' => $code, 'msg' => $msg, 'result' => $result];
        }
        // 拼接请求URL
        $longUrlStr = $this->_getLongUrl($longUrl);
        $shortUrl = $this->shortUrl;
        $appKey = $this->appKey;
        $param = 'source=' . $appKey . '&' . $longUrlStr;
        $curlUrl = $shortUrl . $param;
        // 发送CURL请求
        $result = $this->_sendCurl($curlUrl);
        return ['code' => $code, 'msg' => $msg, 'result' => $result];
    }

    /**
     * 获取请求URL字符串
     * @param array $longUrl 长链接数组
     * @return string 长链接URL字符串
     */
    private function _getLongUrl($longUrl = []) {
        $str = '';
        foreach ($longUrl as $url) {
            $str .= ('url_long=' . $url . '&');
        }
        $newStr = substr($str, 0, strlen($str) - 1);
        return $newStr;
    }

    /**
     * 发送CURL请求（GET）
     * @param string $curlUrl 请求地址
     * @return array 返回信息
     */
    private function _sendCurl($curlUrl) {
        // 初始化
        $ch = curl_init();
        // 设置选项，包括URL
        curl_setopt($ch, CURLOPT_URL, $curlUrl);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_HEADER, 0);
        // 执行并获取HTML文档内容
        $output = curl_exec($ch);
        // 释放curl句柄
        curl_close($ch);
        // Json数据转为数组
        $result = json_decode($output, true);
        return $result;
    }
}

// 实例化对象
$shortObj = new ShortLink();
// 多个连接可以直接放到数组中，类似$longUrl = ['url1', 'url2', ……]
$longUrl = ['http://blog.y0701.com/index.html'];
// 开始转长链接为短链接
$result = $shortObj->getShortUrl($longUrl);
print_r($result);
```

### 结束语

上面说到的网上查找得到的一些AppKey，因为来源不明，所以，不建议用于生产环境，需要用于生产环境的话，建议直接在新浪微博开发者平台里创建自己的应用就行。