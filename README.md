# PTProxy

Turn any pluggable transport for Tor into a obfuscating TCP proxy.

This script is compatible with PT protocol version 1 without Extended ORPort and is independent from Tor.

It's only a bash script `ptproxy.sh`.

## Usage

`./ptproxy.sh {-c|-s} [server] [bind_ip] [bind_port] [pt_args]`

* `-c` for client
* `-s` for server

Before executing the script, you need to first edit the variables listed in the script. Some can be overriden on the command line.

## Dependencies

* bash, awk
* `socat` (client, 2.0+ for PT clients which use SOCKS5)
* the Pluggable Transport you need

## Note

This only operates as a TCP proxy. If you need a HTTP/SOCKS/etc. proxy, first install related softwares on the server, then set `SERVER` to the related address.

The security or obfuscation provided fully depends on the Pluggable Transport you choose. This script is only a wrapper, and is provided AS IS with ABSOLUTELY NO WARRANTY.
