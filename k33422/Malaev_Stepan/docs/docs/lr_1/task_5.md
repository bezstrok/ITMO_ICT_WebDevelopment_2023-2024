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
import threading
from http.client import responses
from urllib.parse import parse_qs, unquote_plus

from config import BUFF_SIZE, HOST, PORT


class GradesServer:
    def __init__(self, host, port, buff_size):
        self.host = host
        self.port = port
        self.buff_size = buff_size
        self.socket = None
        self.grades = {}
        self.lock = threading.Lock()
    
    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        
        print(f"Server started on http://{self.host}:{self.port}")
        
        while True:
            conn, addr = self.socket.accept()
            threading.Thread(target=self.handle_client, args=(conn,)).start()
    
    def handle_client(self, conn):
        request = self.read_request(conn)
        try:
            headers, body = request.split('\r\n\r\n', 1)
            request_line = headers.splitlines()[0]
            method, path, _ = request_line.split()
            
            match method:
                case 'GET':
                    response = self.handle_get(path)
                case 'POST':
                    response = self.handle_post(path, body)
                case _:
                    response = self.http_response(405, "Method Not Allowed")
        except Exception as e:
            response = self.http_response(400, f"Bad Request: {e}")
        
        conn.sendall(response)
        conn.close()
    
    def read_request(self, conn):
        request = ""
        while True:
            part = conn.recv(self.buff_size).decode()
            request += part
            if '\r\n\r\n' in part:
                break
        return request
    
    def handle_get(self, path):
        match path:
            case '/grades':
                content = self.grades_html()
                return self.http_response(200, content, content_type='text/html')
            case _:
                return self.http_response(404, "Not Found")
    
    def handle_post(self, path, body):
        match path:
            case '/submit-grade':
                data = self.parse_form_data(body)
                discipline = data.get('discipline')
                grade = data.get('grade')
                if discipline and grade:
                    with self.lock:
                        self.grades.setdefault(discipline, []).append(grade)
                    return self.handle_get('/grades')
                else:
                    return self.http_response(400, "Bad Request")
            case _:
                return self.http_response(404, "Not Found")
    
    @staticmethod
    def http_response(status_code, body, headers=None, content_type='text/plain'):
        response_line = f"HTTP/1.1 {status_code} {responses[status_code]}\r\n"
        headers = headers or {}
        headers['Content-Type'] = content_type
        headers['Content-Length'] = len(body.encode())
        header_lines = "\r\n".join(f"{key}: {value}" for key, value in headers.items())
        return (response_line + header_lines + "\r\n\r\n" + body).encode()
    
    @staticmethod
    def parse_form_data(body):
        params = parse_qs(body)
        return {k: unquote_plus(v[0]) if v else None for k, v in params.items()}
    
    def grades_html(self):
        content = ('<!DOCTYPE html>'
                   '<html lang="en">'
                   '<head>'
                   '<meta charset="UTF-8"><title>Grades</title>'
                   '</head>'
                   '<body>')
        
        with self.lock:
            for discipline, grades in self.grades.items():
                content += f"<h2>{discipline}</h2><ul>"
                for grade in grades:
                    content += f"<li>{grade}</li>"
                content += "</ul>"
        content += "</body></html>"
        return content


if __name__ == '__main__':
    server = GradesServer(HOST, PORT, BUFF_SIZE)
    server.start()
```

## Основные Моменты

- **Многопоточность**: Использование библиотеки `threading` позволяет серверу обрабатывать несколько запросов
  одновременно, обеспечивая высокую производительность и отзывчивость интерфейса.

- **Работа с HTTP-запросами**: Сервер способен распознавать методы HTTP-запросов (GET и POST), правильно реагируя на них
  в зависимости от указанного пути и содержимого запроса.

- **Безопасное Хранение Данных**: Использование блокировок (`threading.Lock`) при работе с общими данными (список
  оценок) предотвращает возможные гонки данных и обеспечивает целостность информации.

- **Формирование HTML-ответов**: Сервер динамически генерирует HTML-страницы для отображения списка оценок, используя
  данные, хранящиеся в памяти. Это демонстрирует, как можно реализовать простой веб-интерфейс без использования внешних
  фреймворков.

- **Парсинг Тела Запроса**: Обработка POST-запросов включает в себя парсинг тела запроса для извлечения данных формы,
  что позволяет добавлять оценки в систему через веб-форму.

- **Маршрутизация Запросов**: Сервер использует простую систему маршрутизации для определения обработчиков запросов на
  основе URL-пути, что облегчает добавление новых функций и улучшает организацию кода.
