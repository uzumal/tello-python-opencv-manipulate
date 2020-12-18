import socket

tello_ip = '192.168.10.1'
tello_port = 8889

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = (tello_ip , tello_port)

socket.sendto('command'.encode('utf-8'),tello_address)
socket.sendto('ap KE115(2.4GHz) w3.doshisha.ac.jp'.encode('utf-8'),tello_address)
# socket.sendto('ap aterm-23cac4-g 69bf786967ec0'.encode('utf-8'),tello_address)
