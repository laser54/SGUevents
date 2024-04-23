#!/bin/sh

# Запускаем Gunicorn для Django
gunicorn SGUevents.wsgi:application --bind 0.0.0.0:8887 &

# Запускаем бота
python bot/main.py &

# Ждем завершения любого из процессов
wait -n

# Выход с кодом вышедшего процесса
exit $?
