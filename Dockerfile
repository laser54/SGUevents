FROM python:3.11-slim as builder
WORKDIR /code
COPY requirements.txt .
RUN pip3 install --user -r requirements.txt
ENV DJANGO_SETTINGS_MODULE=SGUevents.settings

FROM python:3.11-slim
WORKDIR /code
COPY --from=builder /root/.local /root/.local
COPY . .
# Установка переменной окружения для использования пакетов, установленных в --user
ENV PATH=/root/.local/bin:$PATH
# Создаем entrypoint скрипт, который будет запускать и бота, и Django
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# CMD заменен на entrypoint
ENTRYPOINT ["/entrypoint.sh"]