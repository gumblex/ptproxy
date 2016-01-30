# PTProxy

Turn any pluggable transport for Tor into a obfuscating TCP proxy.

This script is compatible with PT protocol version 1 without Extended ORPort and is independent from Tor.

## Python version

`python3 ptproxy.py [-c|-s] [config.json]`

* No external programs needed.
* [PySocks](https://github.com/Anorov/PySocks) is included for SOCKS4/5 communication with PTs.

`-c|-s` is for overriding the `role` in the config file.

The JSON config file is explained below or in the head of `ptproxy.py`. It MUST NOT contain the comment lines. The file must be in UTF-8 encoding.

```
{
    // Role: client|server
    "role": "server",
    // Where to store PT state files
    "state": ".",
    // For server, which address to forward
    // For client, which address to listen
    "local": "127.0.0.1:1080",
    // For server, which address to listen
    // For client, the server address to connect
    "server": "0.0.0.0:23456",
    // The PT command line
    "ptexec": "obfs4proxy -logLevel=ERROR -enableLogging=true",
    // The PT name, must be only one
    "ptname": "obfs4",
    // [Client] PT arguments
    "ptargs": "cert=AAAAAAAAAAAAAAAAAAAAAAAAAAAAA+AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA;iat-mode=0",
    // [Optional][Server] PT options
    // <key>=<value> [;<key>=<value> ...]
    "ptserveropt": "",
    // [Optional][Client] Which outgoing proxy must PT use
    // <proxy_type>://[<user_name>][:<password>][@]<ip>:<port>
    "ptproxy": ""
}
```

Note：When the server starts successfully, it will print out `ptargs`. Copy and paste this value to your client config file.

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

将任何用于 Tor 的传输插件做成 TCP 混淆代理。

这个脚本兼容 Tor 传输插件协议版本 1，不支持 Extended ORPort。该脚本独立于 Tor。

## Python 版

`python3 ptproxy.py [-c|-s] [config.json]`

* 不需要外部程序。
* 已包含 [PySocks](https://github.com/Anorov/PySocks) 与传输插件通信。

使用 `-c|-s` 参数可覆盖配置文件中 `role` 的值。

以下是对 JSON 配置文件的解释（在 `ptproxy.py` 的头部也有）。配置文件中**不能**包含注释行，必须使用 UTF-8 编码。

```
{
    // 指定工作模式: client|server 客户端或服务器
    "role": "server",
    // 传输插件状态文件储存位置
    "state": ".",
    // 对于服务器，指定要转发的地址
    // 对于客户端，指定本地监听地址
    "local": "127.0.0.1:1080",
    // 对于服务器，指定服务端监听地址
    // 对于客户端，指定要连接的服务端地址
    "server": "0.0.0.0:23456",
    // 传输插件的命令行
    "ptexec": "obfs4proxy -logLevel=ERROR -enableLogging=true",
    // 传输插件名称，只能有一个
    "ptname": "obfs4",
    // [客户端] 传输插件的参数
    "ptargs": "cert=AAAAAAAAAAAAAAAAAAAAAAAAAAAAA+AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA;iat-mode=0",
    // [可选][服务端] 传输插件的选项
    // <键>=<值> [;<键>=<值> ...]
    "ptserveropt": "",
    // [可选][客户端] 传输插件前置代理
    // <代理类型>://[<用户名>][:<密码>][@]<IP>:<端口>
    "ptproxy": ""
}
```

注意：服务端成功启动后，会输出 `ptargs` 参数。请复制粘贴该值到客户端配置文件。

## 原始 Bash 版: `ptproxy.sh`.
__已废弃: `socat` 目前对 SOCKS5 支持不完整。__

### 用法

`./ptproxy.sh {-c|-s} [server] [bind_ip] [bind_port] [pt_args]`

* `-c` 客户端
* `-s` 服务端

在执行该脚本之前，你需要编辑脚本中列出的变量。一些变量可以用命令行参数覆盖。

### 依赖

* bash, awk
* `socat` (客户端)
* 你需要的传输插件

## 注意

这个项目仅能作为 TCP 连接代理。如果你需要一个 HTTP/SOCKS 等代理，请先在服务器上安装相应的软件。

该脚本提供的安全性或混淆程度完全依赖于你选用的传输插件，它只作为一层包装。该脚本“依样”提供，**不做任何担保**。
