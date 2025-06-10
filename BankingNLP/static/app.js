document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('analysis-form');
    const resultsSection = document.getElementById('results-section');
    const textArea = document.getElementById('conversation-text');
    const exampleButtons = document.querySelectorAll('.example-btn');
    
    // Примеры текстов
    const examples = {
        'кредит': 'Клиент: Здравствуйте, хочу оформить кредит на автомобиль. Какие у вас условия?\nОператор: Конечно! Расскажу о наших условиях автокредитования.',
        'проблема': 'Клиент: Не могу войти в мобильное приложение, постоянно выдает ошибку.\nОператор: Давайте разберемся с проблемой доступа к приложению.',
        'ипотека': 'Клиент: Интересует ипотека на вторичное жилье. Какие документы нужны?\nОператор: Отличный выбор! Расскажу о программах ипотечного кредитования.',
        'карта': 'Клиент: Моя карта заблокирована, как восстановить доступ к счету?\nОператор: Поможем разблокировать карту и восстановить доступ.',
        'вклад': 'Клиент: Хочу открыть вклад с максимальным процентом. Что посоветуете?\nОператор: Рассмотрим наши депозитные программы с выгодными условиями.'
    };

    // Обработчики кнопок примеров
    exampleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const exampleType = this.dataset.example;
            textArea.value = examples[exampleType];
            
            // Визуальная обратная связь
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });

    // Обработчик формы
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const text = textArea.value.trim();
        if (!text) {
            alert('Пожалуйста, введите текст для анализа');
            return;
        }

        const analyzeBtn = document.getElementById('analyze-btn');
        const originalText = analyzeBtn.textContent;
        
        // Показываем состояние загрузки
        analyzeBtn.textContent = 'Анализируем...';
        analyzeBtn.disabled = true;

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    language: 'ru'
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Отображаем результаты
            displayResults(data);
            
            // Показываем секцию результатов
            resultsSection.style.display = 'block';
            resultsSection.scrollIntoView({ behavior: 'smooth' });

        } catch (error) {
            console.error('Ошибка при анализе:', error);
            alert('Произошла ошибка при анализе текста. Попробуйте еще раз.');
        } finally {
            // Восстанавливаем кнопку
            analyzeBtn.textContent = originalText;
            analyzeBtn.disabled = false;
        }
    });

    function displayResults(data) {
        // Отображение тематик
        const themesContainer = document.getElementById('themes-container');
        themesContainer.innerHTML = '';
        if (data.themes && data.themes.length > 0) {
            data.themes.forEach(theme => {
                const tag = document.createElement('span');
                tag.className = 'tag';
                tag.textContent = theme;
                themesContainer.appendChild(tag);
            });
        } else {
            themesContainer.innerHTML = '<span class="tag">Не определено</span>';
        }

        // Отображение продуктов
        const productsContainer = document.getElementById('products-container');
        productsContainer.innerHTML = '';
        if (data.products && data.products.length > 0) {
            data.products.forEach(product => {
                const tag = document.createElement('span');
                tag.className = 'tag';
                tag.textContent = product;
                productsContainer.appendChild(tag);
            });
        } else {
            productsContainer.innerHTML = '<span class="tag">Не определено</span>';
        }

        // Отображение эмоций
        const emotionsContainer = document.getElementById('emotions-container');
        emotionsContainer.innerHTML = '';
        if (data.emotions) {
            Object.entries(data.emotions).forEach(([emotion, value]) => {
                const emotionItem = document.createElement('div');
                emotionItem.className = 'emotion-item';
                
                const percentage = Math.round(value * 100);
                emotionItem.innerHTML = `
                    <span>${emotion}</span>
                    <div class="emotion-bar">
                        <div class="emotion-fill" style="width: ${percentage}%"></div>
                    </div>
                    <span>${percentage}%</span>
                `;
                emotionsContainer.appendChild(emotionItem);
            });
        }

        // Отображение уверенности
        const confidenceBar = document.getElementById('confidence-bar');
        const confidenceValue = document.getElementById('confidence-value');
        
        if (data.confidence !== undefined) {
            const confidence = Math.round(data.confidence * 100);
            setTimeout(() => {
                confidenceBar.style.width = `${confidence}%`;
                confidenceValue.textContent = `${confidence}%`;
            }, 300);
        }
    }
});
