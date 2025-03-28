from flask import Flask, request, jsonify, Response
import requests
import os
import json
from pathlib import Path

# Базовый URL для API Solana
SOLANA_API_URL = "https://api.mainnet-beta.solana.com"

# Путь к корневой директории проекта
ROOT_DIR = Path(__file__).resolve().parent.parent

# HTML шаблон для главной страницы
def get_html_template():
    with open(ROOT_DIR / "templates" / "index.html", "r") as file:
        return file.read()

# Функция для получения статического файла
def get_static_file(path):
    try:
        with open(ROOT_DIR / "static" / path, "r") as file:
            content = file.read()
            
        # Определение типа контента
        if path.endswith(".css"):
            content_type = "text/css"
        elif path.endswith(".js"):
            content_type = "application/javascript"
        else:
            content_type = "text/plain"
            
        return Response(content, content_type=content_type)
    except:
        return Response("File not found", status=404)

# Обработчик для запроса баланса
def handle_balance_request(request_data):
    wallet_address = request_data.get('wallet')
    
    if not wallet_address:
        return {"error": "Адрес кошелька не указан"}, 400
    
    try:
        # Формируем запрос к Solana API
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBalance",
            "params": [wallet_address]
        }
        
        response = requests.post(SOLANA_API_URL, json=payload)
        data = response.json()
        
        if "result" in data:
            # Конвертируем ламports в SOL (1 SOL = 1,000,000,000 lamports)
            balance_lamports = data["result"]["value"]
            balance_sol = balance_lamports / 1_000_000_000
            
            return {
                "balance_lamports": balance_lamports,
                "balance_sol": balance_sol
            }, 200
        else:
            return {"error": "Ошибка при получении баланса"}, 400
            
    except Exception as e:
        return {"error": str(e)}, 500

# Главная функция-обработчик для Vercel
def handler(request):
    path = request.path
    
    # Обработка статических файлов
    if path.startswith("/static/"):
        # Получаем путь к файлу (удаляем "/static/" из пути)
        file_path = path[8:]
        return get_static_file(file_path)
    
    # Обработка главной страницы
    if path == "/" or path == "":
        html_content = get_html_template()
        return Response(html_content, content_type="text/html")
    
    # Обработка API для получения баланса
    if path == "/get_balance" and request.method == "POST":
        try:
            request_data = json.loads(request.body)
            result, status_code = handle_balance_request(request_data)
            return Response(json.dumps(result), status=status_code, content_type="application/json")
        except Exception as e:
            return Response(json.dumps({"error": str(e)}), status=500, content_type="application/json")
    
    # Если ни один из обработчиков не сработал
    return Response("Not found", status=404) 