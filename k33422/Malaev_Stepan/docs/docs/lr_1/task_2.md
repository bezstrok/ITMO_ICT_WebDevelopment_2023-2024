# Задание 2

## Листинг кода

`config.py`

```python
HOST = '127.0.0.1'
PORT = 8080
BUFF_SIZE = 1024
```

`tools.py`

```python
def solve_quadratic_equation(a, b, c) -> float or tuple:
    d = b ** 2 - 4 * a * c
    if d < 0:
        return None
    elif d == 0:
        return -b / (2 * a)
    else:
        return (-b - d ** 0.5) / (2 * a), (-b + d ** 0.5) / (2 * a)
```

`server.py`

```python
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
```

`client.py`

```python
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
```

## Основные Моменты

- **TCP Соединение**: В отличие от предыдущего примера с UDP, здесь используется TCP протокол, который гарантирует
  доставку данных и сохранение порядка сообщений.

- **Обработка Квадратного Уравнения**: Функция `solve_quadratic_equation` рассчитывает дискриминант и корни уравнения,
  предоставляя разные ответы в зависимости от значения дискриминанта.

- **Простой Интерфейс**: Сервер запрашивает у клиента коэффициенты уравнения в формате `a, b, c`, что делает
  взаимодействие понятным и простым.

- **Использование Матчинга По Шаблону**: В Python 3.10 и выше доступен оператор `match` для удобной обработки различных
  случаев возвращаемых значений функции. Это упрощает код и делает его более читаемым.

- **Декодирование и Кодирование Сообщений**: Передача данных между клиентом и сервером осуществляется в байтовом
  формате, что требует их декодирования и кодирования для работы с текстовым представлением.

- **Обработка Исключений**: Сервер обрабатывает исключение `ValueError` для случаев, когда ввод не соответствует
  ожидаемому формату, что предотвращает его аварийное завершение.