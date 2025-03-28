import requests
import os
import json
from pathlib import Path
import traceback
from templates import INDEX_HTML

# Добавим отладочные сообщения
print("DEBUG: Модуль index.py загружен")

# Базовый URL для API Solana
SOLANA_API_URL = "https://api.mainnet-beta.solana.com"

# Простой класс для ответа
class SimpleResponse:
    def __init__(self, body, status=200, content_type="text/plain"):
        self.body = body
        self.status = status
        self.content_type = content_type
        
    def to_vercel_response(self):
        return {
            "statusCode": self.status,
            "headers": {
                "Content-Type": self.content_type
            },
            "body": self.body
        }

# Обработчик для запроса баланса
def handle_balance_request(request_data):
    wallet_address = request_data.get('wallet')
    
    if not wallet_address:
        return SimpleResponse(json.dumps({"error": "Адрес кошелька не указан"}), 400, "application/json")
    
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
            
            result = {
                "balance_lamports": balance_lamports,
                "balance_sol": balance_sol
            }
            
            return SimpleResponse(json.dumps(result), 200, "application/json")
        else:
            return SimpleResponse(json.dumps({"error": "Ошибка при получении баланса"}), 400, "application/json")
            
    except Exception as e:
        print(f"DEBUG: Error in balance request: {str(e)}")
        traceback.print_exc()
        return SimpleResponse(json.dumps({"error": str(e)}), 500, "application/json")

# Главная функция-обработчик для Vercel
def handler(request):
    try:
        print(f"DEBUG: Handling request to path: {request.path}, method: {request.method}")
        path = request.path
        
        # Обработка главной страницы
        if path == "/" or path == "":
            return SimpleResponse(INDEX_HTML, 200, "text/html").to_vercel_response()
        
        # Обработка API для получения баланса
        if path == "/get_balance" and request.method == "POST":
            try:
                body = request.body.decode("utf-8") if request.body else "{}"
                print(f"DEBUG: Request body: {body}")
                request_data = json.loads(body)
                response = handle_balance_request(request_data)
                return response.to_vercel_response()
            except Exception as e:
                print(f"DEBUG: Error in balance API: {str(e)}")
                traceback.print_exc()
                error_response = {"error": str(e)}
                return SimpleResponse(json.dumps(error_response), 500, "application/json").to_vercel_response()
        
        # Если ни один из обработчиков не сработал
        return SimpleResponse("Not found", 404, "text/plain").to_vercel_response()
        
    except Exception as e:
        print(f"DEBUG: Unhandled exception in handler: {str(e)}")
        traceback.print_exc()
        error_info = {
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(error_info)
        } 