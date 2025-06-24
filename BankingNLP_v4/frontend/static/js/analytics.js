async function runBenchmark() {
    const button = event.target;
    const originalText = button.innerHTML;
    
    try {
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Запуск бенчмарка...';
        
        const response = await fetch('/api/v1/benchmark/performance?records_count=10000', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Обновляем метрики на dashboard
        document.getElementById('processingSpeed').textContent = data.records_per_second.toFixed(1);
        document.getElementById('avgProcessingTime').textContent = data.avg_time_per_record_ms.toFixed(2);
        document.getElementById('memoryUsage').textContent = data.memory_usage_mb.toFixed(1);
        
        // Показываем уведомление об успехе
        showNotification(`Бенчмарк завершён! Обработано ${data.total_records} записей за ${data.total_time_seconds.toFixed(2)}с. Файл: ${data.results_file}`, 'success');
        
    } catch (error) {
        console.error('Ошибка при запуске бенчмарка:', error);
        showNotification('Ошибка при запуске бенчмарка: ' + error.message, 'error');
    } finally {
        button.disabled = false;
        button.innerHTML = originalText;
    }
}

function showNotification(message, type) {
    const alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    // Добавляем уведомление в начало страницы
    const container = document.querySelector('.container');
    container.insertAdjacentHTML('afterbegin', alertHtml);
    
    // Автоматически скрываем через 5 секунд
    setTimeout(() => {
        const alert = document.querySelector('.alert');
        if (alert) {
            alert.remove();
        }
    }, 5000);
}
