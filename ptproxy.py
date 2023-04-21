#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
PTProxy - Turn any pluggable transport for Tor into an obfuscating TCP tunnel.

Copyright (c) 2015-2016 Dingyuan Wang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import os
import sys
import time
import json
import shlex
import asyncio
import threading
import subprocess

import aiosocks

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

# Default config
# If config file is not specified on the command line, this is used instead.

CFG = {
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

# End

TRANSPORT_VERSIONS = ('1',)

startupinfo = None
if os.name == 'nt':
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

logtime = lambda: time.strftime('%Y-%m-%d %H:%M:%S')

class PTConnectFailed(Exception):
    pass


async def proxy_data(reader, writer):
    try:
        while 1:
            buf = await reader.read(4096)
            if not buf:
                break
            writer.write(buf)
            await writer.drain()
        writer.close()
    except Exception as ex:
        print(logtime(), ex)

async def proxied_connection(dst, proxy_type=None, addr=None, port=None, rdns=True, username=None, password=None):
    if proxy_type == 'SOCKS4':
        socks4_addr = aiosocks.Socks4Addr(addr, port)
        socks4_auth = aiosocks.Socks4Auth(username)
        return await aiosocks.open_connection(socks4_addr, socks4_auth, dst, remote_resolve=rdns)
    elif proxy_type == 'SOCKS5':
        socks5_addr = aiosocks.Socks5Addr(addr, port)
        socks5_auth = aiosocks.Socks5Auth(username, password)
        return await aiosocks.open_connection(socks5_addr, socks5_auth, dst, remote_resolve=rdns)
    else:
        return await asyncio.open_connection(*dst)

async def handle_client(client_reader, client_writer):
    host, port = CFG['server'].rsplit(':', 1)
    try:
        remote_reader, remote_writer = await proxied_connection(
            (host, int(port)), *CFG['_ptcli'])
    except aiosocks.SocksError as ex:
        print(logtime(), ex)
        print(logtime(), 'WARNING: Please check the config and the log of PT.')
        return
    asyncio.ensure_future(proxy_data(client_reader, remote_writer))
    asyncio.ensure_future(proxy_data(remote_reader, client_writer))

def ptenv():
    env = os.environ.copy()
    env['TOR_PT_STATE_LOCATION'] = CFG['state']
    env['TOR_PT_MANAGED_TRANSPORT_VER'] = ','.join(TRANSPORT_VERSIONS)
    if CFG["role"] == "client":
        env['TOR_PT_CLIENT_TRANSPORTS'] = CFG['ptname']
        if CFG.get('ptproxy'):
            env['TOR_PT_PROXY'] = CFG['ptproxy']
    elif CFG["role"] == "server":
        env['TOR_PT_SERVER_TRANSPORTS'] = CFG['ptname']
        env['TOR_PT_SERVER_BINDADDR'] = '%s-%s' % (
            CFG['ptname'], CFG['server'])
        env['TOR_PT_ORPORT'] = CFG['local']
        env['TOR_PT_EXTENDED_SERVER_PORT'] = ''
        if CFG.get('ptserveropt'):
            env['TOR_PT_SERVER_TRANSPORT_OPTIONS'] = ';'.join(
                '%s:%s' % (CFG['ptname'], kv) for kv in CFG['ptserveropt'].split(';'))
    else:
        raise ValueError('"role" must be either "server" or "client"')
    return env


def checkproc():
    global PT_PROC
    if PT_PROC is None or PT_PROC.poll() is not None:
        PT_PROC = subprocess.Popen(shlex.split(
            CFG['ptexec']), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, env=ptenv(), startupinfo=startupinfo)
    return PT_PROC


def parseptline(iterable):
    global CFG
    for ln in iterable:
        ln = ln.decode('utf_8', errors='replace').rstrip('\n')
        sp = ln.split(' ', 1)
        kw = sp[0]
        if kw in ('ENV-ERROR', 'VERSION-ERROR', 'PROXY-ERROR',
                  'CMETHOD-ERROR', 'SMETHOD-ERROR'):
            raise PTConnectFailed(ln)
        elif kw == 'VERSION':
            if sp[1] not in TRANSPORT_VERSIONS:
                raise PTConnectFailed('PT returned invalid version: ' + sp[1])
        elif kw == 'PROXY':
            if sp[1] != 'DONE':
                raise PTConnectFailed('PT returned invalid info: ' + ln)
        elif kw == 'CMETHOD':
            vals = sp[1].split(' ')
            if vals[0] == CFG['ptname']:
                host, port = vals[2].split(':')
                CFG['_ptcli'] = (
                    vals[1].upper(), host, int(port),
                    True, CFG['ptargs'][:255], CFG['ptargs'][255:] or '\0')
        elif kw == 'SMETHOD':
            vals = sp[1].split(' ')
            if vals[0] == CFG['ptname']:
                print('===== Server information =====')
                print('"server": "%s",' % vals[1])
                print('"ptname": "%s",' % vals[0])
                for opt in vals[2:]:
                    if opt.startswith('ARGS:'):
                        print('"ptargs": "%s",' % opt[5:].replace(',', ';'))
                print('==============================')
        elif kw in ('CMETHODS', 'SMETHODS') and sp[1] == 'DONE':
            print(logtime(), 'PT started successfully.')
            return
        else:
            # Some PTs may print extra debugging info
            print(logtime(), ln)


def runpt():
    global CFG, PTREADY
    while CFG.get('_run', True):
        print(logtime(), 'Starting PT...')
        proc = checkproc()
        # If error then die
        parseptline(proc.stdout)
        PTREADY.set()
        # Use this to block
        # stdout may be a channel for logging
        try:
            out = proc.stdout.readline()
            while out:
                print(logtime(), out.decode('utf_8', errors='replace').rstrip('\n'))
        except BrokenPipeError:
            pass
        PTREADY.clear()
        print(logtime(), 'PT died.')

PT_PROC = None
PTREADY = threading.Event()

def main():
    global CFG, PTREADY, PT_PROC
    try:
        if len(sys.argv) == 1:
            pass
        elif len(sys.argv) == 2:
            if sys.argv[1] in ('-h', '--help'):
                print('usage: python3 %s [-c|-s] [config.json]' % __file__)
                return 0
            else:
                CFG = json.load(open(sys.argv[1], 'r', encoding='utf-8'))
        elif len(sys.argv) == 3:
            CFG = json.load(open(sys.argv[2], 'r', encoding='utf-8'))
            if sys.argv[1] == '-c':
                CFG['role'] = 'client'
            elif sys.argv[1] == '-s':
                CFG['role'] = 'server'
    except Exception as ex:
        print(ex)
        print('usage: python3 %s [-c|-s] [config.json]' % sys.argv[0])
        return 1

    #loop = None

    try:
        CFG['_run'] = True
        if CFG['role'] == 'client':
            ptthr = threading.Thread(target=runpt)
            ptthr.daemon = True
            ptthr.start()
            PTREADY.wait()
            host, port = CFG['local'].split(':')
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                asyncio.start_server(handle_client, host=host, port=int(port)))
            loop.run_forever()
        elif CFG['local'].startswith('socks5'):
            from socksserver import SOCKS5Server
            sockssrv = SOCKS5Server('127.0.0.1', 0, *CFG['local'].split(' ')[1:])
            CFG['local'] = '127.0.0.1:%d' % sockssrv.port
            ptthr = threading.Thread(target=runpt)
            ptthr.daemon = True
            ptthr.start()
            sockssrv.run_forever()
        else:
            runpt()
    except KeyboardInterrupt:
        pass
    finally:
        CFG['_run'] = False
        if PT_PROC:
            PT_PROC.kill()
        # No long list of destroyed tasks
        #if loop:
            #loop.close()
    return 0

if __name__ == '__main__':
    sys.exit(main())
