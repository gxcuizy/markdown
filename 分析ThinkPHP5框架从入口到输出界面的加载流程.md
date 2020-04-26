---
title: 分析ThinkPHP5框架从入口到输出界面的加载流程
date: 2020-04-21 13:58:19
tags: [PHP, 程序员]
---

![](https://image-static.segmentfault.com/184/515/1845150031-5ea145cc3fcfb_articlex)

### 安装ThinkPHP

怎么安装，我就不细说了，[官方文档-安装ThinkPHP](https://www.kancloud.cn/manual/thinkphp5/118006)说的很全了，可以通过Composer、Git或者直接去[ThinkPHP官网下载](http://www.thinkphp.cn/down.html)zip包，我安装的版本是5.0.24

### 测试运行

下载安装完毕后，如果项目是下载目录是你本地服务器的项目根目录下，可以直接在浏览器输入地址`http://localhost/thinkphp5/public/`，就可以进入到ThinkPHP5的默认欢迎页，如下图所示，这就说明ThinkPHP5已经安装成功

<!-- more -->

![](https://image-static.segmentfault.com/150/172/1501722930-5e9d597b67275_articlex)

除了上面的这个方式的地址运行，我们也可以通过Apache或者Nginx配置虚拟主机实现项目的访问，有兴趣的可以网上查看具体教程，然后配置虚拟主机进行访问。

下面进入正题，我们来逐步分析ThinkPHP5的执行流程……

### 入口文件（public\index.php）

打开`public\index.php`文件后，我们可以看到，入口文件原始代码如下

```php
// [ 应用入口文件 ]

// 定义应用目录
define('APP_PATH', __DIR__ . '/../application/');
// 加载框架引导文件
require __DIR__ . '/../thinkphp/start.php';
```

入口文件代码很简洁，就两行代码，作用分别为
1. `define('APP_PATH', __DIR__ . '/../application/');`定义应用目录的常量APP_PATH
2. `require __DIR__ . '/../thinkphp/start.php';`加载框架引导文件

除了上面的这两个作用外，我们还可以额外在入口文件中，定义我们自己的常量，例如添加一行代码`define('PUBLIC_PATH', __DIR__ .'/../public');`定义public目录的常量以及一些预处理等

### 加载框架引导文件（thinkphp\start.php）

同样的，进入`thinkphp\start.php`文件后，我们可以知道，代码并不多

```php
namespace think;

// ThinkPHP 引导文件
// 1. 加载基础文件
require __DIR__ . '/base.php';

// 2. 执行应用
App::run()->send();
```

从这简短的两行代码，我们可以看到，主要左右有两个
1. `require __DIR__ . '/base.php';`加载基础文件
2. `App::run()->send();`执行应用

下面两个大点，将具体介绍这两个左右都做了什么

### 加载基础文件（thinkphp\base.php）

我们继续打开`thinkphp\base.php`文件，发现这个文件终于不再像前两个文件那样，只有两行代码了……

```php
define('THINK_VERSION', '5.0.24');
define('THINK_START_TIME', microtime(true));
define('THINK_START_MEM', memory_get_usage());
define('EXT', '.php');
define('DS', DIRECTORY_SEPARATOR);
defined('THINK_PATH') or define('THINK_PATH', __DIR__ . DS);
define('LIB_PATH', THINK_PATH . 'library' . DS);
define('CORE_PATH', LIB_PATH . 'think' . DS);
define('TRAIT_PATH', LIB_PATH . 'traits' . DS);
defined('APP_PATH') or define('APP_PATH', dirname($_SERVER['SCRIPT_FILENAME']) . DS);
defined('ROOT_PATH') or define('ROOT_PATH', dirname(realpath(APP_PATH)) . DS);
defined('EXTEND_PATH') or define('EXTEND_PATH', ROOT_PATH . 'extend' . DS);
defined('VENDOR_PATH') or define('VENDOR_PATH', ROOT_PATH . 'vendor' . DS);
defined('RUNTIME_PATH') or define('RUNTIME_PATH', ROOT_PATH . 'runtime' . DS);
defined('LOG_PATH') or define('LOG_PATH', RUNTIME_PATH . 'log' . DS);
defined('CACHE_PATH') or define('CACHE_PATH', RUNTIME_PATH . 'cache' . DS);
defined('TEMP_PATH') or define('TEMP_PATH', RUNTIME_PATH . 'temp' . DS);
defined('CONF_PATH') or define('CONF_PATH', APP_PATH); // 配置文件目录
defined('CONF_EXT') or define('CONF_EXT', EXT); // 配置文件后缀
defined('ENV_PREFIX') or define('ENV_PREFIX', 'PHP_'); // 环境变量的配置前缀

// 环境常量
define('IS_CLI', PHP_SAPI == 'cli' ? true : false);
define('IS_WIN', strpos(PHP_OS, 'WIN') !== false);

// 载入Loader类
require CORE_PATH . 'Loader.php';

// 加载环境变量配置文件
if (is_file(ROOT_PATH . '.env')) {
    $env = parse_ini_file(ROOT_PATH . '.env', true);

    foreach ($env as $key => $val) {
        $name = ENV_PREFIX . strtoupper($key);

        if (is_array($val)) {
            foreach ($val as $k => $v) {
                $item = $name . '_' . strtoupper($k);
                putenv("$item=$v");
            }
        } else {
            putenv("$name=$val");
        }
    }
}

// 注册自动加载
\think\Loader::register();

// 注册错误和异常处理机制
\think\Error::register();

// 加载惯例配置文件
\think\Config::set(include THINK_PATH . 'convention' . EXT);
```
仔细一看，发现代码虽然有六十多行，但是，代码的作用却显而易见，作用主要有以下六点

1. 使用`define('', '')`函数定义了很多个系统常量，外加两个环境常量
2. 引入loader类（thinkphp\library\think\loader.php），供后续使用
3. 加载环境变量配置文件（环境变量配置文件名为`.env`，这个文件不一定存在，都是在实际开发过程中根据需要加上去的）
4. 调用`\think\Loader::register()`注册自动加载机制
	- 注册系统自动加载
	- `Composer`自动加载支持
	- 注册命名空间定义
	- 加载类库映射文件，存在于`runtime`缓存目录下`classmap.php`
	- 自动加载`extend`目录
5. 调用`\think\Error::register()`注册异常和错误处理机制
6. 加载惯例配置文件（thinkphp\convention.php）

### 执行应用（thinkphp\library\think\App.php）下的run方法

为了方便，这个run方法的代码虽然有点长，但是我还是选择把整个方法贴出来，别打我哈

```php
/**
 * 执行应用程序
 * @access public
 * @param  Request $request 请求对象
 * @return Response
 * @throws Exception
 */
public static function run(Request $request = null)
{
    $request = is_null($request) ? Request::instance() : $request;

    try {
        $config = self::initCommon();

        // 模块/控制器绑定
        if (defined('BIND_MODULE')) {
            BIND_MODULE && Route::bind(BIND_MODULE);
        } elseif ($config['auto_bind_module']) {
            // 入口自动绑定
            $name = pathinfo($request->baseFile(), PATHINFO_FILENAME);
            if ($name && 'index' != $name && is_dir(APP_PATH . $name)) {
                Route::bind($name);
            }
        }

        $request->filter($config['default_filter']);

        // 默认语言
        Lang::range($config['default_lang']);
        // 开启多语言机制 检测当前语言
        $config['lang_switch_on'] && Lang::detect();
        $request->langset(Lang::range());

        // 加载系统语言包
        Lang::load([
            THINK_PATH . 'lang' . DS . $request->langset() . EXT,
            APP_PATH . 'lang' . DS . $request->langset() . EXT,
        ]);

        // 监听 app_dispatch
        Hook::listen('app_dispatch', self::$dispatch);
        // 获取应用调度信息
        $dispatch = self::$dispatch;

        // 未设置调度信息则进行 URL 路由检测
        if (empty($dispatch)) {
            $dispatch = self::routeCheck($request, $config);
        }

        // 记录当前调度信息
        $request->dispatch($dispatch);

        // 记录路由和请求信息
        if (self::$debug) {
            Log::record('[ ROUTE ] ' . var_export($dispatch, true), 'info');
            Log::record('[ HEADER ] ' . var_export($request->header(), true), 'info');
            Log::record('[ PARAM ] ' . var_export($request->param(), true), 'info');
        }

        // 监听 app_begin
        Hook::listen('app_begin', $dispatch);

        // 请求缓存检查
        $request->cache(
            $config['request_cache'],
            $config['request_cache_expire'],
            $config['request_cache_except']
        );

        $data = self::exec($dispatch, $config);
    } catch (HttpResponseException $exception) {
        $data = $exception->getResponse();
    }

    // 清空类的实例化
    Loader::clearInstance();

    // 输出数据到客户端
    if ($data instanceof Response) {
        $response = $data;
    } elseif (!is_null($data)) {
        // 默认自动识别响应输出类型
        $type = $request->isAjax() ?
        Config::get('default_ajax_return') :
        Config::get('default_return_type');

        $response = Response::create($data, $type);
    } else {
        $response = Response::create();
    }

    // 监听 app_end
    Hook::listen('app_end', $response);

    return $response;
}
```

这大概90行的代码，具体做了什么呢，结合注释分析，主要有以下几步的功能

- 第一步：处理变量`$request`，保证有效有用不为null
- 第二步：`self::initCommon()`调用当前控制器中的initCommon()方法，负责初始化应用，并返回配置信息
	- `Loader::addNamespace(self::$namespace, APP_PATH);`注册命名空间
	- `self::init()`调用本类的init()方法初始化应用
    	- 加载各种配置文件
    	- 加载行为扩展文件
    	- 加载公共文件
    	- 加载语言包
    - 应用调试模式相关处理
    - 加载额外文件，通过配置项`extra_file_list`的值去加载相关文件
	- `date_default_timezone_set($config['default_timezone']);`设置系统时区
	- 调用`Hook::listen('app_init');`监听app_init标签的行为
- 第三步：判断是否进行模块或者控制器的绑定
- 第四步：系统语言设置和加载
- 第五步：`self::routeCheck($request, $config)`加载当前控制器的routeCheck()方法进行路由检测
	- 先进行路由地址配置检测，先读取缓存路由，不存在再导入路由文件配置
	- 无路由配置，直接解析模块/控制器/操作
	- 返回module模块信息（模块名、控制器名和操作方法名）
- 第六步：开启调试模式下，记录路由和请求信息的日志
- 第七步：`self::exec($dispatch, $config)`调用控制器中的exec()方法执行调用分发
	- 根据用户请求类型进行分发处理，这里是module模块类型
	- 调用`self::module()`执行模块，进行模块部署和初始化，获取和设置当前控制器名和操作名
- 第八步：清空类的实例化，并输出相应格式的数据到客户端，即用户看到的输出界面

### 总结

本文大概解析了ThinkPHP5的基础执行流程，有说的不到位的，也不用给我说了，因为我也不会补上去的，就是这么皮；但是如果是说错的呢，麻烦指出来，我肯定会加以改正的，就这么耿直。对了，如果觉得对你有帮助，点个赞再走呗，感谢！