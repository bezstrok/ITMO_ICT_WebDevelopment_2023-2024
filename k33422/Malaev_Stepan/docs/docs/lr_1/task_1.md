# Задание 1

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

from config import BUFF_SIZE, HOST, PORT

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    while True:
        data, addr = s.recvfrom(BUFF_SIZE)
        print(f"Received from {addr}: {data.decode()}")
        s.sendto(b"Hello, client!", addr)
```

`client.py`

```python
import socket

from config import BUFF_SIZE, HOST, PORT

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(b"Hello, server!", (HOST, PORT))
    data, addr = s.recvfrom(BUFF_SIZE)
    print(f"Received from {addr}: {data.decode()}")
```

## Основные Моменты

- **Использование UDP**: В отличие от TCP, UDP является протоколом без подтверждения доставки, что обеспечивает меньшую
  задержку и меньшие требования к пропускной способности, но без гарантии доставки или порядка сообщений.

- **Конфигурация через Модуль**: Параметры подключения (адрес хоста, порт и размер буфера) вынесены в отдельный
  модуль `config`, что улучшает читаемость кода и упрощает его изменение.

- **Примеры Клиента и Сервера**:
    - Клиент отправляет сообщение "Hello, server!" на сервер и ожидает ответа.
    - Сервер принимает сообщение от клиента, выводит его содержимое и отвечает сообщением "Hello, client!".

- **Менеджер Контекста для Сокетов**: Использование конструкции `with` для автоматического закрытия сокета после выхода
  из блока кода упрощает управление ресурсами и предотвращает утечки.

- **Отладочные Сообщения**: Вывод сообщений о полученных данных и адресе отправителя помогает в отладке и мониторинге
  взаимодействия между клиентом и сервером.