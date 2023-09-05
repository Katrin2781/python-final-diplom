# импортируем из созданного нами ранее файла celery.py наш объект(экземпляр класса) celery (app)
from .celery import app
# Подключаем объект
__all__ = ('app',)