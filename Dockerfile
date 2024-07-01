# Используем официальный образ Python Slim для минимизации размера образа
FROM python:3.11-slim

# Установка рабочей директории в контейнере
WORKDIR /code

# Копирование файла зависимостей
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего проекта в рабочую директорию
COPY . .

# Установка переменных окружения для доступа к настройкам Django
ENV DJANGO_SETTINGS_MODULE=SGUevents.settings
ENV PYTHONPATH=/code

# Открытие порта 8887 для внешнего доступа к Django
EXPOSE 8887

# Команда для запуска Gunicorn с вашим приложением Django
CMD ["gunicorn", "SGUevents.wsgi:application", "--bind", "0.0.0.0:8887"]