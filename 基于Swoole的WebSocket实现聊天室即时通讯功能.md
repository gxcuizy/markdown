---
title: 基于Swoole的WebSocket实现聊天室即时通讯功能
date: 2020-06-01 13:29:31
tags: [PHP, Swoole, 聊天室, WebSocket, 即时通讯]
---

![](https://image-static.segmentfault.com/136/195/1361957441-5ed45c4b268a6_articlex)

### 前言

前段时间，不是刚搭建好本地开发环境，那怎么也得搞点事情啊，看了下[Swoole开发文档](https://wiki.swoole.com/)，就先试试WebSocket弄一下即时通讯吧，那就安排一下聊天室，开搞……

### Swoole是什么

> Swoole 是一个 PHP 的 协程 高性能 网络通信引擎，使用 C/C++ 语言编写，提供了多种通信协议的网络服务器和客户端模块。可以方便快速的实现 TCP/UDP服务、高性能Web、WebSocket服务、物联网、实时通讯、游戏、微服务等，使 PHP 不再局限于传统的 Web 领域。

从官方介绍中可以看到，`Swoole`支持`WebSocket服务`，我们就利用这个来快速开发一个简易的聊天室。

<!--more-->

### 聊天室效果

首先进入到项目根目录下，执行命令`php SwooleChat.php`开启`WebSocket`服务，然后双击`chat.html`文件在浏览器中打开，就进入了聊天界面了，就可以开始愉快的吹水了……

![](https://image-static.segmentfault.com/262/538/262538780-5ed494dd34075_articlex)

### 服务器端（SwooleChat.php）

从[官方文档-WebSocket 服务器](https://wiki.swoole.com/#/start/start_ws_server)可以看到，PHP服务器端主要有`onOpen`、 `onMessage`和`onClose`，这三个事件的作用如下：

- onOpen：监听WebSocket连接打开事件
- onMessage：监听WebSocket消息事件
- onClose：监听WebSocket连接关闭事件

#### onOpen监听WebSocket连接打开

新用户开启一个WebSocket连接，都会走`onOpen`事件，我根据官方的例子简单封装一下，用户创建连接后，用户信息存入`MySQL`数据库中，并且通知其他在线用户。对了，提醒一下，这里用到了`MySQL`，如果没有安装的，请先安装相关扩展。

```php
/**
 * 监听WebSocket连接打开
 */
private function open()
{
    $this->ws->on('open', function ($ws, $request) {
        // 用户存入数据库
        $this->initConn();
        $user_name = $request->get['user_name'];
        $fd = $request->fd;
        $sql = "INSERT INTO chat_user (fd, user_name, add_time) VALUES ($fd, '{$user_name}', " . time() . ")";
        $this->conn->query($sql);
        // 推送上线通知
        $this->return['type'] = 'on';
        $this->return['msg'] = '欢迎【' . $user_name . '】进入聊天室';
        // 用户列表
        $sql = "SELECT fd,user_name FROM chat_user WHERE online_status = 1";
        $result = $this->conn->query($sql);
        $user_list = [];
        if (mysqli_num_rows($result) > 0) {
            // 给其他用户推送上线通知
            while ($row = mysqli_fetch_assoc($result)) {
                $user_list[] = ['fd' => $row['fd'], 'name' => $row['user_name']];
                if ($row['fd'] != $fd) {
                    $this->return['data'] = ['fd' => $fd, 'name' => $user_name];
                    $ws->push($row['fd'], json_encode($this->return));
                }
            }
        }
        // 在线用户
        $this->return['type'] = 'open';
        $this->return['data'] = ['user_list' => $user_list];
        $ws->push($fd, json_encode($this->return));
    });
}
```

#### onMessage监听WebSocket消息

客户端发送的消息，需要推送给聊天室内的其他人，并且告知其他用户，这条信息是谁什么时间发送的。

```php
/**
 * 监听WebSocket消息
 */
private function message()
{
    $this->ws->on('message', function ($ws, $frame) {
        $this->initConn();
        // 聊天消息
        $fd = $frame->fd;
        $message = $frame->data;
        $this->return['type'] = 'chat';
        $this->return['msg'] = $message;
        // 用户名称
        $sql = "SELECT user_name FROM chat_user WHERE fd = {$fd} LIMIT 1";
        $res = $this->conn->query($sql);
        $user = $res->fetch_assoc();
        $user_name = $user['user_name'];
        // 用户列表
        $sql = "SELECT fd,user_name FROM chat_user WHERE online_status = 1 ORDER BY id desc";
        $result = $this->conn->query($sql);
        if (mysqli_num_rows($result) > 0) {
            // 推送发送的消息
            while ($row = mysqli_fetch_assoc($result)) {
                $this->return['data'] = ['user_name' => $user_name, 'from' => $fd, 'to' => $row['fd'], 'time' => date('Y-m-d H:i:s')];
                $ws->push($row['fd'], json_encode($this->return));
            }
        }
    });
}
```

#### onClose监听WebSocket连接关闭

当客户端连接关闭的时候，需要处理用户状态为离线，并且告知其他在线用户，该用户已下线离开聊天室。

```php
/**
 * 监听WebSocket连接关闭
 */
private function close()
{
    $this->ws->on('close', function ($ws, $fd) {
        $this->initConn();
        // 用户下线
        $sql = "UPDATE chat_user SET online_status = 0 WHERE fd = $fd";
        $this->conn->query($sql);
        // 用户名称
        $sql = "SELECT user_name FROM chat_user WHERE fd = {$fd} LIMIT 1";
        $res = $this->conn->query($sql);
        $user = $res->fetch_assoc();
        $user_name = $user['user_name'];
        // 用户列表
        $sql = "SELECT fd,user_name FROM chat_user WHERE online_status = 1 ORDER BY id desc";
        $result = $this->conn->query($sql);
        if (mysqli_num_rows($result) > 0) {
            // 给其他用户推送下线通知
            while ($row = mysqli_fetch_assoc($result)) {
                if ($row['fd'] != $fd) {
                    $this->return['type'] = 'off';
                    $this->return['msg'] = '【' . $user_name . '】离开聊天室';
                    $this->return['data'] = ['fd' => $fd];
                    $ws->push($row['fd'], json_encode($this->return));
                }
            }
        }
    });
}
```

### 客户端（chat.html）

#### HTML界面

界面，为了简单快速，我用了[Bootstrap](https://v3.bootcss.com/getting-started/)，可以快速写简单的一个聊天室页面

```html
<head>
    <meta charset="UTF-8">
    <title>聊天室</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">
</head>
<body>
<div class="container">
    <div class="row">
        <div class="page-header">
            <h2>基于Swoole的WebSocket聊天室</h2>
        </div>
        <div class="col-xs-9 col-sm-9 col-md-9">
            <div class="form-group send-message">
                <textarea name="message" rows="5" class="form-control col-xs-12 col-sm-12 col-md-12"
                          placeholder="请输入聊天内容"></textarea>
                <button type="button" class="btn btn-info btn-block send-button">发送</button>
            </div>
        </div>
        <div class="col-xs-3 col-sm-3 col-md-3">
            <h3>在线用户</h3>
            <table class="table table-hover online-user">
                <tr>
                    <th>FD编号</th>
                    <th>用户名</th>
                </tr>
            </table>
        </div>
    </div>
</div>
</body>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous">
</script>
<script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.5.1/jquery.js"></script>
```

#### JS交互

同样的，我们从实例中也看到，客户端的主要事件和服务器端是一样的，也就是，客户端建立`ws`连接后，需要处理来自于服务器端推送的各种事件对应的消息，主要处理上下线消息通知以及普通聊天消息等；为了省事，这里用户名我直接随机获取了，千万别说我懒哈。

```js
<script>
    // 随机用户名
    var user_name = 'user-' + Math.floor(Math.random() * 10000 + 1);
    // 建立ws连接
    var wsServer = 'ws://127.0.0.1:9502?user_name=' + user_name;
    var websocket = new WebSocket(wsServer);
    websocket.onmessage = function (evt) {
        var data = jQuery.parseJSON(evt.data);
        console.log(data);
        if (data.type == 'open') {
            // 刚连接，初始化用户数据
            var user_list = data.data.user_list;
            var open_html = '';
            $.each(user_list, function (k, val) {
                open_html += '<tr data-id="' + val.fd + '"><td>' + val.fd + '</td> <td>' + val.name + '</td> </tr>';
            });
            $('.online-user').append(open_html);
        } else if (data.type == 'chat') {
            // 聊天消息推送
            var is_myself = '';
            if (data.data.from == data.data.to) {
                is_myself = ' text-right';
            }
            var chat_html = '<div class="panel panel-info">' +
                    '<div class="panel-heading ' + is_myself + '">【' + data.data.user_name + '】 ' + data.data.time + '</div>' +
                    '<div class="panel-body ' + is_myself + '">' + data.msg +
                    '</div></div>';
            $('.send-message').before(chat_html);
        } else if (data.type == 'on') {
            // 新用户连接
            var on_html = '<tr data-id="' + data.data.fd + '"><td>' + data.data.fd + '</td> <td>' + data.data.name + '</td> </tr>';
            $('.online-user').append(on_html);
            // 上线欢迎
            var notice_html = '<div class="panel panel-info">' +
                    '<div class="panel-body text-center">' + data.msg +
                    '</div></div>';
            $('.send-message').before(notice_html);
        } else if (data.type == 'off') {
            // 用户关闭连接
            $('.online-user').find('tr[data-id=' + data.data.fd + ']').remove();
            // 下线提醒
            var off_html = '<div class="panel panel-info">' +
                    '<div class="panel-body text-center">' + data.msg +
                    '</div></div>';
            $('.send-message').before(off_html);
        }
    };
    websocket.onopen = function (evt) {
        console.log("Connected to WebSocket server.");
    };
    websocket.onclose = function (evt) {
        alert('服务器已断开连接，即将开始重连');
        window.location.reload();
    };
    websocket.onerror = function (evt, e) {
        console.log('Error occured: ' + evt.data);
    };
    $(".send-button").off('click').on('click', function () {
        var message = $("textarea[name=message]").val().trim();
        if (message == '') {
            alert('请输入聊天内容……');
            return false;
        }
        websocket.send(message);
        $("textarea[name=message]").val('');
    });
</script>
```

### 完整源码

为了方便，我肯定会把完整源码分享出来的，虽然上面说了一堆核心的代码，但是并凑起来运行还是挺费劲的，作为一个有良心的搬砖工人，我肯定会给大家那种只要环境没问题，就可以直接运行跑起来嗨的代码的，你可能要说了：`BB is easy, Show me the code.`，好吧，我已经把源码上传到[GitHub](https://github.com/gxcuizy/Blog/blob/master/chat)交友网站了，大家可以去上面查看即可。

* 聊天室完整源码：[https://github.com/gxcuizy/Blog/blob/master/chat](https://github.com/gxcuizy/Blog/blob/master/chat)

* 服务器端源码：[SwooleChat.php](https://github.com/gxcuizy/Blog/blob/master/chat/SwooleChat.php)

* 客户端源码：[chat.html](https://github.com/gxcuizy/Blog/blob/master/chat/chat.html)

### 总结

这只是一个简单的聊天室，仅供学习参考和交流使用，如有任何问题或者不明白的，多可以留言与我沟通，共同学习和进步，谢谢。