import socket
import threading

from config import BUFF_SIZE, HOST, PORT

clients = {}
lock = threading.Lock()


def handle_client(conn, addr):
	name = None
	try:
		conn.sendall(b'Enter your name: ')
		name = conn.recv(BUFF_SIZE).decode()
		
		with lock:
			clients[conn] = name
		
		print(f'New connection: {name} {addr}')
		broadcast_message(f'{name} joined the chat', conn)
		
		while True:
			data = conn.recv(BUFF_SIZE)
			
			if not data:
				print(f"{name} has disconnected.")
				break
			
			print(f"Message from {name}: {data.decode()}")
			broadcast_message(f'{name}: {data.decode()}', conn)
	except ConnectionResetError:
		print(f"Connection reset by {name}.")
	finally:
		if name:
			with lock:
				if conn in clients:
					del clients[conn]
			conn.close()
			broadcast_message(f'{name} has left the chat', conn)


def broadcast_message(message, sender_conn):
	with lock:
		for client in clients:
			if client != sender_conn:
				client.sendall(message.encode())


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen()
	while True:
		conn, addr = s.accept()
		threading.Thread(target=handle_client, args=(conn, addr)).start()
