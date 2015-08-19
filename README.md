# PTProxy

Turn any pluggable transport for Tor into a obfuscating TCP proxy.

This script is compatible with PT protocol version 1 without Extended ORPort and is independent from Tor.

## Python version

`python3 ptproxy.py [-c|-s] [config.json]`

* No external programs needed.
* [PySocks](https://github.com/Anorov/PySocks) is included for SOCKS4/5 communication with Tor.

The JSON config file is explained in the head of `ptproxy.py`.

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
