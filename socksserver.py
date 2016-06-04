#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import socket
import struct
import asyncio

@asyncio.coroutine
def proxy_data(reader, writer):
    try:
        while 1:
            buf = yield from reader.read(4096)
            if not buf:
                break
            writer.write(buf)
            yield from writer.drain()
        writer.close()
    except Exception:
        pass

class SOCKS5Server:

    def __init__(self, host, port, username=None, password=None, *, loop=None):
        self.username = self.password = None
        if username and password:
            self.username = username.encode('utf-8')
            self.password = password.encode('utf-8')

        self.loop = loop or asyncio.get_event_loop()
        coro = asyncio.start_server(self.handle_socks, host, port, loop=self.loop)
        self.server = self.loop.run_until_complete(coro)
        # for random ports
        self.host, self.port = self.server.sockets[0].getsockname()[:2]

    def handle_socks(self, reader, writer):
        version, authnum = yield from reader.read(2)
        if version != 0x05:
            writer.close()
            return
        methods = yield from reader.read(authnum)
        if self.username and 0x02 in methods:
            # Username/password
            writer.write(b'\x05\x02')
            version, ulen = yield from reader.read(2)
            username = yield from reader.read(ulen)
            ulen = (yield from reader.read(1))[0]
            password = yield from reader.read(ulen)
            if version == 0x01 and (
                username == self.username and password == self.password):
                writer.write(b'\x01\x00')
            else:
                writer.write(b'\x01\xFF')
                writer.close()
                return
        elif self.username is None and 0x00 in methods:
            # No authentication
            writer.write(b'\x05\x00')
        else:
            writer.write(b'\x05\xFF')
            writer.close()
            return

        version, command, reserved, addrtype = yield from reader.read(4)
        if version != 0x05:
            writer.close()
            return
        if addrtype == 0x01:
            host = yield from reader.read(4)
            hostname = socket.inet_ntop(socket.AF_INET, host)
        elif addrtype == 0x03:
            length = (yield from reader.read(1))[0]
            hostname = (yield from reader.read(length)).decode('utf-8')
        elif addrtype == 0x04:
            host = yield from reader.read(16)
            hostname = socket.inet_ntop(socket.AF_INET6, host)
        port = struct.unpack('!H', (yield from reader.read(2)))[0]

        sockname = writer.get_extra_info('sockname')
        # a (address, port) 2-tuple for AF_INET,
        # a (address, port, flow info, scope id) 4-tuple for AF_INET6
        if len(sockname) == 2:
            bndinfo = b'\x01' + socket.inet_pton(socket.AF_INET, sockname[0])
        else:
            bndinfo = b'\x04' + socket.inet_pton(socket.AF_INET6, sockname[0])
        bndinfo += struct.pack('!H', sockname[1])
        if command == 0x01:
            writer.write(b'\x05\x00\x00' + bndinfo)
        else:
            writer.write(b'\x05\x07\x00' + bndinfo)
            writer.close()
            return

        r_reader, r_writer = yield from asyncio.open_connection(hostname, port)
        asyncio.async(proxy_data(reader, r_writer), loop=self.loop)
        asyncio.async(proxy_data(r_reader, writer), loop=self.loop)

    def run_forever(self):
        self.loop.run_forever()

if __name__ == '__main__':
    try:
        host = '0.0.0.0'
        port = 1080
        if len(sys.argv) == 1:
            pass
        elif len(sys.argv) == 2:
            if sys.argv[1] in ('-h', '--help'):
                print('usage: python3 %s [port|listen port]' % __file__)
                sys.exit(0)
            else:
                port = int(sys.argv[1])
        elif len(sys.argv) == 3:
            host = sys.argv[1]
            port = int(sys.argv[2])
    except Exception as ex:
        print(ex)
        print('usage: python3 %s [port|listen port]' % sys.argv[0])
        sys.exit(1)

    srv = SOCKS5Server(host, port)
    print('Listening on %s:%d' % (host, port))
    try:
        srv.run_forever()
    except KeyboardInterrupt:
        pass
