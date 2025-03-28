import requests
import json

# Базовый URL для API Solana
SOLANA_API_URL = "https://api.mainnet-beta.solana.com"

# HTML содержимое страницы (сокращенная версия)
INDEX_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Проверка баланса Solana</title>
    <style>
        body { background: black; color: white; font-family: Arial; }
        .container { max-width: 800px; margin: 0 auto; padding: 2rem; }
        .logo { color: #ff00ff; font-size: 2.5rem; text-align: center; }
        input { padding: 10px; border-radius: 5px 0 0 5px; border: none; }
        button { background: #ff00ff; color: white; padding: 10px; border: none; 
                border-radius: 0 5px 5px 0; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">NEVER SLEEP AI MASTER</div>
        <div style="text-align: center; color: #ff00ff;">(аня зарабатывает)</div>
        <h1 style="text-align: center;">Проверка баланса кошелька Solana</h1>
        
        <div style="background: #1a1a1a; padding: 20px; border-radius: 10px;">
            <div style="display: flex; margin-bottom: 20px;">
                <input type="text" id="wallet-address" placeholder="Введите адрес кошелька Solana" style="flex: 1;">
                <button id="check-balance">Проверить баланс</button>
            </div>
            
            <div id="loading" style="display: none; text-align: center;">Получаем данные...</div>
            
            <div id="result" style="display: none;">
                <h2 style="color: #ff00ff;">Баланс кошелька</h2>
                <div style="background: #333; padding: 15px; border-radius: 8px;">
                    <p>Адрес: <span id="result-address"></span></p>
                    <p>Баланс: <span id="result-balance"></span> SOL</p>
                </div>
            </div>
            
            <div id="error" style="display: none; color: red;"></div>
        </div>
        
        <footer style="text-align: center; margin-top: 30px; opacity: 0.6;">
            © 2024 NEVER SLEEP AI MASTER | Проверка баланса Solana
        </footer>
    </div>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const walletInput = document.getElementById('wallet-address');
            const checkButton = document.getElementById('check-balance');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const error = document.getElementById('error');
            
            checkButton.addEventListener('click', checkBalance);
            
            function checkBalance() {
                const wallet = walletInput.value.trim();
                if (!wallet) {
                    showError('Введите адрес кошелька');
                    return;
                }
                
                loading.style.display = 'block';
                result.style.display = 'none';
                error.style.display = 'none';
                
                fetch('/api/solana', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ wallet })
                })
                .then(res => res.json())
                .then(data => {
                    loading.style.display = 'none';
                    if (data.error) {
                        showError(data.error);
                    } else {
                        document.getElementById('result-address').textContent = wallet;
                        document.getElementById('result-balance').textContent = data.balance_sol.toFixed(9);
                        result.style.display = 'block';
                    }
                })
                .catch(err => {
                    loading.style.display = 'none';
                    showError('Ошибка при запросе данных');
                });
            }
            
            function showError(message) {
                error.textContent = message;
                error.style.display = 'block';
            }
        });
    </script>
</body>
</html>"""

def handler(request):
    """Основной обработчик для Vercel Edge Function"""
    
    # Обработка GET запроса - показываем страницу
    if request.method == "GET":
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": INDEX_HTML
        }
    
    # Обработка POST запроса для получения баланса
    if request.method == "POST":
        try:
            # Получаем данные из тела запроса
            request_data = json.loads(request.body)
            wallet_address = request_data.get('wallet')
            
            if not wallet_address:
                return {
                    "statusCode": 400,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"error": "Адрес кошелька не указан"})
                }
            
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
                # Конвертируем ламports в SOL
                balance_lamports = data["result"]["value"]
                balance_sol = balance_lamports / 1_000_000_000
                
                return {
                    "statusCode": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({
                        "balance_lamports": balance_lamports,
                        "balance_sol": balance_sol
                    })
                }
            else:
                return {
                    "statusCode": 400,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"error": "Ошибка при получении баланса"})
                }
                
        except Exception as e:
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": str(e)})
            }
    
    # Если метод не GET и не POST
    return {
        "statusCode": 405,
        "headers": {"Content-Type": "text/plain"},
        "body": "Method Not Allowed"
    }
