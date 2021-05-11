---
title: PHP脚本自动生成MySQL全库数据表的数据字典在线查看
date: 2021-05-11 09:36:19
tags: [PHP, MySQL, 数据字典]
---

![](https://image-static.segmentfault.com/609/801/609801494-609a1c712e257_fix732)

### 为什么需要数据字典

通过Navicat等数据库管理工具，我们也能看到数据表的结构设计，但是，如果我们把全部的数据表的结构设计都做成可在线预览的，会不会更加清晰明朗呢，而且也更加容易对比发现问题和及时优化，更有效率。

### 生成数据字典的方式

这里我主要利用`showdoc`在线文档实现数据字典的在线查看，主要说两种实现方式：分别是官方shell脚本和我写的PHP脚本；

- 官方shell脚本：仅支持在Linux服务器中运行，官方的文档地址：[https://www.showdoc.com.cn/page/312209902620725](https://www.showdoc.com.cn/page/312209902620725)
- 我写的PHP脚本：不管是在Linux还是在Windows等操作系统中都支持，而且更加灵活可控

<!--more-->

官方的脚本运行方式也比较简单，看看文档即明白，我下面主要说一下我写的PHP脚本的思路和运行方式，也就是利用`showdoc`提供的开放API接口实现将数据结构的信息以Markdown的格式上传到指定项目，文档地址：[https://www.showdoc.com.cn/page/102098](https://www.showdoc.com.cn/page/102098)

### 关键信息配置

因为连接数据库的配置信息以及需要上传的项目地址也不同，所以这些信息需要单独配置，具体我也不多说了，看下面代码及注释信息即可

```php
// 数据库连接配置信息
private $host = '127.0.0.1';
private $user_name = 'root';
private $password = 'root';
private $db_name = 'test';
private $port = 3306;
private $conn;
// showdoc文档API密钥配置，获取方法：https://www.showdoc.com.cn/page/741656402509783
private $api_key = '6b0ddb543b53f5002f6033cb2b00cec01908536369';
private $api_token = '9da3190d0dda1118de0e8bde08907fc51712469974';
```

### 连接和关闭MySQL数据库

为了方便快速跨平台使用，我使用的都是PHP原生的写法，所以，连接数据库以及查询数据都是使用原生的PHP写法，利用PHP类的语法特性，在构造函数中连接数据库并且在析构函数中关闭连接。

```php
/**
 * 构造函数，连接数据库
 * GetMysqlDict constructor.
 */
public function __construct()
{
    // 创建连接
    $this->conn = new mysqli($this->host, $this->user_name, $this->password, $this->db_name, $this->port);
    // 检测连接
    if ($this->conn->connect_error) {
        exit("数据库连接失败: " . $this->conn->connect_error);
    }
    $this->echoMsg('数据库连接成功');
}

/**
 * 析构函数，关闭数据库连接
 */
public function __destruct()
{
    $this->conn->close();
    $this->echoMsg('已关闭数据库连接');
}
```

### 查询表结构信息

连接上了数据库，那么我们就可以查询利用`Sql`语句数据库信息相关信息，利用语句`show table status;`可以查出当前连接库的全部数据表信息，然后再查询`information_schema.COLUMNS`表上具体某个表的数据结构信息，并组装数组返回使用。

```php
/**
 * 获取数据表列表
 * @return array
 */
private function getTableList()
{
    // 查看所有表信息
    $sql = 'show table status;';
    $result = $this->conn->query($sql);
    // 循环获取表数据
    $table_list = array();
    while ($row = $result->fetch_assoc()) {
        $table_list[] = $row;
    }
    return $table_list;
}

/**
 * 获取表结构信息
 * @param string $table
 * @return array
 */
private function getDictList($table = '')
{
    // 获取表结构信息（COLUMN_NAME,COLUMN_TYPE,NUMERIC_SCALE,IS_NULLABLE,COLUMN_DEFAULT,COLUMN_COMMENT）
    $sql = "select * from information_schema.COLUMNS where table_schema='" . $this->db_name . "' and table_name='" . $table . "';";
    $result = $this->conn->query($sql);
    $dict_list = array();
    while ($row = $result->fetch_assoc()) {
        $dict_list[] = $row;
    }
    return $dict_list;
}
```

### 通过API接口上传到项目

获取到表的数据结构信息，我们就可以拼装字段信息，并且通过开放API接口上传到执行的项目中，大家可以看我的一个测试的项目[https://www.showdoc.com.cn/1383736300665067](https://www.showdoc.com.cn/1383736300665067)，大家需要上传到自己的项目，只需要按照上面的说明修改相关配置即可，如果不想上传到`showdoc`官方的域名，可以自己利用开源代码搭建到自己的服务器上，然后部署好，上传到自己搭建的项目中也可以，具体可以查看相关的文档。

![](https://image-static.segmentfault.com/378/811/3788113120-6099ee506dade_fix732)

```php
/**
 * 发送接口请求，生成文档
 * @param string $title 页面标题（请保证其唯一）
 * @param string $content 页面内容（支持Markdown和HTML）
 * @param string $name 目录名（可选参数）
 * @param int $number 页面序号（默认99，越小越靠前）
 * @return array
 */
private function apiPost($title = '', $content = '', $name = '', $number = 99)
{
    // 接口地址，如果是自己利用开源搭建的，则接口地址为：http://xx.com/server/index.php?s=/api/item/updateByApi
    $url = 'https://www.showdoc.cc/server/api/item/updateByApi';
    // 请求参数
    $data = array(
        'api_key' => $this->api_key,
        'api_token' => $this->api_token,
        'cat_name' => $name,
        'page_title' => $title,
        'page_content' => $content,
        's_number' => $number
    );
    // 发送POST请求
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 10);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    $response = curl_exec($ch);
    curl_close($ch);
    return json_decode($response, true);
}
```

### 脚本执行核心处理

上面的数据获取以及上传方法有了，那么就可以将全部的表结构字段进行循环处理，拼装成Markdown的格式，上传到项目中。开放API接口有请求频率限制，也就是10分钟只能请求1000次，所以，如果单次请求过多的话，需要做频率控制，防止请求失败，未能成功上传到项目中。

![](https://image-static.segmentfault.com/729/014/729014535-6099ee729d049_fix732)

```php
/**
 * 执行入口
 */
public function run()
{
    // 获取数据表
    $table_list = $this->getTableList();
    $this->echoMsg('数据表总数：' . count($table_list));
    // 循环表获取结构信息
    $request_num = 0;
    foreach ($table_list as $table) {
        // 频率控制，10分钟内只能请求1000次
        if ($request_num >= 1000) {
            $request_num = 0;
            $this->echoMsg('频率控制，请等待10分钟后继续');
            sleep(600);
        }
        // 获取数据结构
        $msg = '表名：' . $table['Name'] . '（' . $table['Comment'] . '）';
        // 字典表头信息
        $table_dict = '#### ' . $table['Name'] . ' ' . $table['Comment'] . PHP_EOL;
        $table_dict .= '| 字段名称 | 类型长度 | 是否NULL | 默认值 | 注释 |' . PHP_EOL;
        $table_dict .= '| --- | --- | --- | --- | --- |' . PHP_EOL;
        // 获取表字段信息
        $dict_list = $this->getDictList($table['Name']);
        foreach ($dict_list as $dict) {
            $c_name = $dict['COLUMN_NAME'];
            $c_type = $dict['COLUMN_TYPE'];
            $c_null = $dict['IS_NULLABLE'];
            $c_default = $dict['COLUMN_DEFAULT'];
            $c_comment = $dict['COLUMN_COMMENT'];
            $table_dict .= '| ' . $c_name . ' | ' . $c_type . ' | ' . $c_null . ' | ' . $c_default . ' | ' . $c_comment . ' |' . PHP_EOL;
        }
        // 利用showdoc文档在线展示数据字典
        $response = $this->apiPost($table['Name'], $table_dict);
        if ($response['error_code'] == 0) {
            $msg .= ' 生成文档成功';
        } else {
            $msg .= ' 生成文档失败（' . $response['error_message'] . '）';
        }
        $request_num++;
        $this->echoMsg($msg);
    }
}
```

### 完整源码

上面的拆分部分，基本已经把核心的代码都列出来了，但是为了大家更方便快捷的使用以及反馈问题，一键复制完整源码直接运行，我把代码上传到交友网站了[Github](https://github.com/gxcuizy/Blog/tree/master/%E8%87%AA%E5%8A%A8%E7%94%9F%E6%88%90%E6%95%B0%E6%8D%AE%E5%AD%97%E5%85%B8)，同时，也把完整源码贴在下面，请叫我当代活雷锋……（我也不容易，别吐槽我用代码占用大量篇幅了）

```php
<?php

/**
 * 自动生成数据字典上传到showdoc项目中
 * User: gxcuizy
 * Date: 2021/05/10 0011
 * Time: 下午 15:17
 * Class GetMysqlDict
 */
class GetMysqlDict
{
    // 数据库连接配置信息
    private $host = '127.0.0.1';
    private $user_name = 'root';
    private $password = 'root';
    private $db_name = 'test';
    private $port = 3306;
    private $conn;
    // showdoc文档API密钥配置，获取方法：https://www.showdoc.com.cn/page/741656402509783
    private $api_key = '6b0ddb543b53f5002f6033cb2b00cec01908536369';
    private $api_token = '9da3190d0dda1118de0e8bde08907fc51712469974';

    /**
     * 构造函数，连接数据库
     * GetMysqlDict constructor.
     */
    public function __construct()
    {
        // 创建连接
        $this->conn = new mysqli($this->host, $this->user_name, $this->password, $this->db_name, $this->port);
        // 检测连接
        if ($this->conn->connect_error) {
            exit("数据库连接失败: " . $this->conn->connect_error);
        }
        $this->echoMsg('数据库连接成功');
    }

    /**
     * 执行入口
     */
    public function run()
    {
        // 获取数据表
        $table_list = $this->getTableList();
        $this->echoMsg('数据表总数：' . count($table_list));
        // 循环表获取结构信息
        $request_num = 0;
        foreach ($table_list as $table) {
            // 频率控制，10分钟内只能请求1000次
            if ($request_num >= 1000) {
                $request_num = 0;
                $this->echoMsg('频率控制，请等待10分钟后继续');
                sleep(600);
            }
            // 获取数据结构
            $msg = '表名：' . $table['Name'] . '（' . $table['Comment'] . '）';
            // 字典表头信息
            $table_dict = '#### ' . $table['Name'] . ' ' . $table['Comment'] . PHP_EOL;
            $table_dict .= '| 字段名称 | 类型长度 | 是否NULL | 默认值 | 注释 |' . PHP_EOL;
            $table_dict .= '| --- | --- | --- | --- | --- |' . PHP_EOL;
            // 获取表字段信息
            $dict_list = $this->getDictList($table['Name']);
            foreach ($dict_list as $dict) {
                $c_name = $dict['COLUMN_NAME'];
                $c_type = $dict['COLUMN_TYPE'];
                $c_null = $dict['IS_NULLABLE'];
                $c_default = $dict['COLUMN_DEFAULT'];
                $c_comment = $dict['COLUMN_COMMENT'];
                $table_dict .= '| ' . $c_name . ' | ' . $c_type . ' | ' . $c_null . ' | ' . $c_default . ' | ' . $c_comment . ' |' . PHP_EOL;
            }
            // 利用showdoc文档在线展示数据字典
            $response = $this->apiPost($table['Name'], $table_dict);
            if ($response['error_code'] == 0) {
                $msg .= ' 生成文档成功';
            } else {
                $msg .= ' 生成文档失败（' . $response['error_message'] . '）';
            }
            $request_num++;
            $this->echoMsg($msg);
        }
    }

    /**
     * 获取数据表列表
     * @return array
     */
    private function getTableList()
    {
        // 查看所有表信息
        $sql = 'show table status;';
        $result = $this->conn->query($sql);
        // 循环获取表数据
        $table_list = array();
        while ($row = $result->fetch_assoc()) {
            $table_list[] = $row;
        }
        return $table_list;
    }

    /**
     * 获取表结构信息
     * @param string $table
     * @return array
     */
    private function getDictList($table = '')
    {
        // 获取表结构信息（COLUMN_NAME,COLUMN_TYPE,NUMERIC_SCALE,IS_NULLABLE,COLUMN_DEFAULT,COLUMN_COMMENT）
        $sql = "select * from information_schema.COLUMNS where table_schema='" . $this->db_name . "' and table_name='" . $table . "';";
        $result = $this->conn->query($sql);
        $dict_list = array();
        while ($row = $result->fetch_assoc()) {
            $dict_list[] = $row;
        }
        return $dict_list;
    }

    /**
     * 发送接口请求，生成文档
     * @param string $title 页面标题（请保证其唯一）
     * @param string $content 页面内容（支持Markdown和HTML）
     * @param string $name 目录名（可选参数）
     * @param int $number 页面序号（默认99，越小越靠前）
     * @return array
     */
    private function apiPost($title = '', $content = '', $name = '', $number = 99)
    {
        // 接口地址，如果是自己利用开源搭建的，则接口地址为：http://xx.com/server/index.php?s=/api/item/updateByApi
        $url = 'https://www.showdoc.cc/server/api/item/updateByApi';
        // 请求参数
        $data = array(
            'api_key' => $this->api_key,
            'api_token' => $this->api_token,
            'cat_name' => $name,
            'page_title' => $title,
            'page_content' => $content,
            's_number' => $number
        );
        // 发送POST请求
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_HEADER, 0);
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 10);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
        $response = curl_exec($ch);
        curl_close($ch);
        return json_decode($response, true);
    }

    /**
     * 打印输出信息
     * @param string $msg
     */
    private function echoMsg($msg = '')
    {
        if (!empty($msg)) {
            $msg = "[" . date("Y-m-d H:i:s") . "] " . $msg . PHP_EOL;
            echo $msg;
            @ob_flush();
            @flush();
        }
    }

    /**
     * 析构函数，关闭数据库连接
     */
    public function __destruct()
    {
        $this->conn->close();
        $this->echoMsg('已关闭数据库连接');
    }
}

// 实例化类并执行
$obj = new GetMysqlDict;
$obj->run();
```

### 最后

任何的工具，都是为了方便你我他，希望大家能相处更多更好的工具以及办法，更好更快的完成工作内容，大家有什么好的想法也可以和我分享，一起集思广益，发现问题并及时解决，谢谢。