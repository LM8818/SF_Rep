from utils.config import config
from utils.logging import get_logger, log_data_operation

# Тест конфигурации
print("Путь к raw данным:", config.get('data.raw_data_path'))
print("Базовая модель:", config.get('model.base_model'))

# Тест логирования
logger = get_logger(__name__)
logger.info("Тест логирования успешен!")

# Тест аудит логирования
log_data_operation("TEST", "test_file.txt", 100)

print("Шаг 1 выполнен успешно!")
