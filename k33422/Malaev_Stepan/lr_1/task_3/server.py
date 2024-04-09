import socket

from config import HOST, PORT

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen(1)
	while True:
		conn, addr = s.accept()
		print('Connected by', addr)
		
		with open('index.html', 'rb') as f:
			data = f.read()
		
		conn.sendall(
			b'HTTP/1.1 200 OK\n'
			b'Content-Type: text/html\n'
			b'Connection: close\n\n'
			+ data
		)

# http://localhost:8080/
