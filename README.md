# PTProxy

Turn any pluggable transport for Tor into an obfuscating TCP tunnel.

This script is compatible with PT protocol version 1 without Extended ORPort and is independent from Tor.

    Client --> PTProxy -(SOCKS5)-> pt-client --.
                                               |
    Server <-- pt-server(managed by PTProxy) <-'

## Usage

`python3 ptproxy.py [-c|-s] [config.json]`

* **Async version**: Please make sure your Python version is >= 3.4
* Install [aiosocks](https://github.com/nibrag/aiosocks/) first: `pip3 install aiosocks`
* (Optional) supports `uvloop`

This async version has higher performance than the version using threads before. To be compatible with Python 3.2 or 3.3, `git checkout v1.0` to use the older version (implemented with threads)

`-c|-s` is for overriding the `role` in the config file.

The JSON config file is explained below or in the head of `ptproxy.py`. It MUST NOT contain the comment lines. The file must be in UTF-8 encoding.

**Experimental feature**: built-in SOCKS5 server. In the server-side config, set
`"local"` to `"socks5"` (or `"socks5 username password"`).

```
{
    // Role: client|server
    "role": "server",
    // Where to store PT state files
    "state": ".",
    // For server, which address to forward
    //   can be an IP or "socks5" for a built-in SOCKS5 proxy
    // For client, which address to listen
    "local": "127.0.0.1:1080",
    // For server, which address to listen (must be an IP)
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

## Note

This only operates as a TCP proxy. If you need a HTTP/SOCKS/etc. proxy, first install related softwares on the server.

The security or obfuscation provided fully depends on the Pluggable Transport you choose. This script is only a wrapper, and is provided AS IS with ABSOLUTELY NO WARRANTY.

----------

# PTProxy

将任何用于 Tor 的传输插件做成 TCP 混淆隧道。

这个脚本兼容 Tor 传输插件协议版本 1，不支持 Extended ORPort。该脚本独立于 Tor。

    Client --> PTProxy -(SOCKS5)-> pt-client --.
                                               |
    Server <-- pt-server(managed by PTProxy) <-'

## 用法

`python3 ptproxy.py [-c|-s] [config.json]`

* **异步版本**: 请确保 Python 版本 >= 3.4
* 请先安装 [aiosocks](https://github.com/nibrag/aiosocks/): `pip3 install aiosocks`
* （可选）支持 `uvloop`

该异步版本比之前使用线程的版本性能更高。如果要兼容 Python 3.2 或 3.3， `git checkout v1.0` 来使用旧版本（用线程实现）

使用 `-c|-s` 参数可覆盖配置文件中 `role` 的值。

以下是对 JSON 配置文件的解释（在 `ptproxy.py` 的头部也有）。配置文件中**不能**包含注释行，必须使用 UTF-8 编码。

**实验性功能**: 内置 SOCKS5 服务器。在服务端配置中，将
`"local"` 设置为 `"socks5"` （或 `"socks5 username password"`）。

```
{
    // 指定工作模式: client|server 客户端或服务器
    "role": "server",
    // 传输插件状态文件储存位置
    "state": ".",
    // 对于服务器，指定要转发的地址
    //   可以是 IP，或可以是 "socks5" 来打开内置 SOCKS5 代理
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

## 注意

这个项目仅能作为 TCP 连接代理。如果你需要一个 HTTP/SOCKS 等代理，请先在服务器上安装相应的软件。

该脚本提供的安全性或混淆程度完全依赖于你选用的传输插件，它只作为一层包装。该脚本“依样”提供，**不做任何担保**。
