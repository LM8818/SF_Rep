import os
import sys
import subprocess
import logging
import logging.config
import yaml

def setup_logging():
    """Настраивает логирование из файла logging.yaml или использует базовую настройку."""
    try:
        with open('logging.yaml') as f:
            config = yaml.safe_load(f)
        logging.config.dictConfig(config)
    except Exception:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger().warning("Не удалось загрузить logging.yaml, используется базовая настройка логирования.")

def create_venv_and_install():
    """Создаёт виртуальную среду и устанавливает зависимости из requirements.txt."""
    venv_dir = "venv"
    if not os.path.exists(venv_dir):
        print("Создаётся виртуальная среда...")
        subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
    python_bin = os.path.join(venv_dir, "Scripts" if os.name == "nt" else "bin", "python")
    pip_bin = os.path.join(venv_dir, "Scripts" if os.name == "nt" else "bin", "pip")
    print("Устанавливаются зависимости из requirements.txt...")
    subprocess.check_call([pip_bin, "install", "-r", "requirements.txt"])
    print(f"Используйте {python_bin} для запуска пайплайна в виртуальной среде.")

def main(step='all'):
    logger = logging.getLogger("run")
    try:
        if step == 'venv':
            create_venv_and_install()
            logger.info("Виртуальная среда создана и зависимости установлены.")
            return
        # Импортируем только после установки зависимостей
        from src.data.load_data import load_transcripts
        from src.features.build_features import build_features
        from src.models.train_model import train_model
        from src.models.predict_model import predict
        from src.evaluation.evaluate import evaluate

        if step in ('all', 'data'):
            logger.info("=== Загрузка и подготовка данных ===")
            df = load_transcripts()
        if step in ('all', 'features'):
            logger.info("=== Генерация признаков ===")
            import pandas as pd
            df = pd.read_csv('data/processed/cleaned_transcripts.csv')
            df = build_features(df)
            df.to_csv('data/processed/features.csv', index=False)
        if step in ('all', 'train'):
            logger.info("=== Обучение модели ===")
            train_model()
        if step in ('all', 'predict'):
            logger.info("=== Предсказание ===")
            predict()
        if step in ('all', 'eval'):
            logger.info("=== Оценка качества ===")
            evaluate()
        logger.info("Пайплайн успешно завершён.")
    except Exception as e:
        logger.exception(f"Ошибка в пайплайне: {e}")

if __name__ == "__main__":
    setup_logging()
    # Новый режим: python run.py venv — создать виртуальную среду и установить зависимости
    step = sys.argv[1] if len(sys.argv) > 1 else 'all'
    main(step)
