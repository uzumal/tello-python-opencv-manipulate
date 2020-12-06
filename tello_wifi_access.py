import socket

tello_ip = '192.168.10.1'
tello_port = 8889

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = (tello_ip , tello_port)

socket.sendto('command'.encode('utf-8'),tello_address)
socket.sendto('ap KE101-2(2.4) w3.doshisha.ac.jp'.encode('utf-8'),tello_address)

