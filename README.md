# SGUevents

![Python](https://img.shields.io/badge/python-3.11-3776AB?logo=python)&nbsp;
![Django](https://img.shields.io/badge/django-4.2-092E20?logo=django)&nbsp;
![DRF](https://img.shields.io/badge/DRF-3.15-ff1709?logo=django&logoColor=white)&nbsp;
![aiogram](https://img.shields.io/badge/aiogram-3.11-2CA5E0?logo=telegram&logoColor=white)&nbsp;
![Postgres](https://img.shields.io/badge/postgres-14-336791?logo=postgresql)&nbsp;
![Redis](https://img.shields.io/badge/redis-6.2-a41e11?logo=redis)&nbsp;
![Celery](https://img.shields.io/badge/celery-5.4-37814A?logo=celery)&nbsp;
![Gunicorn](https://img.shields.io/badge/gunicorn-20.1-499848?logo=gunicorn&logoColor=white)&nbsp;
![Nginx](https://img.shields.io/badge/nginx-1.21-009639?logo=nginx)&nbsp;
![Docker](https://img.shields.io/badge/docker-compose%203.8-0db7ed?logo=docker)

## Содержание

- [Обзор](#обзор)
- [TL;DR](#tldr)
- [Структура проекта](#структура-проекта)
- [Переменные окружения](#переменные-окружения)
- [Локальный запуск (LinuxmacOS)](#локальный-запуск-linuxmacos)
- [Локальный запуск (Windows)](#локальный-запуск-windows-1011-powershell)
- [Продакшен  VPS](#продакшен--vps)

## Обзор

Платформа мероприятий объединяет витрины онлайн/офлайн событий, каталоги достопримечательностей, личный кабинет с закладками, административные процессы и Telegram-механики (логин, бот, мини-приложение). Основной стек: Django + DRF, Celery + Redis, PostgreSQL, отдельный aiogram-бот, Nginx и docker-compose для продакшена.

- мульти-лендинги: события, календарь, культурные объекты, персональные подборки;
- кастомная регистрация/логин через Telegram Login Widget, Telegram Mini App и напрямую из Telegram-бота (aiogram 3);
- уведомления, отложенные публикации и бэкофис-процессы на Celery/Redis;
- автономный бот (`bot/main.py`) для рассылок и обратной связи;
- интеграция с Yandex Disk для документов;
- сопровождающие скрипты для создания департаментов, суперпользователя и загрузки фикстур.

## TL;DR

```
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
touch .env  # заполняем по таблице ниже, обязательно ALLOWED_HOSTS/WEBHOOK_HOST
python manage.py migrate
python manage.py loaddata fixtures/events_available/events_online.json
python manage.py runserver 127.0.0.1:8000 --noreload & python manage.py startbot --noreload
# параллельно (другие терминалы/сессии)
celery -A SGUevents worker -l info -P solo  # без -P solo только на Linux/macOS
celery -A SGUevents beat -l info
```

## Структура

- `SGUevents/` — конфигурация Django, Celery, маршруты, SSL-настройки для Telegram WebApp.
- `users`, `bookmark`, `events_*`, `personal`, `support` — доменные приложения.
- `bot/` — aiogram 3.x бот, инициализируется через `python bot/main.py`.
- `Dockerfile`, `docker-compose.yml`, `nginx.conf` — образ и оркестрация (gunicorn на 8887, Nginx на 8080, отдельные celery worker/beat).
- `fixtures/` — готовые данные для наполнения страниц.
- `setup_and_run_*.py` — вспомогательные скрипты (необязательно, но повторяют инструкции ниже).

## Переменные окружения

Создайте `.env` в корне (рядом с `docker-compose.yml`). Минимум:

| Ключ | Что задать |
| --- | --- |
| `DJANGO_ENV` | `development` локально, `production`/любое другое на сервере (влияет на БД и токены) |
| `SECRET_KEY` | собственный Django secret |
| `LOCAL_DB_*` | имя/логин/пароль/хост/порт локальной PostgreSQL (используются когда `DJANGO_ENV=development`) |
| `DB_NAME`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `DB_HOST`, `DB_PORT` | боевой Postgres/контейнер |
| `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND` | `redis://redis:6379/0` или `redis://localhost:6379/0` |
| `TELEGRAM_BOT_TOKEN`, `TELEGRAM_DEV_BOT_TOKEN` | токены рабочего и дев-бота |
| `ADMIN_TG_NAME`, `DEV_SUPPORT_CHAT_ID`, `SUPPORT_CHAT_ID` | сервисные чаты/админы |
| `WEBHOOK_HOST` | `https://subdomain.yourdomain.ru` (поддомен на VPS/HTTPS-туннеле) |
| `BOT_NAME`, `DEV_BOT_NAME`, `TELEGRAM_BOT_SECRET` | параметры логина/миниаппа |
| `YANDEX_DISK_CLIENT_ID`, `YANDEX_DISK_CLIENT_SECRET`, `YANDEX_DISK_OAUTH_TOKEN` | по необходимости |

Следует добавить используемый поддомен в `ALLOWED_HOSTS` и `CSRF_TRUSTED_ORIGINS` (правка в `SGUevents/settings.py` или через env-переменные и доп. код).

## Локальный запуск (Linux/macOS)

1. **Зависимости**: Python 3.11 (обязателен для совместимости), PostgreSQL ≥14, Redis ≥6, Node.js не нужен.
2. **Виртуальное окружение**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip wheel
   pip install -r requirements.txt
   ```
3. **PostgreSQL**: создаём базу и пользователя (пример: `createdb sguevents_local`, `createuser --pwprompt sguevents`). Прописываем значения в `.env` (`LOCAL_DB_NAME`, `LOCAL_DB_USER`, `LOCAL_DB_PASSWORD`, `LOCAL_DB_HOST=127.0.0.1`).
4. **Миграции и данные**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py loaddata fixtures/events_available/events_online.json
   python manage.py loaddata fixtures/events_available/events_offline.json
   python manage.py loaddata fixtures/events_cultural/attractions.json
   python manage.py loaddata fixtures/events_cultural/events_for_visiting.json
   python manage.py loaddata fixtures/departments.json
   ```
5. **Статика**: `python manage.py collectstatic --noinput`
6. **Сервисы**:
   - Django + встроенный `startbot`: `python manage.py runserver 127.0.0.1:8000 --noreload & python manage.py startbot --noreload`
   - Celery worker: `celery -A SGUevents worker -l info` (или `-P solo`, если Windows/WSL)
   - Celery beat: `celery -A SGUevents beat -l info`
   - Отдельный aiogram-бот (альтернатива команде `startbot`): `python bot/main.py`
   - На macOS/Linux удобно держать всё в `tmux`, `honcho`, `foreman`, `taskfile`.
7. **Telegram Login Widget** **не** работает без внешнего HTTPS-домена/поддомена. Даже для локальной разработки нужен внешний URL (ngrok/caddy/VPS), иначе Telegram не отдаст данные авторизации. Быстрый вариант:
   ```bash
   ngrok http 8000
   export WEBHOOK_HOST="https://<random>.ngrok-free.app"
   ```

## Локальный запуск (Windows 10/11, PowerShell)

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
python -m venv venv
.\venv\Scripts\activate
pip install --upgrade pip wheel
pip install -r requirements.txt
```

- Redis: проще всего поднять в Docker Desktop `docker run --name redis -p 6379:6379 -d redis:latest`
- PostgreSQL: либо локальный сервис, либо контейнер `docker run --name postgres -e POSTGRES_PASSWORD=secret -p 5432:5432 -d postgres:14`
- Миграции/fixtures команды такие же, только `python` вместо `python3`.
- Основной запуск: `python manage.py runserver 127.0.0.1:8000 --noreload & python manage.py startbot --noreload`
- Celery worker всегда с `-P solo`: `celery -A SGUevents worker -l info -P solo`
- Celery beat: `celery -A SGUevents beat -l info`
- Авторизация через Telegram Login Widget заработает только если зайти по внешнему HTTPS-домену (ngrok/поддомен на VPS). Локальный вариант: `ngrok http http://localhost:8000` и подставить URL в `WEBHOOK_HOST`.

## Продакшен / VPS с поддоменом

1. **DNS**: в панели регистрации домена прописать `A`-запись `events.example.ru → <IP VPS>`. При необходимости добавить `CNAME` или `AAAA`.
2. **Файлы**: на сервер заливаются `.env`, `docker-compose.yml`, `nginx.conf`, каталоги `static/` и `media/`. Рекомендуемая директория — `/opt/sguevents`.
3. **.env для продакшена**:
   ```
   DJANGO_ENV=production
   DB_HOST=db
   DB_PORT=5432
   DB_NAME=sguevents
   POSTGRES_USER=sgu
   POSTGRES_PASSWORD=<strong_pass>
   WEBHOOK_HOST=https://events.example.ru
   CELERY_BROKER_URL=redis://redis:6379/0
   CELERY_RESULT_BACKEND=redis://redis:6379/0
   ```
   Тот же поддомен требуется в `ALLOWED_HOSTS` и `CSRF_TRUSTED_ORIGINS`. Если используется внешний reverse-proxy, домен указывается именно тот, который видит браузер.
4. **Старт стека**:
   ```bash
   docker compose pull
   docker compose --env-file .env up -d db redis
   sleep 5
   docker compose --env-file .env up -d backend bot celery celery_beat nginx
   ```
   При необходимости все сервисы запускаются одной командой `docker compose --env-file .env up -d`.
5. **Миграции внутри контейнера**:
   ```bash
   docker compose exec backend python manage.py migrate
   docker compose exec backend python manage.py collectstatic --noinput
   docker compose exec backend python manage.py createsuperuser
   docker compose exec backend python manage.py loaddata fixtures/events_available/events_online.json
   ```
6. **Сброс схемы** (при зависших миграциях):
   ```bash
   docker exec -it $(docker ps -qf name=db) psql -U $POSTGRES_USER -d $DB_NAME
   DROP SCHEMA public CASCADE;
   CREATE SCHEMA public;
   \q
   ```
7. **SSL**: Nginx (см. `nginx.conf`) лучше всего завернуть в Certbot, Caddy или другой ACME-клиент. Telegram WebApp и Login Widget требуют полноценный HTTPS, иначе из-за `SECURE_SSL_REDIRECT` проект недоступен.

