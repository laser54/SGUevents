import subprocess
import os
import sys
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Функция для выполнения команд в оболочке
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Команда {command} успешно выполнена.")
    else:
        print(f"Ошибка при выполнении команды {command}: {result.stderr}")
        sys.exit(1)

# Перезапуск базы данных PostgreSQL
def recreate_postgres_db():
    try:
        conn = psycopg2.connect(
            dbname='postgres',  # Подключаемся к служебной базе данных
            user=os.getenv("LOCAL_DB_USER"),
            password=os.getenv("LOCAL_DB_PASSWORD"),
            host=os.getenv("LOCAL_DB_HOST"),
            port=os.getenv("LOCAL_DB_PORT")
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(os.getenv("LOCAL_DB_NAME"))))
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(os.getenv("LOCAL_DB_NAME"))))
        cursor.close()
        conn.close()
        print(f"База данных {os.getenv('LOCAL_DB_NAME')} успешно пересоздана.")
    except Exception as e:
        print(f"Ошибка при перезапуске базы данных PostgreSQL: {e}")
        sys.exit(1)

# Перезапуск БД
recreate_postgres_db()

run_command('python delete_migrations.py')
run_command('python manage.py makemigrations')
run_command('python manage.py migrate')
run_command('python load_fixtures.py')

# Создание суперпользователя
create_superuser_command = """
from django.contrib.auth import get_user_model

User = get_user_model()
if not User.objects.filter(username='Admin').exists():
    User.objects.create_superuser(email='ad@min.com', password='root', username='Admin')
else:
    print('Суперпользователь уже существует.')
"""

with open('create_superuser.py', 'w') as f:
    f.write(create_superuser_command)

run_command('python manage.py shell -c "exec(open(\'create_superuser.py\').read())"')

os.remove('create_superuser.py')
print('Суперпользователь успешно создан.')

# runserver
subprocess.run('python manage.py runserver', shell=True)
