from flask import Flask, request, jsonify, render_template, send_from_directory
import requests
import os
import sys
from pathlib import Path

# Добавляем корневой каталог в путь
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Создаем Flask-приложение
app = Flask(__name__, 
           template_folder=str(Path(__file__).resolve().parent.parent / "templates"),
           static_folder=str(Path(__file__).resolve().parent.parent / "static"))

# Базовый URL для API Solana
SOLANA_API_URL = "https://api.mainnet-beta.solana.com"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/get_balance', methods=['POST'])
def get_balance():
    wallet_address = request.json.get('wallet')
    
    if not wallet_address:
        return jsonify({'error': 'Адрес кошелька не указан'}), 400
    
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
            
            return jsonify({
                'balance_lamports': balance_lamports,
                'balance_sol': balance_sol
            })
        else:
            return jsonify({'error': 'Ошибка при получении баланса'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Для Vercel Serverless Functions
def handler(request, context):
    with app.request_context(request):
        return app(request) 