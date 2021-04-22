## 一、简介：

```
    _____    _      _____                    
 __|___  |__| | __ |_   _|__  __ _ _ __ ___  
/ __| / / __| |/ /   | |/ _ \/ _` | '_ ` _ \ 
\__ \/ / (__|   <    | |  __/ (_| | | | | | |
|___/_/ \___|_|\_\   |_|\___|\__,_|_| |_| |_|

   __          __  _     _____                                 
   \ \        / / | |   / ____|                                
  __\ \  /\  / /__| |__| (___   ___ __ _ _ __  _ __   ___ _ __ 
 / __\ \/  \/ / _ \ '_ \\\___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
 \__ \\\  /\  /  __/ |_) |___) | (_| (_| | | | | | | |  __/ |   
 |___/ \/  \/ \___|_.__/_____/ \___\__,_|_| |_|_| |_|\___|_|   

http://www.s7ck.com    
```

 **作为一个网络安全从业人员，在测试网站目录时，常用的就是御剑，7kb等几款，使用下来始终觉得缺少了什么东西，于是重复造了一个轮子，此版本支持自定义字典，返回大小，代理IP模式，爆破模式，希望这款工具能给大家带来居多的便利，by the way，希望我们天真的努力，能换来一小部分干净努力的圈子，而不是吹逼娱乐圈，我们在努力～**

**目前平台还在持续开发中，肯定有不少问题和需要改进的地方，欢迎大佬们提交建议和Bug，也非常欢迎各位大佬Star或者是Fork**

1.敏感文件扫描

2.二次判断降低误报率

3.扫描内容规则化（支持自定义规则）

4.多目录扫描

5.爆破模式（支持自定义规则）

6.代理IP模式（支持导入和获取接口）

7.对接网络空间测绘接口（Fofa Zoomeye Quake Shodan）

程序只供交流，请勿用于非法用途，否则产生的一切后果自行承担！！!

**程序只供交流，请勿用于非法用途，否则产生的一切后果自行承担！！!**

### 开发语言

* Python3.6+

### 运行环境

* Linux
* Windows
* Mac

### 使用依赖库

* requests
* colorama
* aiohttp
* xlrd
* pyparsing
* xlsxwriter
* tldextract


### 安装
	git clone https://github.com/s7ckTeam/sWebScanner
	cd sWebScanner
	pip3 install -r requirements.txt

## 二、使用方法：

```
Usage: python3 sWebScanner.py --fofa title="admin"
Usage: python3 sWebScanner.py -f api.txt
Usage: python3 sWebScanner.py -u www.baidu.com
Usage: python3 sWebScanner.py (--fofa | -f | -u) -d dict.txt
Usage: python3 sWebScanner.py (--fofa | -f | -u) -func [a-z]{2}
Usage: python3 sWebScanner.py (--fofa | -f | -u) (-d | -func) -o txt
Usage: python3 sWebScanner.py (--fofa | -f | -u) (-d | -func) --method POST
Usage: python3 sWebScanner.py (--fofa | -f | -u) (-d | -func) --params params={{'your get params': 'value'}},json={{'your post params':'value'}},'data': {{}}
Usage: python3 sWebScanner.py (--fofa | -f | -u) (-d | -func) --porxy porxy.txt
Usage: python3 sWebScanner.py (--fofa | -f | -u) (-d | -func) --code 200,403


usage: sWebScanner.py [-h] [-fofa QUERY] [-f FILE] [-u URL] [-d DICT] [-o OUTPUT] [--method METHOD] [--params PARAMS] [--porxy PORXY]
                   [--code CODE] [-v] [--update]

Screenshot.

optional arguments:
  -h, --help            show this help message and exit
  -fofa QUERY, --fofa QUERY
                        Input your api query.
  -f FILE, --file FILE  Input your api.txt.
  -u URL, --url URL     Input your url.
  -d DIR, --dir DIR     Input your dir path.
  --method METHOD       Input your method.
  --params PARAMS       Input your params.
  --porxy PORXY         Input your porxy file.
  --code CODE           Input your code value. 200,404
  -v, --version         Show program's version number and exit.
  --update              Update the program.
```
#### 说明：
* --fofa: 通过fofaapi获取url
* -f: url文件
* --u: 单个url
* -d: 文件 （内容可以是以下类型）
  
  1. 字符串
  
  2. 正则
  
    `%\d%`

  3. 变量：
  ```
    {Domain} 为当前扫描目标域名 www.baidu.com
    {SubDomain} 为当前扫描目标子域名 www
    {DomainCenter} 为当前扫描目标域名主体 baidu
    {DomainCenterAndTld} 为当前扫描目标域名主体与后缀 baidu.com
  ```
* -func: 规则函数`[字符集]{字符位数}`
  ```
  字符集内特殊字符
  [ ]  " . - \ 需要转义，前面加转义符‘\’
  a-z可以表示a到z
  0-9可以表示0到9
  ```
* -o: 输出文件类型
  
  `默认txt，支持 txt,csv,json,xls,xlsx`
* --method: 请求方式
  
  `默认GET, 支持GET, POST, HEAD, PUT, DELETE`
* --params: 请求参数可与--method配合使用

  ```
  params={{'your get params': 'value'}},json={{'your post params':'value'}},'data': {{}}
  ```
* --porxy: 代理文件
* --code: 需要输出的状态码, 默认200,403
  

#### 相关配置更改

* API设置
  1. 在`config/config.py`中`fofaApi`设置，输入对应的`email`与`key`即可
  2. 在`config/config.py`中`Proxy_api`设置随机代理的api地址即可
  3. 在`config/config.py`中`ProxyPool`设置自己的代理地址即可***或***使用`--porxy`参数加载本地代理文件
  4. 在`config/config.py`中`Proxy_api`和`ProxyPool`如果都配置优先使用`Proxy_api`中的代理，如果都为空则不使用代理
