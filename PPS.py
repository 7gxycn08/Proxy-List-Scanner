import socket
import threading
from colorama import Fore
from colorama import init, AnsiToWin32
import time
import sys

init(wrap=False)
stream = AnsiToWin32(sys.stderr).stream
with open('ProxyList.txt','r',encoding='utf8') as f:
    iplist = f.readlines()

number_of_ips = len(iplist)
response_check = bytes('200 OK', encoding='utf-8')
request = 'GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n'

class SocketPool:
    def __init__(self, max_size=1000):
        self.max_size = max_size
        self.pool = []

    def get_connection(self):
        if self.pool:
            return self.pool.pop()
        else:
            return socket.socket()

    def return_connection(self, connection):
        if len(self.pool) < self.max_size:
            self.pool.append(connection)

    def close_all(self):
        for connection in self.pool:
            connection.close()
        self.pool = []

pool = SocketPool()
