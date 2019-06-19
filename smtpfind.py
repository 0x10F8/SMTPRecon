#!/usr/bin/python3
import sys
import socket
from concurrent.futures import ThreadPoolExecutor

if len(sys.argv) != 2:
    print(
        "usage: smtpfind.py [IP RANGE] (e.g. smtpfind.py 10.1.1.1-10.1.1.254")
    exit(1)


def get_ip_range(iprange):
    tokenized = iprange.split('-')
    return (tokenized[0], tokenized[1])


def get_network_address(ip):
    tokenized = ip.split('.')
    return '%s.%s.%s' % (tokenized[0], tokenized[1], tokenized[2])


def get_last_octate(ip):
    return int(ip.split('.')[3])


def try_server(ip_address):
    try:
        with(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.settimeout(1)
            s.connect((ip_address, 25))
            banner = s.recv(1024)
            print("[+] %s %s" % (ip_address, banner))
    except:
        pass


iprange = sys.argv[1]
(firstip, lastip) = get_ip_range(iprange)
network_address = get_network_address(firstip)
first_octate = get_last_octate(firstip)
last_octate = get_last_octate(lastip)


thread_pool = ThreadPoolExecutor(max_workers=50)
thread_results = []

for octate in range(first_octate, last_octate):
    ip_address = "%s.%d" % (network_address, octate)
    thread_pool.submit(try_server, ip_address)

thread_pool.shutdown()
