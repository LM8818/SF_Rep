import os
import pandas as pd
import logging
from logging.handlers import RotatingFileHandler
from sklearn.metrics import (
    classification_report, accuracy_score, confusion_matrix,
    roc_auc_score, precision_recall_curve, average_precision_score, f1_score
)
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import json

# Для explainability (если требуется)
try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False

log_formatter = logging.Formatter(
    '{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "message": "%(message)s"}'
)
log_handler = RotatingFileHandler('logs/evaluation.log', maxBytes=1000000, backupCount=3, encoding='utf-8')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

PREDICTIONS_PATH = 'data/processed/predictions.csv'
MODEL_PATH = 'models/logreg_model.joblib'
METRICS_PATH = 'reports/metrics_latest.json'
BUSINESS_COST_MATRIX = {
    ('жалоба', 'информация'): 10,
    ('информация', 'жалоба'): 2,
    # Добавьте остальные пары по бизнес-логике
}

def plot_confusion_matrix(y_true, y_pred, labels):
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.xlabel('Предсказанный класс')
    plt.ylabel('Истинный класс')
    plt.title('Матрица ошибок')
    plt.tight_layout()
    os.makedirs('reports/figures', exist_ok=True)
    plt.savefig('reports/figures/confusion_matrix.png')
    plt.close()

def compute_cost_sensitive_metric(y_true, y_pred):
    total_cost = 0
    for true_label, pred_label in zip(y_true, y_pred):
        if true_label != pred_label:
            cost = BUSINESS_COST_MATRIX.get((true_label, pred_label), 1)
            total_cost += cost
    return total_cost

def save_metrics(metrics_dict, path=METRICS_PATH):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(metrics_dict, f, ensure_ascii=False, indent=2)

def evaluate():
    """
    Расширенная оценка модели: классические, бизнес-, регуляторные метрики и explainability.
    """
    try:
        if not os.path.exists(PREDICTIONS_PATH):
            logger.error('Файл с предсказаниями не найден. Оценка невозможна.')
            return

        df = pd.read_csv(PREDICTIONS_PATH)
        if 'theme' not in df.columns or 'predicted_theme' not in df.columns:
            logger.error('В файле отсутствуют необходимые колонки для оценки.')
            return

        y_true = df['theme']
        y_pred = df['predicted_theme']
        labels = sorted(list(set(y_true) | set(y_pred)))

        # 1. Классические метрики
        acc = accuracy_score(y_true, y_pred)
        f1_macro = f1_score(y_true, y_pred, average='macro')
        report = classification_report(y_true, y_pred, digits=3)
        logger.info(f'Accuracy: {acc:.3f}')
        logger.info(f'Macro F1-score: {f1_macro:.3f}')
        logger.info('\n' + report)
        print(f'Accuracy: {acc:.3f}')
        print(f'Macro F1-score: {f1_macro:.3f}')
        print(report)

        # 2. Матрица ошибок
        plot_confusion_matrix(y_true, y_pred, labels)
        logger.info('Матрица ошибок сохранена в reports/figures/confusion_matrix.png')

        # 3. Бизнес-метрика (cost-sensitive)
        cost = compute_cost_sensitive_metric(y_true, y_pred)
        logger.info(f'Суммарная стоимость ошибок по бизнес-метрике: {cost}')
        print(f'Суммарная стоимость ошибок (бизнес-метрика): {cost}')

        # 4. ROC-AUC и PR-AUC (если задача бинарная)
        if len(labels) == 2 and 'predicted_proba' in df.columns:
            roc_auc = roc_auc_score(y_true, df['predicted_proba'])
            logger.info(f'ROC-AUC: {roc_auc:.3f}')
            print(f'ROC-AUC: {roc_auc:.3f}')
            precision, recall, _ = precision_recall_curve(y_true, df['predicted_proba'])
            pr_auc = average_precision_score(y_true, df['predicted_proba'])
            logger.info(f'PR-AUC: {pr_auc:.3f}')
            print(f'PR-AUC: {pr_auc:.3f}')

        # 5. Explainability (SHAP)
        if SHAP_AVAILABLE and os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            feature_cols = [col for col in df.columns if col not in ['theme', 'predicted_theme']]
            X = df[feature_cols].select_dtypes(include=['number'])
            if X.shape[1] > 0:
                explainer = shap.Explainer(model, X)
                shap_values = explainer(X)
                shap.summary_plot(shap_values, X, show=False)
                os.makedirs('reports/figures', exist_ok=True)
                plt.tight_layout()
                plt.savefig('reports/figures/shap_summary.png')
                plt.close()
                logger.info('SHAP summary plot сохранён в reports/figures/shap_summary.png')

        # 6. Сохранение метрик для мониторинга
        metrics = {
            'accuracy': acc,
            'macro_f1': f1_macro,
            'business_cost': cost
        }
        save_metrics(metrics)
        logger.info(f'Метрики сохранены в {METRICS_PATH}')

    except Exception as e:
        logger.error(f'Ошибка при оценке модели: {e}')

if __name__ == '__main__':
    evaluate()
