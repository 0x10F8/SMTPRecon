#!/usr/bin/python3
import sys
import socket
from concurrent.futures import ThreadPoolExecutor

if len(sys.argv) != 3:
    print(
        "usage: smtpverify.py [IP] [USER LIST]")
    exit(1)


ip = sys.argv[1]
users_list = sys.argv[2]

try:
    with(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.settimeout(3)
        s.connect((ip, 25))
        s.recv(1024) # Recieve the banner
        with (open(users_list, 'r')) as users:
            for username in users.readlines():
                s.send(b'VRFY ' + username.encode('ascii'))
                response = s.recv(1024)
                print(response.decode('ascii'))
except Exception as e:
    print('Error connecting to %s : %s' % (ip, e))
