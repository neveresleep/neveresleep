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