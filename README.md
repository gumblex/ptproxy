# PTProxy

　　Turn any pluggable transport for Tor into a obfuscating TCP proxy.

　　This script is compatible with PT protocol version 1 without Extended ORPort and is independent from Tor.

## Python version

　　`python3 ptproxy.py [-c|-s] [config.json]`

　　* No external programs needed.
　　* [PySocks](https://github.com/Anorov/PySocks) is included for SOCKS4/5 communication with Tor.

　　`-c|-s` is for overriding the `role` in the config file.

　　The JSON config file is explained below or in the head of `ptproxy.py`. It must not contain the comment lines.

```
{
    # Role: client|server
    "role": "server",
    # Where to store PT state files
    "state": ".",
    # For server, which address to forward
    # For client, which address to listen
    "local": "127.0.0.1:1080",
    # For server, which address to listen
    # For client, write the IP of your server,and the port is the listening port of your server
    "server": "0.0.0.0:23456",
    # The PT command line
    "ptexec": "obfs4proxy -logLevel=ERROR -enableLogging=true",
    # The PT name, must be only one
    "ptname": "obfs4",
    # [Client] PT arguments
    "ptargs": "cert=AAAAAAAAAAAAAAAAAAAAAAAAAAAAA+AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA;iat-mode=1",
    # [Optional][Server] PT options
    # <key>=<value> [;<key>=<value> ...]
    "ptserveropt": "",
    # [Optional][Client] Which outgoing proxy must PT use
    # <proxy_type>://[<user_name>][:<password>][@]<ip>:<port>
    "ptproxy": ""
}
```
　　Note：When you start your server,you'll see something like this：
```
2015-09-11 21:49:16 Starting PT…
===== Server information =====
“server”: “xxx.xxx.xxx.xxx:xxxxx”,
“ptname”: “obfs4”,
“ptargs”:  “cert=balabalabala;iat-mode=1”,
==============================
2015-09-11 21:49:16 PT started successfully.
```
　　Please copy "cert=xxxxxx"，and paste it to the same position of `ptargs` in your client config file.
## Original Bash version: `ptproxy.sh`.
__Deprecated: `socat` doesn't have full SOCKS5 support at present.__

### Usage

　　`./ptproxy.sh {-c|-s} [server] [bind_ip] [bind_port] [pt_args]`

　　* `-c` for client
　　* `-s` for server

　　Before executing the script, you need to first edit the variables listed in the script. Some can be overriden on the command line.

### Dependencies

　　* bash, awk
　　* `socat` (client)
　　* the Pluggable Transport you need

## Note

　　This only operates as a TCP proxy. If you need a HTTP/SOCKS/etc. proxy, first install related softwares on the server.

　　The security or obfuscation provided fully depends on the Pluggable Transport you choose. This script is only a wrapper, and is provided AS IS with ABSOLUTELY NO WARRANTY.

----------

# PTProxy

　　将Tor的传输插件做成混淆TCP代理。

　　这个脚本可以在没有Extended ORPort的情况下兼容传输协议协议版本1，并且独立于Tor。
## Python 版

　　`python3 ptproxy.py [-c|-s] [config.json]`

　　* 不需要外部程序。
　　* 使用[PySocks](https://github.com/Anorov/PySocks) 与Tor通信。

　　注意：`-c|-s` 参数会覆盖配置文件中 `role` 的值。


　　以下是对json配置文件的解释(在`ptproxy.py`的头部也有)。配置文件中**不能**包含注释行。
```
{
    # 指定工作模式: client|server
    "role": "server",
    # 存放传输插件状态文件的位置
    "state": ".",
    # 对于服务器，指定要混淆的端口
    # 对于客户端，指定本地监听端口
    "local": "127.0.0.1:1080",
    # 对于服务器，指定服务端监听端口
    # 对于客户端，IP填写服务端地址，端口与服务端配置中的server段一致
    "server": "0.0.0.0:23456",
    # 传输插件的命令行
    "ptexec": "obfs4proxy -logLevel=ERROR -enableLogging=true",
    # 所使用的传输插件名称，必须唯一
    "ptname": "obfs4",
    # [客户端] 传输插件的参数；推荐将iat-mode设置为1或者2，要与服务器一致
    "ptargs": "cert=AAAAAAAAAAAAAAAAAAAAAAAAAAAAA+AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA;iat-mode=1",
    # [可选][服务端] 传输插件的选项
    # <key>=<value> [;<key>=<value> ...]
    "ptserveropt": "",
    # [可选][客户端] 前置代理(只有当你需要通过代理连接到服务器时使用)
    # <代理类型>://[<用户名>][:<密码>][@]<ip>:<端口>
    "ptproxy": ""
}
```
　　注意：服务端启动后，会输出类似如下内容：
```
2015-09-11 21:49:16 Starting PT…
===== Server information =====
“server”: “xxx.xxx.xxx.xxx:xxxxx”,
“ptname”: “obfs4”,
“ptargs”:  “cert=balabalabala;iat-mode=1”,
==============================
2015-09-11 21:49:16 PT started successfully.
```
　　此时请复制`"cert=xxxx"`，并粘贴到客户端配置文件中`ptargs`选项的同样位置。
## 原始Bash版: `ptproxy.sh`.
__已废弃: `socat` 目前对Socks5支持不完整。__

### 用法

　　`./ptproxy.sh {-c|-s} [server] [bind_ip] [bind_port] [pt_args]`

　　* `-c` 客户端
　　* `-s` 服务端


　　在执行该脚本之前，你需要编辑脚本中列出的变量。一些变量可以被命令行参数覆盖。
### 依赖

　　* bash, awk
　　* `socat` (客户端)
　　* 你需要的传输插件

## 注意

　　这个项目仅能建立TCP连接代理。如果你需要一个HTTP/SOCKS等代理，请先在你的服务器上安装对应的软件。

　　该混淆代理的安全性完全依赖于你选用的传输插件。这个脚本只是简单调用了传输插件进行混淆，不对安全性提供任何保障。
