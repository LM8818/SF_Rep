"""
Тестирование модуля предобработки текста
"""
from core.data_processing.preprocessors import BankingTextPreprocessor, DialoguePreprocessor
from core.data_processing.tokenizers import BankingTokenizer
from core.data_processing.augmentation import TextAugmenter

def test_text_preprocessor():
    """
    Тестирование препроцессора текста
    """
    preprocessor = BankingTextPreprocessor()
    
    # Тестовые тексты
    texts = [
        "Я хочу оформить кредитку с лимитом 100000 руб.",
        "Мой номер карты 1234 5678 9012 3456, проверьте баланс.",
        "Отправьте выписку на email@example.com",
        "Позвоните мне по номеру +7(123)456-78-90",
        "Я хочу положить деньги на депозит под высокий процент."
    ]
    
    print("=== Тестирование препроцессора текста ===")
    for text in texts:
        processed_text = preprocessor.preprocess(text)
        print(f"Исходный текст: {text}")
        print(f"Обработанный текст: {processed_text}")
        print("-" * 50)

def test_dialogue_preprocessor():
    """
    Тестирование препроцессора диалогов
    """
    preprocessor = DialoguePreprocessor()
    
    # Тестовый диалог
    dialogue = {
        'id': '12345',
        'timestamp': '2025-06-12T10:30:00',
        'turns': [
            {'speaker': 'client', 'text': "Здравствуйте, я хочу узнать о кредитке с кэшбэком."},
            {'speaker': 'operator', 'text': "Добрый день! Мы предлагаем несколько кредитных карт с кэшбэком. Какой лимит вас интересует?"},
            {'speaker': 'client', 'text': "Примерно 100000 рублей. И еще важен процент."},
            {'speaker': 'operator', 'text': "У нас есть карта с лимитом до 150000 руб и процентной ставкой 19.9% годовых."}
        ]
    }
    
    print("\n=== Тестирование препроцессора диалогов ===")
    processed_dialogue = preprocessor.preprocess_dialogue(dialogue)
    
    print("Обработанный диалог:")
    for turn in processed_dialogue['turns']:
        print(f"{turn['speaker']}: {turn['text']}")
    
    print("\nЗапросы клиента:")
    client_queries = preprocessor.extract_client_queries(dialogue)
    for query in client_queries:
        print(f"- {query}")
    
    print("\nОтветы оператора:")
    operator_responses = preprocessor.extract_operator_responses(dialogue)
    for response in operator_responses:
        print(f"- {response}")
    print("-" * 50)

def test_tokenizer():
    """
    Тестирование токенизатора
    """
    tokenizer = BankingTokenizer()
    
    # Тестовый текст
    text = "Я хочу оформить кредитную карту с лимитом 100000 руб и сроком на 3 года."
    
    print("\n=== Тестирование токенизатора ===")
    tokens = tokenizer.tokenize(text)
    print(f"Исходный текст: {text}")
    print(f"Токены: {tokens['input_ids'].shape}")
    
    # Декодирование
    decoded_text = tokenizer.decode(tokens['input_ids'][0])
    print(f"Декодированный текст: {decoded_text}")
    print("-" * 50)

def test_augmenter():
    """
    Тестирование аугментатора текста
    """
    augmenter = TextAugmenter(seed=42)
    
    # Тестовый текст
    text = "Я хочу оформить кредит на покупку автомобиля с низкой процентной ставкой."
    
    print("\n=== Тестирование аугментатора текста ===")
    print(f"Исходный текст: {text}")
    
    # Замена синонимов
    synonym_text = augmenter.synonym_replacement(text, n=2)
    print(f"Замена синонимов: {synonym_text}")
    
    # Вставка терминов
    insertion_text = augmenter.random_insertion(text, n=1)
    print(f"Вставка терминов: {insertion_text}")
    
    # Перестановка слов
    swap_text = augmenter.random_swap(text, n=2)
    print(f"Перестановка слов: {swap_text}")
    
    # Удаление слов
    deletion_text = augmenter.random_deletion(text, p=0.1)
    print(f"Удаление слов: {deletion_text}")
    
    # Комбинированная аугментация
    augmented_texts = augmenter.augment(text, techniques=['synonym', 'insertion', 'swap', 'deletion'], n_per_technique=1)
    print("\nКомбинированная аугментация:")
    for i, aug_text in enumerate(augmented_texts, 1):
        print(f"{i}. {aug_text}")
    print("-" * 50)

if __name__ == "__main__":
    test_text_preprocessor()
    test_dialogue_preprocessor()
    test_tokenizer()
    test_augmenter()
