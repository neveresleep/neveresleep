from flask import Flask
from io import BytesIO
import sys
import os
from pathlib import Path

# Импортируем Flask-приложение
sys.path.insert(0, str(Path(__file__).resolve().parent))
from index import app

# Функция-адаптер для вызова Flask из Vercel
def handler(request):
    environ = {
        'wsgi.input': BytesIO(request.body),
        'wsgi.errors': sys.stderr,
        'wsgi.version': (1, 0),
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
        'SERVER_SOFTWARE': 'vercel',
        'REQUEST_METHOD': request.method,
        'PATH_INFO': request.path,
        'QUERY_STRING': request.query,
        'CONTENT_TYPE': request.headers.get('Content-Type', ''),
        'CONTENT_LENGTH': request.headers.get('Content-Length', ''),
        'REMOTE_ADDR': '127.0.0.1',
        'SERVER_NAME': 'vercel',
        'SERVER_PORT': '80',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.url_scheme': 'https',
    }

    # Добавляем заголовки запроса в окружение
    for key, value in request.headers.items():
        key = 'HTTP_' + key.upper().replace('-', '_')
        environ[key] = value

    # Выполнение запроса через WSGI
    response_data = {}
    def start_response(status, response_headers, exc_info=None):
        response_data['status'] = status
        response_data['headers'] = dict(response_headers)

    # Получаем результат выполнения Flask-приложения
    body = b''.join(app.wsgi_app(environ, start_response))
    
    # Возвращаем ответ в формате, который ожидает Vercel
    return {
        'statusCode': int(response_data['status'].split()[0]),
        'headers': response_data['headers'],
        'body': body.decode('utf-8')
    } 