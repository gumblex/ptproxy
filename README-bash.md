# PTProxy (legacy)

The original bash version: `ptproxy.sh`

__Deprecated: `socat` doesn't have full SOCKS5 support at present. It also has performance issues.__

## Usage

`./ptproxy.sh {-c|-s} [server] [bind_ip] [bind_port] [pt_args]`

* `-c` for client
* `-s` for server

Before executing the script, you need to first edit the variables listed in the script. Some can be overriden on the command line.

## Dependencies

* bash, awk
* `socat` (client)
* the Pluggable Transport you need

----------

原始 Bash 版: `ptproxy.sh`.

__已废弃: `socat` 目前对 SOCKS5 支持不完整，且有性能问题。__

## 用法

`./ptproxy.sh {-c|-s} [server] [bind_ip] [bind_port] [pt_args]`

* `-c` 客户端
* `-s` 服务端

在执行该脚本之前，你需要编辑脚本中列出的变量。一些变量可以用命令行参数覆盖。

## 依赖

* bash, awk
* `socat` (客户端)
* 你需要的传输插件
