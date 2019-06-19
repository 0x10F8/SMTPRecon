#!/usr/bin/python3
import sys
import socket

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
    return int(ip.split('.')[4])


iprange = sys.argv[1]
(firstip, lastip) = get_ip_range(iprange)
network_address = get_network_address(firstip)
first_octate = get_last_octate(firstip)
last_octate = get_last_octate(lastip)

for octate in range(first_octate, last_octate):
    ip_address = "%s.%d" % (network_address, octate)

    try:
        with(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            connect = s.connect((ip_address, 25))
            banner = s.recv(1024)
            print(banner)
            s.send('VRFY bob\r\n')
            result = s.recv(1024)
            print(result)
    except:
        pass
