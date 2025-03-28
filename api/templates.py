"""
Модуль содержит встроенные шаблоны HTML и CSS/JS контент
для случаев, когда Vercel не может получить доступ к файлам
в каталогах вне /api
"""

# HTML шаблон главной страницы
INDEX_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Проверка баланса Solana</title>
    <style id="main-styles">
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: #000000;
            color: #ffffff;
            line-height: 1.6;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            overflow: hidden;
        }

        .animated-background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            overflow: hidden;
        }

        .bg-element {
            position: absolute;
            opacity: 0;
            pointer-events: none;
            animation-name: float;
            animation-timing-function: ease-in-out;
            animation-iteration-count: infinite;
        }

        .heart {
            color: rgba(255, 0, 255, 0.3);
            font-size: 30px;
            text-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
        }

        .solana-token {
            color: rgba(153, 69, 255, 0.3);
            font-size: 35px;
            text-shadow: 0 0 10px rgba(153, 69, 255, 0.5);
        }

        @keyframes float {
            0% {
                transform: translateY(100vh) translateX(0) rotate(0deg);
                opacity: 0;
            }
            10% {
                opacity: 0.7;
            }
            90% {
                opacity: 0.7;
            }
            100% {
                transform: translateY(-50px) translateX(var(--translateX, 100px)) rotate(var(--rotate, 360deg));
                opacity: 0;
            }
        }

        .container {
            width: 100%;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            position: relative;
            z-index: 1;
        }

        header {
            text-align: center;
            margin-bottom: 3rem;
        }

        .logo {
            font-size: 2.8rem;
            color: #ff00ff;
            text-shadow: 0 0 15px rgba(255, 0, 255, 0.7);
            font-weight: bold;
            margin-bottom: 0.5rem;
        }

        .logo-subtitle {
            font-size: 1.2rem;
            color: #ff00ff;
            opacity: 0.8;
            font-style: italic;
        }

        header h1 {
            font-size: 2.5rem;
            color: #9945FF;
            text-shadow: 0 2px 10px rgba(153, 69, 255, 0.2);
            margin-top: 1.5rem;
        }

        .wallet-form {
            background-color: rgba(20, 20, 20, 0.9);
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(255, 0, 255, 0.2);
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 0, 255, 0.3);
        }

        .input-group {
            display: flex;
            margin-bottom: 2rem;
        }

        input {
            flex: 1;
            padding: 1rem;
            border-radius: 8px 0 0 8px;
            border: none;
            background-color: #1a1a1a;
            color: #ffffff;
            font-size: 1rem;
            outline: none;
            border: 1px solid rgba(255, 0, 255, 0.5);
        }

        button {
            padding: 1rem 1.5rem;
            background-color: #ff00ff;
            color: white;
            border: none;
            border-radius: 0 8px 8px 0;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }

        @keyframes pulse {
            0% {
                transform: scale(1);
                box-shadow: 0 0 0 0 rgba(255, 0, 255, 0.7);
            }
            70% {
                transform: scale(1.05);
                box-shadow: 0 0 0 10px rgba(255, 0, 255, 0);
            }
            100% {
                transform: scale(1);
                box-shadow: 0 0 0 0 rgba(255, 0, 255, 0);
            }
        }

        @keyframes flash {
            0%, 100% {
                background-color: #ff00ff;
            }
            50% {
                background-color: #ffffff;
                color: #000000;
            }
        }

        button.clicked {
            animation: flash 0.3s ease;
        }

        button:hover {
            background-color: #d400d4;
            animation: pulse 1.5s infinite;
        }

        .loading, .result, .error {
            display: none;
            margin-top: 2rem;
            text-align: center;
        }

        .loading.active, .result.active, .error.active {
            display: block;
            animation: fadeIn 0.5s ease;
        }

        .spinner {
            margin: 0 auto;
            width: 50px;
            height: 50px;
            border: 5px solid rgba(255, 0, 255, 0.3);
            border-top: 5px solid #ff00ff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        .result h2 {
            color: #ff00ff;
            margin-bottom: 1rem;
        }

        .balance-info {
            background-color: #1a1a1a;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid rgba(255, 0, 255, 0.5);
        }

        .balance-info p {
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
        }

        #result-balance {
            color: #ff00ff;
            font-weight: bold;
            font-size: 1.3rem;
        }

        .error {
            color: #ff4a4a;
            background-color: rgba(255, 74, 74, 0.1);
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid rgba(255, 74, 74, 0.5);
        }

        footer {
            text-align: center;
            margin-top: 3rem;
            color: rgba(255, 255, 255, 0.6);
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        @media (max-width: 600px) {
            .container {
                padding: 1rem;
            }
            
            .logo {
                font-size: 2rem;
            }
            
            .logo-subtitle {
                font-size: 1rem;
            }
            
            header h1 {
                font-size: 1.8rem;
            }
            
            .input-group {
                flex-direction: column;
            }
            
            input {
                border-radius: 8px;
                margin-bottom: 1rem;
            }
            
            button {
                border-radius: 8px;
            }
        }
    </style>
</head>
<body>
    <div class="animated-background">
        <!-- Элементы будут добавлены через JavaScript -->
    </div>
    
    <div class="container">
        <header>
            <div class="logo">NEVER SLEEP AI MASTER</div>
            <div class="logo-subtitle">(аня зарабатывает)</div>
            <h1>Проверка баланса кошелька Solana</h1>
        </header>
        
        <main>
            <div class="wallet-form">
                <div class="input-group">
                    <input type="text" id="wallet-address" placeholder="Введите адрес кошелька Solana">
                    <button id="check-balance">Проверить баланс</button>
                </div>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Получаем данные...</p>
                </div>
                
                <div class="result" id="result">
                    <h2>Баланс кошелька</h2>
                    <div class="balance-info">
                        <p>Адрес: <span id="result-address"></span></p>
                        <p>Баланс: <span id="result-balance"></span> SOL</p>
                    </div>
                </div>
                
                <div class="error" id="error">
                    <p id="error-message"></p>
                </div>
            </div>
        </main>
        
        <footer>
            <p>© 2024 NEVER SLEEP AI MASTER | Проверка баланса Solana</p>
        </footer>
    </div>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Получаем элементы DOM
            const walletInput = document.getElementById('wallet-address');
            const checkButton = document.getElementById('check-balance');
            const loadingSection = document.getElementById('loading');
            const resultSection = document.getElementById('result');
            const errorSection = document.getElementById('error');
            const resultAddress = document.getElementById('result-address');
            const resultBalance = document.getElementById('result-balance');
            const errorMessage = document.getElementById('error-message');
            const animatedBackground = document.querySelector('.animated-background');
            
            // Создаем анимированный фон
            createAnimatedBackground();
            
            // Эффект нажатия кнопки
            checkButton.addEventListener('mousedown', function() {
                this.style.transform = 'scale(0.95)';
                this.style.filter = 'brightness(0.9)';
            });
            
            checkButton.addEventListener('mouseup', function() {
                this.style.transform = 'scale(1)';
                this.style.filter = 'brightness(1)';
            });
            
            checkButton.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
                this.style.filter = 'brightness(1)';
            });
            
            // Устанавливаем обработчик клика на кнопку
            checkButton.addEventListener('click', checkBalance);
            
            // Также проверяем баланс при нажатии Enter в поле ввода
            walletInput.addEventListener('keypress', function(event) {
                if (event.key === 'Enter') {
                    checkBalance();
                }
            });
            
            // Функция для создания анимированного фона
            function createAnimatedBackground() {
                // Количество элементов
                const numElements = 30;
                
                // Символы для анимации
                const heartSymbol = '❤';
                const solanaSymbol = '◎';
                
                // Создаем элементы
                for (let i = 0; i < numElements; i++) {
                    // Создаем элемент
                    const element = document.createElement('div');
                    
                    // Случайно выбираем тип элемента (сердечко или токен Solana)
                    const isHeart = Math.random() > 0.5;
                    
                    // Добавляем соответствующие классы и содержимое
                    element.classList.add('bg-element');
                    if (isHeart) {
                        element.classList.add('heart');
                        element.textContent = heartSymbol;
                    } else {
                        element.classList.add('solana-token');
                        element.textContent = solanaSymbol;
                        // Начальный поворот для токена Solana
                        element.style.transform = `rotate(${Math.random() * 360}deg)`;
                    }
                    
                    // Устанавливаем случайную начальную позицию по горизонтали
                    const startX = Math.random() * 100; // процент ширины экрана
                    element.style.left = `${startX}%`;
                    
                    // Устанавливаем CSS переменные для анимации
                    // Случайное горизонтальное смещение
                    const translateX = -100 + Math.random() * 200; // от -100 до 100 пикселей
                    element.style.setProperty('--translateX', `${translateX}px`);
                    
                    // Случайный поворот
                    const rotate = Math.random() > 0.5 ? 360 : -360; // либо по часовой, либо против
                    element.style.setProperty('--rotate', `${rotate}deg`);
                    
                    // Устанавливаем случайную длительность анимации
                    const duration = 10 + Math.random() * 20; // от 10 до 30 секунд
                    element.style.animationDuration = `${duration}s`;
                    
                    // Устанавливаем случайную задержку начала анимации
                    const delay = Math.random() * 15; // от 0 до 15 секунд
                    element.style.animationDelay = `${delay}s`;
                    
                    // Добавляем элемент на страницу
                    animatedBackground.appendChild(element);
                }
            }
            
            // Функция проверки баланса
            function checkBalance() {
                const walletAddress = walletInput.value.trim();
                
                // Проверяем, что адрес введен
                if (!walletAddress) {
                    showError('Пожалуйста, введите адрес кошелька Solana.');
                    return;
                }
                
                // Скрываем предыдущие результаты и показываем загрузку
                hideAllSections();
                loadingSection.classList.add('active');
                
                // Добавляем эффект успешного нажатия
                checkButton.classList.add('clicked');
                setTimeout(() => {
                    checkButton.classList.remove('clicked');
                }, 300);
                
                // Отправляем запрос на сервер
                fetch('/get_balance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ wallet: walletAddress })
                })
                .then(response => response.json())
                .then(data => {
                    // Скрываем загрузку
                    loadingSection.classList.remove('active');
                    
                    if (data.error) {
                        showError(data.error);
                        return;
                    }
                    
                    // Показываем результат
                    resultAddress.textContent = walletAddress;
                    resultBalance.textContent = data.balance_sol.toFixed(9);
                    resultSection.classList.add('active');
                })
                .catch(error => {
                    // Скрываем загрузку и показываем ошибку
                    loadingSection.classList.remove('active');
                    showError('Ошибка при получении баланса. Пожалуйста, попробуйте позже.');
                    console.error('Ошибка:', error);
                });
            }
            
            // Функция для скрытия всех разделов результатов
            function hideAllSections() {
                loadingSection.classList.remove('active');
                resultSection.classList.remove('active');
                errorSection.classList.remove('active');
            }
            
            // Функция для отображения ошибки
            function showError(message) {
                errorMessage.textContent = message;
                errorSection.classList.add('active');
            }
        });
    </script>
</body>
</html>""" 