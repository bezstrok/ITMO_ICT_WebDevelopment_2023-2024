import socket

from config import BUFF_SIZE, HOST, PORT

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
	s.sendto(b"Hello, server!", (HOST, PORT))
	data, addr = s.recvfrom(BUFF_SIZE)
	print(f"Received from {addr}: {data.decode()}")
