from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

app = Flask(__name__)

# Базовый URL для API Solana
SOLANA_API_URL = "https://api.mainnet-beta.solana.com"

@app.route('/')
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

# Если запускается как основной скрипт, то запускаем сервер в режиме debug
if __name__ == '__main__':
    # В production режиме использовать port из переменной окружения
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 