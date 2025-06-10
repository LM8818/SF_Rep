# -*- coding: utf-8 -*-
"""
Генератор CSV данных для Banking NLP System
Создает реалистичные банковские разговерации данных

Для создания CSV файлов с тестовыми данными в вашей Banking NLP System необходимо создать специальный модуль генератора, который будет создавать реалистичные банковские разговоры и сохранять их в структурированном формате.

## Создание генератора данных

### Структура файла генератора

Создайте файл `data_generator.py` в корневой директории вашего проекта Banking NLP System:

```python
# -*- coding: utf-8 -*-
"""
Генератор CSV данных для Banking NLP System
Создает реалистичные банковские разговоры для тестирования и обучения
"""

import csv
import json
import random
from datetime import datetime, timedelta
from path, Dict, Any
import pandas as pd
from faker import Fakerерации данных

Для создания CSV файлов с тестовыми данными в вашей Banking NLP System необходимо создать специальный модуль генератора, который будет создавать реалистичные банковские разговоры и сохранять их в структурированном формате.

## Создание генератора данных

### Структура файла генератора

Создайте файл `data_generator.py` в корневой директории вашего проекта Banking NLP System:

```python
# -*- coding: utf-8 -*-
"""
Генератор CSV данных для Banking NLP System
Создает реалистичные банковские разговоры для тестирования и обучения
"""

import csv
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd
from faker import Faker as pd
from faker import Faker

class BankingDataGenerator:
    def __init__(self):
        self.faker = Faker('ru_RU')
        self.faker.seed_instance(42)  # Для воспроизводимости результатовукты и их ключевые слерации данных

Для создания CSV файлов с тестовыми данными в вашей Banking NLP System необходимо создать специальный модуль генератора, который будет создавать реалистичные банковские разговоры и сохранять их в структурированном формате.

## Создание генератора данных

### Структура файла генератора

Создайте файл `data_generator.py` в корневой директории вашего проекта Banking NLP System:

```python
# -*- coding: utf-8 -*-
"""
Генератор CSV данных для Banking NLP System
Создает реалистичные банковские разговоры для тестирования и обучения
"""

import csv
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd
from faker import Faker

class BankingDataGenerator:
    def __init__(self):
        self.faker = Faker('ru_RU')
        self.faker.seed_instance(42)  # Для воспроизводимости результатов
        
        # Банковские продукты и их ключевые слукты и их ключевые слова
        self.products = {
            'кредит': ['кредит', 'займ', 'ссуда', 'кредитование'],
            'вклад': ['вклад', 'депозит', 'накопления', 'сбережения'],
            'карточка', 'платежипотека': ['ипотека',хование': ['страховка', 'страхование', 'полис']
        }
        
        # Тересует', 'расскажите о'],
            'поддержка': ['не работает', 'проблема с', 'не могу войти'],
            'ен', 'жалуюсь', 'плохое обслуживание'],
            'информация': ['как работает', 'какерации данных

Для создания CSV файлов с тестовыми данными в вашей Banking NLP System необходимо создать специальный модуль генератора, который будет создавать реалистичные банковские разговоры и сохранять их в структурированном формате.

## Создание генератора данных

### Структура файла генератора

Создайте файл `data_generator.py` в корневой директории вашего проекта Banking NLP System:

```python
# -*- coding: utf-8 -*-
"""
Генератор CSV данных для Banking NLP System
Создает реалистичные банковские разговоры для тестирования и обучения
"""

import csv
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd
from faker import Faker

class BankingDataGenerator:
    def __init__(self):
        self.faker = Faker('ru_RU')
        self.faker.seed_instance(42)  # Для воспроизводимости результатов
        
        # Банковские продукты и их ключевые слова
        self.products = {
            'кредит': ['кредит', 'займ', 'ссуда', 'кредитование'],
            'вклад': ['вклад', 'депозит', 'накопления', 'сбережения'],
            'карта': ['карта', 'карточка', 'платежная карта'],
            'ипотека': ['ипотека', 'жилищный кредит', 'недвижимость'],
            'страхование': ['страховка', 'страхование', 'полис']
        }
        
        # Тематики разговоров
        self.themes = {
            'продажи': ['хочу оформить', 'интересует', 'расскажите о'],
            'поддержка': ['не работает', 'проблема с', 'не могу войти'],
            'жалобы': ['недоволен', 'жалуюсь', 'плохое обслуживание'],
            'информация': ['как работает', 'какация': ['как работает', 'какие условия', 'сколько стоит']
        }
