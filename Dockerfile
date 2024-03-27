FROM python:3.11-slim as builder
WORKDIR /code
COPY requirements.txt .
RUN pip3 install --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /code
COPY --from=builder /root/.local /root/.local
COPY . .
# Установка переменной окружения для использования пакетов, установленных в --user
ENV PATH=/root/.local/bin:$PATH
# Используйте Gunicorn в качестве WSGI сервера для запуска приложения
CMD gunicorn SGUevents.wsgi:application --bind 0.0.0.0:8887