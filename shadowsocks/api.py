#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, \
    with_statement

import os
import sys
from multiprocessing import Process

from shadowsocks import asyncdns, tcprelay, udprelay, eventloop, shell

# 对外提供API服务代码
# 具体要求是 当接收到 一个uid和相关配置后，启动监听和事件

__all__ = ['start_server', 'stop_server', 'is_server_started']

p = dict()


def call_back(port, data_len):
    print(port, data_len)


def start_server(uid, port, password, crypt_name):
    def handler():
        config = {
            "password": password,
            "method": crypt_name,
            "server_port": port,
            "timeout": 60,
            "server": "::",
            "fast_open": False
        }

        try:
            loop = eventloop.EventLoop()

            dns_resolver = asyncdns.DNSResolver()
            tcp_server = tcprelay.TCPRelay(config, dns_resolver, False, stat_callback=call_back)
            udp_server = udprelay.UDPRelay(config, dns_resolver, False)

            dns_resolver.add_to_loop(loop)
            tcp_server.add_to_loop(loop)
            udp_server.add_to_loop(loop)

            loop.run()
        except IOError as e:
            if e.errno == 98:
                sys.exit(1)
        except Exception as e:
            shell.print_exception(e)
            sys.exit(1)

    if is_server_started(uid):
        stop_server(uid)
    prs = Process(target=handler, name=uid)
    prs.daemon = True
    prs.start()
    p[uid] = prs
    return prs.pid


def is_server_started(uid):
    if uid in p.keys() and p[uid].is_alive():
        return True
    return False


def stop_server(uid):
    if uid in p.keys():
        os.kill(p[uid].pid, 4)
