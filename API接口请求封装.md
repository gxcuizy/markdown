---
title: API接口请求的配置化封装
date: 2021-02-21 13:36:50
tags: [PHP, API]
---

![page_img](https://image-static.segmentfault.com/270/946/2709466764-6030b88952faa_articlex)

### 抛出问题

- 问题1：日常开发中，我们都会遇到接口类的请求，各种各样的第三方接口，以及内部接口等，大家都是怎么方便快捷的维护这些接口的快速请求呢？
- 问题2：面对第三方的接口，对接的时候记得，后续查找会不会觉得找不到在哪了呢？或者查找归类比较麻烦呢？
- 问题3：类似的第三方接口，你是否写重复的方法调用和处理结果呢？
- ……

如果你有上面的类似问题，是否会考虑优化呢？也就是把几户一样的接口做成配置化，不管是调用还是后期维护都比较方便呢？本着“方便他人，造福自己”的开发原则，必须从优处理，安排！

<!--more-->

### API接口例子

```php
// 接口1
地址： $url = 'https://www.test.com/api/test';
参数： $param = array('id' => 1, 'code' => '123', 'status' => 1);
返回： array('code' => 200, 'msg' => '');

// 接口2
地址： $url = 'https://www.test.com/api/test2';
参数： $param = array('type' => 1, 'num' => '');
返回： array('code' => 200, 'msg' => '');

// 接口N
```

针对上面的两个接口，如果做成配置化的请求，也就是，写好统一的请求入口，对于后续新增同样接口，只需要根据格式配置接口地址以及请求参数即可。

### 接口请求类设计原则

1. 单一入口
2. 接口信息可配置化
3. 统一校验接口参数，防止非法参数请求
4. 统一的请求方法和处理
5. 接口返回数据格式一致
6. ……

### 请求类的单一入口

单一入口是指每个接口请求，公共请求这个方法即可，此方法需要传配置的接口键的值，以及请求参数等，具体可以看代码里的注释说明。

```php
/**
 * 接口请求入口
 * @param string $action 配置的接口键名
 * @param array $param 请求参数
 * @param bool $is_format 是否格式化请求结果
 * @param bool $debug 是否开启调试模式
 * @return array|string 返回请求结果
 */
public static function request($action = '', $param = array(), $is_format = true, $debug = false)
{
    // 初始化
    self::initParam();
    // 校验参数，并设置请求参数
    $check = self::setApiParam($action, $param);
    if (!$check) {
        return self::$result;
    }
    // 发起接口请求
    $response = self::curlByPost(self::$url, self::$param, self::$token, self::$type);
    // 无需格式化直接返回
    if (!$is_format) {
        return $response;
    }
    // 设置返回值
    self::setResult($response);
    // 是否调试输出请求信息
    if ($debug) {
        self::echo_msg("url: " . self::$url);
        self::echo_msg("token: " . self::$token);
        self::echo_msg("param: " . json_encode(self::$param));
        self::echo_msg("response: " . $response);
    }
    return self::$result;
}
```

### 配置接口信息

上面的2个接口，直接做成配置化的形式，此配置`api_config`的键的名字可以自定义，最好命名为接口的说明，url为接口地址，type为Content-Type的类型选择，param就是接口参数，具体的参数配置看注释即可。

```php
// 接口地址，请求方式，参数的配置
// 1. required：是否必传（true为必传，false为选传）
// 2. default：可设置默认值，不传值时取
// 3. range：可设置传值范围，只可传范围内的值
// 其他可自由修改进行扩展
private static $api_config = array(
    // 测试接口1配置
    'test_1' => array(
        'url' => 'https://www.test.com/api/test',
        'type' => 'x-www-form-urlencoded',
        'param' => array(
            'id' => array('required' => true, 'default' => 1),
            'code' => array('required' => true),
            'status' => array('required' => true, 'range' => array(1, 2))
        )
    ),
    // 测试接口2配置
    'test_2' => array(
        'url' => 'https://www.test.com/api/test2',
        'type' => 'form-data',
        'param' => array(
            'type' => array('required' => true, 'default' => 1),
            'num' => array('required' => false)
        )
    ),
);
```

### 校验参数

根据配置的参数，进行校验请求传入的参数是否有效，可以有效过滤部分非法参数

```php
/**
 * 设置接口请求的参数和地址等请求信息
 * @param string $action 配置的接口键名
 * @param array $param 请求参数
 * @return bool 返回真假
 */
public static function setApiParam($action = '', $param = array())
{
    // 检查接口方法是否已配置
    if (!isset(self::$api_config[$action])) {
        self::$result['msg'] = '接口未配置';
        return false;
    }
    // 获取接口配置
    $api_info = self::$api_config[$action];
    $api_param = $api_info['param'];
    // 循环校验参数
    foreach ($api_param as $key => $config) {
        if (!isset($param[$key])) {
            // 字段未传
            if ($config['required'] && !isset($config['default'])) {
                // 必传，并且没有默认值则报错
                self::$result['msg'] = '参数[' . $key . ']必传';
                return false;
            }
            // 非必传，取默认值
            isset($config['default']) && self::$param[$key] = $config['default'];
        } else {
            // 字段已传
            self::$param[$key] = $param[$key];
        }
        // 判断是否在取值范围内
        if (self::$param[$key] && isset($config['range'])) {
            if (!in_array(self::$param[$key], $config['range'])) {
                // 不在取值范围内
                self::$result['msg'] = '参数[' . $key . ']的值不在取值范围内';
                return false;
            }
        }
    }
    // 如果需要获取token密钥，此方法需要to-do，如果其他签名方式可根据实际修改
    self::$token = self::getToken();
    // 接口地址
    if (empty($api_info['url'])) {
        self::$result['msg'] = '接口地址为空';
        return false;
    }
    self::$url = $api_info['url'];
    // Content-Type请求类型
    if (!isset(self::$headers[$api_info['type']])) {
        self::$result['msg'] = '无此请求类型';
        return false;
    }
    self::$type = $api_info['type'];
    return true;
}
```

### 完整源码

上面说的三点为核心部分，可能看起来有点云里雾里的感觉，我肯定不是那种不将就的人，完整的源码必须安排上，如有写到不到位或者不全的，请不要吐槽我啦，你懂的。

```php
<?php

/**
 * Created by PhpStorm.
 * User: gxcuizy
 * Date: 2021/02/20
 * Time: 下午 13:18
 * api接口请求封装类
 * Class ApiRequest
 */
class ApiRequest
{
    // 接口地址
    private static $url = '';
    // 请求header类型
    private static $type = '';
    // 接口密钥
    private static $token = '';
    // 请求参数
    private static $param = array();
    // 返回数组格式
    private static $result = array(
        'code' => 0,
        'msg' => '',
        'data' => array()
    );
    // header头类型数组
    private static $headers = array(
        '' => array(),
        'form-data' => array('Content-Type: multipart/form-data'),
        'x-www-form-urlencoded' => array('Content-Type：application/x-www-form-urlencoded'),
        'json' => array('Content-Type: application/json'),
    );
    // 接口地址，请求方式，参数的配置
    // 1. required：是否必传（true为必传，false为选传）
    // 2. default：可设置默认值，不传值时取
    // 3. range：可设置传值范围，只可传范围内的值
    // 其他可自由修改进行扩展
    private static $api_config = array(
        // 测试接口1配置
        'test_1' => array(
            'url' => 'https://www.test.com/api/test',
            'type' => 'x-www-form-urlencoded',
            'param' => array(
                'id' => array('required' => true, 'default' => 1),
                'code' => array('required' => true),
                'status' => array('required' => true, 'range' => array(1, 2))
            )
        ),
        // 测试接口2配置
        'test_2' => array(
            'url' => 'https://www.test.com/api/test2',
            'type' => 'form-data',
            'param' => array(
                'type' => array('required' => true, 'default' => 1),
                'num' => array('required' => false)
            )
        ),
    );

    /**
     * 接口请求入口
     * @param string $action 配置的接口键名
     * @param array $param 请求参数
     * @param bool $is_format 是否格式化请求结果
     * @param bool $debug 是否开启调试模式
     * @return array|string 返回请求结果
     */
    public static function request($action = '', $param = array(), $is_format = true, $debug = false)
    {
        // 初始化
        self::initParam();
        // 校验参数，并设置请求参数
        $check = self::setApiParam($action, $param);
        if (!$check) {
            return self::$result;
        }
        // 发起接口请求
        $response = self::curlByPost(self::$url, self::$param, self::$token, self::$type);
        // 无需格式化直接返回
        if (!$is_format) {
            return $response;
        }
        // 设置返回值
        self::setResult($response);
        // 是否调试输出请求信息
        if ($debug) {
            self::echo_msg("url: " . self::$url);
            self::echo_msg("token: " . self::$token);
            self::echo_msg("param: " . json_encode(self::$param));
            self::echo_msg("response: " . $response);
        }
        return self::$result;
    }

    /**
     * 初始化参数值
     */
    private static function initParam()
    {
        self::$url = '';
        self::$type = '';
        self::$token = '';
        self::$param = array();
        self::$result['code'] = 0;
        self::$result['msg'] = '';
        self::$result['data'] = array();
    }

    /**
     * 设置接口请求的参数和地址等请求信息
     * @param string $action 配置的接口键名
     * @param array $param 请求参数
     * @return bool 返回真假
     */
    public static function setApiParam($action = '', $param = array())
    {
        // 检查接口方法是否已配置
        if (!isset(self::$api_config[$action])) {
            self::$result['msg'] = '接口未配置';
            return false;
        }
        // 获取接口配置
        $api_info = self::$api_config[$action];
        $api_param = $api_info['param'];
        // 循环校验参数
        foreach ($api_param as $key => $config) {
            if (!isset($param[$key])) {
                // 字段未传
                if ($config['required'] && !isset($config['default'])) {
                    // 必传，并且没有默认值则报错
                    self::$result['msg'] = '参数[' . $key . ']必传';
                    return false;
                }
                // 非必传，取默认值
                isset($config['default']) && self::$param[$key] = $config['default'];
            } else {
                // 字段已传
                self::$param[$key] = $param[$key];
            }
            // 判断是否在取值范围内
            if (self::$param[$key] && isset($config['range'])) {
                if (!in_array(self::$param[$key], $config['range'])) {
                    // 不在取值范围内
                    self::$result['msg'] = '参数[' . $key . ']的值不在取值范围内';
                    return false;
                }
            }
        }
        // 如果需要获取token密钥，此方法需要to-do，如果其他签名方式可根据实际修改
        self::$token = self::getToken();
        // 接口地址
        if (empty($api_info['url'])) {
            self::$result['msg'] = '接口地址为空';
            return false;
        }
        self::$url = $api_info['url'];
        // Content-Type请求类型
        if (!isset(self::$headers[$api_info['type']])) {
            self::$result['msg'] = '无此请求类型';
            return false;
        }
        self::$type = $api_info['type'];
        return true;
    }

    /**
     * POST请求
     * @param string $url 接口地址
     * @param array $data 请求参数
     * @param string $token 密钥token
     * @param string $type 传参类型
     * @param array $header_ext 扩展的header信息
     * @return bool|string 返回请求结果
     */
    private static function curlByPost($url = '', $data = array(), $token = '', $type = 'json', $header_ext = array())
    {
        $header = self::$headers[$type];
        // 是否需要token
        if ($token) {
            $header[] = "Authorization:$token";
        }
        // 扩展的header信息
        if (!empty($header_ext)) {
            $header = array_merge($header, $header_ext);
        }
        // 发送POST请求
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $header);
        curl_setopt($ch, CURLOPT_HEADER, 0);
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 10);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
        $output = curl_exec($ch);
        curl_close($ch);
        return $output;
    }

    /**
     * 处理接口响应返回
     * @param string $response 接口返回数据
     */
    private static function setResult($response = '')
    {
        if ($response) {
            // 有返回值
            $result = json_decode($response, true);
            if (isset($result['code']) && $result['code'] == 200) {
                // 请求成功
                self::$result['data'] = $result['data'];
                self::$result['code'] = 200;
            } else {
                // 请求失败
                if (isset($result['code'])) {
                    self::$result['code'] = $result['code'];
                }
                self::$result['msg'] = $response;
            }
        } else {
            // 无返回值异常
            self::$result['msg'] = "empty response.";
        }
    }

    /**
     * 获取密钥token（TODO）
     * @return string
     */
    private static function getToken()
    {
        $token = '';
        return $token;
    }

    /**
     * 打印输出信息
     * @param string $msg 输出文本
     */
    private static function echo_msg($msg = '')
    {
        if (!empty($msg)) {
            $msg = "[" . date("Y-m-d H:i:s") . "] " . $msg . PHP_EOL;
            echo $msg;
            @ob_flush();
            @flush();
        }
    }
}
```

### 最后

刚过完春节，大家估计都还没缓过劲来进入Coding状态，恭祝大家在新的一年里能够收获多多，收获满满，2021所想皆能实现。如果大家有什么好的想法或者建议，也可以底部留言给我哈，感谢哦！