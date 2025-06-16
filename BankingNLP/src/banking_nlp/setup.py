#!/usr/bin/env python3
"""
Установочный скрипт для банковского NLP проекта
Автоматически создает виртуальную среду, устанавливает зависимости и запускает тесты
"""

import os
import sys
import subprocess
import venv
import shutil
from pathlib import Path
from setuptools import setup, find_packages, Command
from setuptools.command.install import install

# Определение путей проекта
PROJECT_ROOT = Path(__file__).parent
VENV_NAME = "banking_nlp_env"
VENV_PATH = PROJECT_ROOT / VENV_NAME
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"

class CustomInstallCommand(install):
    """Кастомная команда установки с созданием виртуальной среды"""
    
    def run(self):
        """Основная логика установки"""
        print("🏦 Начинаем установку банковского NLP проекта...")
        
        # Проверка Python версии
        self.check_python_version()
        
        # Создание виртуальной среды
        self.create_virtual_environment()
        
        # Активация виртуальной среды и установка зависимостей
        self.install_dependencies()
        
        # Запуск базовой установки setuptools
        install.run(self)
        
        # Запуск проверочных тестов
        self.run_verification_tests()
        
        print("✅ Установка банковского NLP проекта завершена успешно!")

    def check_python_version(self):
        """Проверка версии Python"""
        version = sys.version_info
        if version.major != 3 or version.minor < 8:
            raise RuntimeError("❌ Требуется Python 3.8 или выше")
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - совместимая версия")

    def create_virtual_environment(self):
        """Создание виртуальной среды"""
        if VENV_PATH.exists():
            print(f"🔄 Удаление существующей виртуальной среды: {VENV_PATH}")
            shutil.rmtree(VENV_PATH)
        
        print(f"🆕 Создание новой виртуальной среды: {VENV_PATH}")
        venv.create(VENV_PATH, with_pip=True, clear=True)
        print("✅ Виртуальная среда создана успешно")

    def install_dependencies(self):
        """Установка зависимостей в виртуальную среду"""
        # Определение пути к Python в виртуальной среде
        if os.name == 'nt':  # Windows
            python_executable = VENV_PATH / "Scripts" / "python.exe"
            pip_executable = VENV_PATH / "Scripts" / "pip.exe"
        else:  # Unix/Linux/macOS
            python_executable = VENV_PATH / "bin" / "python"
            pip_executable = VENV_PATH / "bin" / "pip"
        
        # Обновление pip
        print("🔄 Обновление pip...")
        subprocess.run([str(python_executable), "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True)
        
        # Установка зависимостей из requirements.txt
        if REQUIREMENTS_FILE.exists():
            print("📦 Установка зависимостей из requirements.txt...")
            subprocess.run([str(pip_executable), "install", "-r", str(REQUIREMENTS_FILE)], 
                          check=True)
        else:
            print("⚠️  Файл requirements.txt не найден, устанавливаем базовые зависимости...")
            self.install_basic_dependencies(str(pip_executable))
        
        print("✅ Зависимости установлены успешно")

    def install_basic_dependencies(self, pip_executable):
        """Установка базовых зависимостей если requirements.txt отсутствует"""
        basic_deps = [
            "pymorphy2>=0.9.1",
            "pymorphy2-dicts-ru>=2.4.417127.4579844",
            "transformers>=4.35.0",
            "torch>=2.0.0",
            "pandas>=2.0.0",
            "numpy>=1.24.0",
            "scikit-learn>=1.3.0",
            "pyyaml>=6.0.0",
            "nltk>=3.8.1"
        ]
        
        for dep in basic_deps:
            print(f"📦 Установка {dep}...")
            subprocess.run([pip_executable, "install", dep], check=True)

    def run_verification_tests(self):
        """Запуск проверочных тестов"""
        # Определение пути к Python в виртуальной среде
        if os.name == 'nt':  # Windows
            python_executable = VENV_PATH / "Scripts" / "python.exe"
        else:  # Unix/Linux/macOS
            python_executable = VENV_PATH / "bin" / "python"
        
        print("🧪 Запуск проверочных тестов...")
        
        # Тест 1: Проверка импорта основных модулей
        self.test_basic_imports(str(python_executable))
        
        # Тест 2: Проверка конфигурации
        self.test_configuration(str(python_executable))
        
        # Тест 3: Проверка предобработки текста
        self.test_text_processing(str(python_executable))
        
        print("✅ Все проверочные тесты пройдены успешно!")

    def test_basic_imports(self, python_executable):
        """Тест импорта основных модулей"""
        test_script = '''
import sys
print("🔍 Тестирование импорта основных модулей...")

try:
    import pymorphy2
    print("✅ pymorphy2 импортирован успешно")
except ImportError as e:
    print(f"❌ Ошибка импорта pymorphy2: {e}")
    sys.exit(1)

try:
    import transformers
    print("✅ transformers импортирован успешно")
except ImportError as e:
    print(f"❌ Ошибка импорта transformers: {e}")
    sys.exit(1)

try:
    import pandas
    print("✅ pandas импортирован успешно")
except ImportError as e:
    print(f"❌ Ошибка импорта pandas: {e}")
    sys.exit(1)

print("✅ Все основные модули импортированы успешно")
'''
        subprocess.run([python_executable, "-c", test_script], check=True)

    def test_configuration(self, python_executable):
        """Тест загрузки конфигурации"""
        test_script = f'''
import sys
import os
sys.path.insert(0, r"{PROJECT_ROOT}")

print("🔍 Тестирование системы конфигурации...")

try:
    from utils.config import config
    print("✅ Модуль конфигурации загружен")
    
    # Тест получения базовых параметров
    model_name = config.get('model.base_model', 'default')
    print(f"✅ Базовая модель: {{model_name}}")
    
    batch_size = config.get('model.batch_size', 32)
    print(f"✅ Размер батча: {{batch_size}}")
    
except Exception as e:
    print(f"❌ Ошибка загрузки конфигурации: {{e}}")
    sys.exit(1)

print("✅ Система конфигурации работает корректно")
'''
        subprocess.run([python_executable, "-c", test_script], check=True)

    def test_text_processing(self, python_executable):
        """Тест предобработки текста"""
        test_script = f'''
import sys
sys.path.insert(0, r"{PROJECT_ROOT}")

print("🔍 Тестирование предобработки текста...")

try:
    from core.data_processing.preprocessors import BankingTextPreprocessor
    
    # Создание экземпляра препроцессора
    preprocessor = BankingTextPreprocessor()
    print("✅ Препроцессор текста создан")
    
    # Тест обработки простого текста
    test_text = "Клиент хочет оформить кредитную карту с номером 1234-5678-9012-3456"
    processed_text = preprocessor.preprocess(test_text)
    
    if processed_text:
        print(f"✅ Текст обработан: {{processed_text[:50]}}...")
    else:
        print("❌ Ошибка обработки текста")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Ошибка предобработки текста: {{e}}")
    sys.exit(1)

print("✅ Предобработка текста работает корректно")
'''
        subprocess.run([python_executable, "-c", test_script], check=True)


class TestCommand(Command):
    """Команда для запуска тестов"""
    description = 'Запуск тестов проекта'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Запуск всех тестов проекта"""
        # Определение пути к Python в виртуальной среде
        if os.name == 'nt':  # Windows
            python_executable = VENV_PATH / "Scripts" / "python.exe"
        else:  # Unix/Linux/macOS
            python_executable = VENV_PATH / "bin" / "python"
        
        if not python_executable.exists():
            print("❌ Виртуальная среда не найдена. Сначала выполните: python setup.py install")
            return
        
        print("🧪 Запуск полного набора тестов...")
        
        # Запуск существующих тестов
        test_files = [
            "test_step1.py",
            "test_preprocessing.py"
        ]
        
        for test_file in test_files:
            test_path = PROJECT_ROOT / test_file
            if test_path.exists():
                print(f"🔍 Запуск {test_file}...")
                try:
                    subprocess.run([str(python_executable), str(test_path)], 
                                 check=True, cwd=str(PROJECT_ROOT))
                    print(f"✅ {test_file} выполнен успешно")
                except subprocess.CalledProcessError:
                    print(f"❌ Ошибка в {test_file}")
            else:
                print(f"⚠️  Файл {test_file} не найден")


class CleanCommand(Command):
    """Команда для очистки проекта"""
    description = 'Очистка проекта и удаление виртуальной среды'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Очистка проекта"""
        print("🧹 Очистка проекта...")
        
        # Удаление виртуальной среды
        if VENV_PATH.exists():
            print(f"🗑️  Удаление виртуальной среды: {VENV_PATH}")
            shutil.rmtree(VENV_PATH)
        
        # Удаление кеша Python
        cache_dirs = [
            PROJECT_ROOT / "__pycache__",
            PROJECT_ROOT / "core" / "__pycache__",
            PROJECT_ROOT / "utils" / "__pycache__",
            PROJECT_ROOT / "build",
            PROJECT_ROOT / "dist",
            PROJECT_ROOT / "*.egg-info"
        ]
        
        for cache_dir in cache_dirs:
            if cache_dir.exists():
                if cache_dir.is_dir():
                    shutil.rmtree(cache_dir)
                else:
                    cache_dir.unlink()
        
        print("✅ Очистка завершена")


# Основная конфигурация setuptools
setup(
    name="banking-nlp",
    version="1.0.0",
    description="Банковская система анализа NLP для транскрибированных разговоров",
    long_description=open("README.md", "r", encoding="utf-8").read() if Path("README.md").exists() else "",
    long_description_content_type="text/markdown",
    author="Banking NLP Team",
    author_email="banking-nlp@example.com",
    url="https://github.com/your-org/banking-nlp",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pymorphy2>=0.9.1",
        "pymorphy2-dicts-ru>=2.4.417127.4579844",
        "transformers>=4.35.0",
        "torch>=2.0.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0",
        "pyyaml>=6.0.0",
        "nltk>=3.8.1",
        "tqdm>=4.65.0"
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.0.0"
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    cmdclass={
        'install': CustomInstallCommand,
        'test': TestCommand,
        'clean': CleanCommand,
    },
    entry_points={
        'console_scripts': [
            'banking-nlp-analyze=pipelines.inference:main',
            'banking-nlp-train=pipelines.training:main',
        ],
    },
    include_package_data=True,
    package_data={
        'configs': ['*.yaml', '*.yml'],
        'data': ['*.txt', '*.csv'],
    },
)
