import socket

from config import BUFF_SIZE, HOST, PORT
from tools import solve_quadratic_equation

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen()
	while True:
		conn, addr = s.accept()
		with conn:
			print(f'Connected by {addr}')
			conn.sendall(b'Enter a, b, c: ')
			data = conn.recv(BUFF_SIZE)
			data = data.decode()
			try:
				a, b, c = map(float, data.split(', '))
				res = solve_quadratic_equation(a, b, c)
				match res:
					case None:
						output = 'No roots'
					case float():
						output = f'x = {res}'
					case tuple():
						output = f'x1 = {res[0]:.3f}, x2 = {res[1]:.3f}'
			except ValueError:
				output = 'Invalid input'
			conn.sendall(output.encode())
