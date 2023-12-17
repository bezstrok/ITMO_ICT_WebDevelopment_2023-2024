import socket

from config import BUFF_SIZE, HOST, PORT

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	
	data = s.recv(BUFF_SIZE)
	print(data.decode())
	
	data = input()
	s.sendall(data.encode())
	
	data = s.recv(BUFF_SIZE)
	print(data.decode())
