#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import random
import _main

HOST = '172.20.70.39'
# PORT = 50007
PORT = 3333

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    # data = _main.check()
    # # data = "check"S
    # if data != 'null':
    data = 1
    data += 1
    result = str(data)
    print(result)
    client.sendto(result.encode('utf-8'),(HOST,PORT))