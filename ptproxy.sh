#!/bin/bash

# Client --> socat(SOCKS) --> pt-cli -------> pt-server --> Server
#                                    Internet

USAGE='usage: ./ptproxy.sh {-c|-s} [server] [bind_ip] [bind_port] [pt_args]'

##### Edit these variables #####
# Where to store PT state files
STATE_LOCATION=.
# For server, which address to forward
# For client, which address to listen
PROXY_BIND=127.0.0.1
PROXY_PORT=9234
# For server, which address to listen
# For client, which address to connect
SERVER=127.0.0.1:12346
# The PT command line
TRANSPORT_EXEC="obfs4proxy -logLevel=ERROR -enableLogging=true"
# The PT name, must be only one
TRANSPORT_NAME=obfs4
# Client only
TRANSPORT_ARGS="cert=AAAAAAAAAAAAAAAAAAAAAAAAAAAAA+AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA;iat-mode=0"
# socat executable
# version 2.0+ required if the PT client uses SOCKS5
SOCAT=socat
##### End ######################

PT_OUT='ptout.txt'

export TOR_PT_STATE_LOCATION="$STATE_LOCATION"
export TOR_PT_MANAGED_TRANSPORT_VER=1

ptclient () {
	trap 'kill $(jobs -p)' EXIT
	AWK_SCRIPT='BEGIN {start = 1} {if ($1 == "CMETHOD" && start) {split($4, socks, ":"); print "'"$SOCAT -ddd TCP-LISTEN:$PROXY_PORT,bind=$PROXY_BIND,reuseaddr,fork "'" toupper($3) ":" socks[1] "'":$SERVER,socksport="'" socks[2] "'",socksuser=$TRANSPORT_ARGS"'"; start = 0}}'
	(while true; do $TRANSPORT_EXEC | tee "$PT_OUT"; done) &
	sleep 1
	EXEC_CMD=$(awk "$AWK_SCRIPT" "$PT_OUT")
	echo $EXEC_CMD
	$EXEC_CMD
}

ptserver () {
	set -m
	AWK_SCRIPT='BEGIN {start = 1} {if ($1 == "SMETHOD" && start) {split($4, ptarg, ":"); ptarg1=ptarg[2]; gsub(",", ";", ptarg1); print "SERVER=" $3; print "TRANSPORT_ARGS=\"" ptarg1 "\""; start = 0}}'
	$TRANSPORT_EXEC | tee "$PT_OUT" &
	sleep 1
	echo "===== Client config ====="
	awk "$AWK_SCRIPT" "$PT_OUT"
	echo "========================="
	fg 1
}

if [ -n "$2" ]; then
	SERVER="$2"
fi

if [ -n "$3" ]; then
	PROXY_BIND="$3"
fi

if [ -n "$4" ]; then
	PROXY_PORT="$4"
fi

if [ -n "$5" ]; then
	TRANSPORT_ARGS="$5"
fi

if [ "$1" = "-c" ]; then
	export TOR_PT_CLIENT_TRANSPORTS=$TRANSPORT_NAME
	ptclient
elif [ "$1" = "-s" ]; then
	export TOR_PT_EXTENDED_SERVER_PORT=
	export TOR_PT_ORPORT=$PROXY_BIND:$PROXY_PORT
	export TOR_PT_SERVER_BINDADDR=$TRANSPORT_NAME-$SERVER
	export TOR_PT_SERVER_TRANSPORTS=$TRANSPORT_NAME
	ptserver
else
	echo "$USAGE"
	exit 1
fi

