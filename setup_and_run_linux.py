import subprocess
import os
import sys

# Функция для выполнения команд в оболочке
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Команда {command} успешно выполнена.")
    else:
        print(f"Ошибка при выполнении команды {command}: {result.stderr}")
        sys.exit(1)

# 1. Удаление файла db.sqlite3
db_path = 'db.sqlite3'
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Файл {db_path} успешно удален.")
else:
    print(f"Файл {db_path} не найден.")

# 2. Запуск скрипта delete_migrations.py
run_command('python3 delete_migrations.py')

# 3. Выполнение команды python manage.py makemigrations
run_command('python3 manage.py makemigrations')

# 4. Выполнение команды python manage.py migrate
run_command('python3 manage.py migrate')

# 5. Запуск скрипта load_fixtures.py
run_command('python3 load_fixtures.py')

# 6. Создание суперпользователя
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

run_command('python3 manage.py shell -c "exec(open(\'create_superuser.py\').read())"')

os.remove('create_superuser.py')
print('Суперпользователь успешно создан.')

# 7. Выполнение команды python manage.py runserver
subprocess.run('python3 manage.py runserver', shell=True)
