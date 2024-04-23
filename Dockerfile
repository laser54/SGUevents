FROM python:3.11-slim as builder

# Установка рабочей директории в контейнере
WORKDIR /code

# Копирование файла зависимостей и установка зависимостей
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копирование всего проекта в рабочую директорию
COPY . /code

# Установка переменной окружения для доступа к настройкам Django
ENV DJANGO_SETTINGS_MODULE=SGUevents.settings
ENV PATH="/code/.local/bin:${PATH}"
