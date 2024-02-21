# Задание 4

## Листинг кода

`config.py`

```python
HOST = '127.0.0.1'
PORT = 8080
BUFF_SIZE = 1024
```

`server.py`

```python
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
```

`client.py`

```python
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
```

## Основные Моменты

- **Многопоточность**: Использование потоков (`threading.Thread`) позволяет серверу обрабатывать множество клиентских
  подключений одновременно, обеспечивая каждому пользователю непрерывный прием и отправку сообщений.

- **Управление Клиентами**: Сервер хранит информацию о подключенных клиентах в словаре `clients`, где ключом является
  объект соединения, а значением - имя пользователя. Это облегчает рассылку сообщений всем пользователям, кроме
  отправителя.

- **Блокировки**: Использование объекта `lock` (`threading.Lock()`) обеспечивает потокобезопасное изменение общих
  данных (`clients`), предотвращая возможные гонки данных при одновременном доступе из разных потоков.

- **Приветствие и Имена Пользователей**: При подключении к чату от пользователя требуется ввести имя, которое затем
  используется для идентификации в сообщениях и уведомлениях о подключении/отключении.

- **Беспрерывный Прием Сообщений**: На стороне клиента запускается отдельный поток для приема сообщений, позволяя
  пользователю одновременно отправлять свои сообщения, не прерывая процесс приема входящих.

- **Обработка Исключений**: Код обрабатывает исключения, такие как `ConnectionResetError` и `WindowsError`, для
  корректного завершения работы потока при неожиданных обрывах соединения.
