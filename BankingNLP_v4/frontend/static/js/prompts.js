/**
 * JavaScript для управления промтами
 */

// Глобальные переменные
let promptsData = {};
let promptTypes = [];

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    loadPromptTypes();
    loadPrompts();
    setupEventListeners();
});

/**
 * Загрузить типы промтов
 */
async function loadPromptTypes() {
    try {
        const response = await fetch('/api/v1/prompts/types');
        if (response.ok) {
            promptTypes = await response.json();
            populateTypeFilters();
        } else {
            console.error('Ошибка загрузки типов промтов:', response.statusText);
        }
    } catch (error) {
        console.error('Ошибка загрузки типов промтов:', error);
    }
}

/**
 * Заполнить фильтры типами промтов
 */
function populateTypeFilters() {
    const typeFilter = document.getElementById('typeFilter');
    const createTypeSelect = document.getElementById('promptType');
    const editTypeSelect = document.getElementById('editPromptType');
    
    // Очищаем существующие опции
    typeFilter.innerHTML = '<option value="">Все типы</option>';
    createTypeSelect.innerHTML = '<option value="">Выберите тип</option>';
    editTypeSelect.innerHTML = '<option value="">Выберите тип</option>';
    
    // Добавляем типы промтов
    promptTypes.forEach(type => {
        const option = document.createElement('option');
        option.value = type;
        option.textContent = getTypeDisplayName(type);
        
        typeFilter.appendChild(option.cloneNode(true));
        createTypeSelect.appendChild(option.cloneNode(true));
        editTypeSelect.appendChild(option.cloneNode(true));
    });
}

/**
 * Получить отображаемое имя типа промта
 */
function getTypeDisplayName(type) {
    const typeNames = {
        'topic_extraction': 'Извлечение тематик',
        'product_analysis': 'Анализ продуктов',
        'sentiment_analysis': 'Анализ настроений',
        'intent_classification': 'Классификация намерений',
        'summarization': 'Суммаризация',
        'benchmark': 'Бенчмарк',
        'custom': 'Пользовательский'
    };
    return typeNames[type] || type;
}

/**
 * Загрузить список промтов
 */
async function loadPrompts() {
    try {
        const response = await fetch('/api/v1/prompts/');
        if (response.ok) {
            promptsData = await response.json();
            renderPrompts();
        } else {
            console.error('Ошибка загрузки промтов:', response.statusText);
            showAlert('Ошибка загрузки промтов', 'danger');
        }
    } catch (error) {
        console.error('Ошибка загрузки промтов:', error);
        showAlert('Ошибка загрузки промтов', 'danger');
    }
}

/**
 * Отобразить промты на странице
 */
function renderPrompts() {
    const container = document.getElementById('promptsList');
    container.innerHTML = '';
    
    const filteredPrompts = filterPrompts();
    
    if (filteredPrompts.length === 0) {
        container.innerHTML = `
            <div class="col-12">
                <div class="alert alert-info text-center">
                    <i class="fas fa-info-circle me-2"></i>
                    Промты не найдены
                </div>
            </div>
        `;
        return;
    }
    
    filteredPrompts.forEach(([promptId, prompt]) => {
        const card = createPromptCard(promptId, prompt);
        container.appendChild(card);
    });
}

/**
 * Фильтровать промты по заданным критериям
 */
function filterPrompts() {
    const typeFilter = document.getElementById('typeFilter').value;
    const statusFilter = document.getElementById('statusFilter').value;
    const searchFilter = document.getElementById('searchFilter').value.toLowerCase();
    
    return Object.entries(promptsData).filter(([promptId, prompt]) => {
        // Фильтр по типу
        if (typeFilter && prompt.type !== typeFilter) {
            return false;
        }
        
        // Фильтр по статусу
        if (statusFilter) {
            const isActive = prompt.is_active;
            if (statusFilter === 'active' && !isActive) return false;
            if (statusFilter === 'inactive' && isActive) return false;
        }
        
        // Фильтр по поиску
        if (searchFilter) {
            const searchText = `${prompt.name} ${prompt.description}`.toLowerCase();
            if (!searchText.includes(searchFilter)) {
                return false;
            }
        }
        
        return true;
    });
}

/**
 * Создать карточку промта
 */
function createPromptCard(promptId, prompt) {
    const col = document.createElement('div');
    col.className = 'col-md-6 col-lg-4 mb-4';
    
    const statusBadge = prompt.is_active 
        ? '<span class="badge bg-success">Активный</span>'
        : '<span class="badge bg-secondary">Неактивный</span>';
    
    const typeBadge = `<span class="badge bg-primary prompt-type-badge">${getTypeDisplayName(prompt.type)}</span>`;
    
    const parametersHtml = prompt.parameters.length > 0 
        ? prompt.parameters.map(param => `<span class="badge parameter-badge">${param}</span>`).join('')
        : '<span class="text-muted">Нет параметров</span>';
    
    col.innerHTML = `
        <div class="card prompt-card h-100">
            <div class="card-header d-flex justify-content-between align-items-start">
                <div>
                    <h6 class="card-title mb-1">${prompt.name}</h6>
                    <small class="text-muted">v${prompt.version}</small>
                </div>
                <div>
                    ${statusBadge}
                    ${typeBadge}
                </div>
            </div>
            <div class="card-body">
                <p class="card-text">${prompt.description || 'Описание отсутствует'}</p>
                
                <div class="mb-3">
                    <strong>Параметры:</strong><br>
                    ${parametersHtml}
                </div>
                
                <div class="mb-3">
                    <strong>Шаблон:</strong>
                    <div class="prompt-template">
                        ${escapeHtml(prompt.template.substring(0, 200))}${prompt.template.length > 200 ? '...' : ''}
                    </div>
                </div>
            </div>
            <div class="card-footer">
                <div class="btn-group w-100" role="group">
                    <button class="btn btn-outline-primary btn-sm" onclick="editPrompt('${promptId}')">
                        <i class="fas fa-edit me-1"></i>Редактировать
                    </button>
                    <button class="btn btn-outline-info btn-sm" onclick="formatPrompt('${promptId}')">
                        <i class="fas fa-code me-1"></i>Форматировать
                    </button>
                    <button class="btn btn-outline-${prompt.is_active ? 'warning' : 'success'} btn-sm" 
                            onclick="togglePromptStatus('${promptId}', ${prompt.is_active})">
                        <i class="fas fa-${prompt.is_active ? 'pause' : 'play'} me-1"></i>
                        ${prompt.is_active ? 'Деактивировать' : 'Активировать'}
                    </button>
                    ${prompt.type === 'custom' ? `
                        <button class="btn btn-outline-danger btn-sm" onclick="deletePrompt('${promptId}')">
                            <i class="fas fa-trash me-1"></i>Удалить
                        </button>
                    ` : ''}
                </div>
            </div>
        </div>
    `;
    
    return col;
}

/**
 * Создать новый промт
 */
async function createPrompt() {
    const formData = {
        name: document.getElementById('promptName').value,
        description: document.getElementById('promptDescription').value,
        prompt_type: document.getElementById('promptType').value,
        template: document.getElementById('promptTemplate').value,
        parameters: document.getElementById('promptParameters').value.split(',').map(p => p.trim()).filter(p => p),
        version: document.getElementById('promptVersion').value,
        metadata: {}
    };
    
    if (!formData.name || !formData.prompt_type || !formData.template) {
        showAlert('Заполните все обязательные поля', 'warning');
        return;
    }
    
    try {
        const response = await fetch('/api/v1/prompts/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            const newPrompt = await response.json();
            showAlert('Промт успешно создан', 'success');
            bootstrap.Modal.getInstance(document.getElementById('createPromptModal')).hide();
            resetCreateForm();
            loadPrompts();
        } else {
            const error = await response.json();
            showAlert(`Ошибка создания промта: ${error.detail}`, 'danger');
        }
    } catch (error) {
        console.error('Ошибка создания промта:', error);
        showAlert('Ошибка создания промта', 'danger');
    }
}

/**
 * Редактировать промт
 */
async function editPrompt(promptId) {
    try {
        const response = await fetch(`/api/v1/prompts/${promptId}`);
        if (response.ok) {
            const prompt = await response.json();
            populateEditForm(prompt);
            bootstrap.Modal.getInstance(document.getElementById('editPromptModal')).show();
        } else {
            showAlert('Ошибка загрузки промта', 'danger');
        }
    } catch (error) {
        console.error('Ошибка загрузки промта:', error);
        showAlert('Ошибка загрузки промта', 'danger');
    }
}

/**
 * Заполнить форму редактирования
 */
function populateEditForm(prompt) {
    document.getElementById('editPromptId').value = prompt.id;
    document.getElementById('editPromptName').value = prompt.name;
    document.getElementById('editPromptDescription').value = prompt.description;
    document.getElementById('editPromptType').value = prompt.prompt_type;
    document.getElementById('editPromptTemplate').value = prompt.template;
    document.getElementById('editPromptParameters').value = prompt.parameters.join(', ');
    document.getElementById('editPromptVersion').value = prompt.version;
    document.getElementById('editPromptActive').checked = prompt.is_active;
}

/**
 * Обновить промт
 */
async function updatePrompt() {
    const promptId = document.getElementById('editPromptId').value;
    const formData = {
        name: document.getElementById('editPromptName').value,
        description: document.getElementById('editPromptDescription').value,
        template: document.getElementById('editPromptTemplate').value,
        parameters: document.getElementById('editPromptParameters').value.split(',').map(p => p.trim()).filter(p => p),
        version: document.getElementById('editPromptVersion').value,
        is_active: document.getElementById('editPromptActive').checked
    };
    
    try {
        const response = await fetch(`/api/v1/prompts/${promptId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            showAlert('Промт успешно обновлен', 'success');
            bootstrap.Modal.getInstance(document.getElementById('editPromptModal')).hide();
            loadPrompts();
        } else {
            const error = await response.json();
            showAlert(`Ошибка обновления промта: ${error.detail}`, 'danger');
        }
    } catch (error) {
        console.error('Ошибка обновления промта:', error);
        showAlert('Ошибка обновления промта', 'danger');
    }
}

/**
 * Переключить статус промта
 */
async function togglePromptStatus(promptId, currentStatus) {
    const action = currentStatus ? 'deactivate' : 'activate';
    const actionText = currentStatus ? 'деактивирован' : 'активирован';
    
    try {
        const response = await fetch(`/api/v1/prompts/${promptId}/${action}`, {
            method: 'POST'
        });
        
        if (response.ok) {
            showAlert(`Промт успешно ${actionText}`, 'success');
            loadPrompts();
        } else {
            const error = await response.json();
            showAlert(`Ошибка ${action} промта: ${error.detail}`, 'danger');
        }
    } catch (error) {
        console.error(`Ошибка ${action} промта:`, error);
        showAlert(`Ошибка ${action} промта`, 'danger');
    }
}

/**
 * Удалить промт
 */
async function deletePrompt(promptId) {
    if (!confirm('Вы уверены, что хотите удалить этот промт?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/v1/prompts/${promptId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showAlert('Промт успешно удален', 'success');
            loadPrompts();
        } else {
            const error = await response.json();
            showAlert(`Ошибка удаления промта: ${error.detail}`, 'danger');
        }
    } catch (error) {
        console.error('Ошибка удаления промта:', error);
        showAlert('Ошибка удаления промта', 'danger');
    }
}

/**
 * Форматировать промт
 */
async function formatPrompt(promptId) {
    const prompt = promptsData[promptId];
    if (!prompt) return;
    
    // Простой пример параметров для демонстрации
    const parameters = {};
    prompt.parameters.forEach(param => {
        parameters[param] = `[${param}]`;
    });
    
    try {
        const response = await fetch(`/api/v1/prompts/${promptId}/format`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(parameters)
        });
        
        if (response.ok) {
            const result = await response.json();
            showFormattedPrompt(prompt.name, result.formatted_prompt);
        } else {
            const error = await response.json();
            showAlert(`Ошибка форматирования: ${error.detail}`, 'danger');
        }
    } catch (error) {
        console.error('Ошибка форматирования промта:', error);
        showAlert('Ошибка форматирования промта', 'danger');
    }
}

/**
 * Показать отформатированный промт
 */
function showFormattedPrompt(promptName, formattedPrompt) {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Отформатированный промт: ${promptName}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <pre class="bg-light p-3 rounded" style="max-height: 400px; overflow-y: auto;">${escapeHtml(formattedPrompt)}</pre>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-primary" onclick="copyToClipboard('${escapeHtml(formattedPrompt)}')">
                        <i class="fas fa-copy me-1"></i>Копировать
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    const bootstrapModal = new bootstrap.Modal(modal);
    bootstrapModal.show();
    
    modal.addEventListener('hidden.bs.modal', () => {
        document.body.removeChild(modal);
    });
}

/**
 * Копировать в буфер обмена
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showAlert('Текст скопирован в буфер обмена', 'success');
    }).catch(() => {
        showAlert('Ошибка копирования', 'danger');
    });
}

/**
 * Настройка обработчиков событий
 */
function setupEventListeners() {
    // Фильтры
    document.getElementById('typeFilter').addEventListener('change', renderPrompts);
    document.getElementById('statusFilter').addEventListener('change', renderPrompts);
    document.getElementById('searchFilter').addEventListener('input', renderPrompts);
    
    // Сброс формы создания
    document.getElementById('createPromptModal').addEventListener('hidden.bs.modal', resetCreateForm);
}

/**
 * Сбросить форму создания
 */
function resetCreateForm() {
    document.getElementById('createPromptForm').reset();
    document.getElementById('promptVersion').value = '1.0';
    document.getElementById('promptActive').checked = true;
}

/**
 * Показать уведомление
 */
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

/**
 * Экранировать HTML
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
} 