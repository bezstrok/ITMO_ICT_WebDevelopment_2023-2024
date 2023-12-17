import socket
import threading

from config import BUFF_SIZE, HOST, PORT


def receive_messages(sock):
	while True:
		try:
			message = sock.recv(BUFF_SIZE).decode()
			print(message)
		except WindowsError:
			break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	
	threading.Thread(target=receive_messages, args=(s,)).start()
	
	while True:
		try:
			message = input()
			s.sendall(message.encode('utf-8'))
		except KeyboardInterrupt:
			break
