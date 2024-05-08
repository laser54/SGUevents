from django.core.management.base import BaseCommand
from bot.main import run_bot  # Правильный импорт функции run_bot
import asyncio

class Command(BaseCommand):
    help = 'Запускает телеграм-бота'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Запускаю бота...'))
        asyncio.run(run_bot())


