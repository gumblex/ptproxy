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
    # For client, which address to connect
    "server": "0.0.0.0:23456",
    # The PT command line
    "ptexec": "obfs4proxy -logLevel=ERROR -enableLogging=true",
    # The PT name, must be only one
    "ptname": "obfs4",
    # [Client] PT arguments
    "ptargs": "cert=AAAAAAAAAAAAAAAAAAAAAAAAAAAAA+AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA;iat-mode=0",
    # [Optional][Server] PT options
    # <key>=<value> [;<key>=<value> ...]
    "ptserveropt": "",
    # [Optional][Client] Which outgoing proxy must PT use
    # <proxy_type>://[<user_name>][:<password>][@]<ip>:<port>
    "ptproxy": ""
}
```

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
