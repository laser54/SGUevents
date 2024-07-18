from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from django.db.models.signals import post_migrate
        from scheduler_startup import check_tables_and_start_scheduler
        post_migrate.connect(check_tables_and_start_scheduler, sender=self)

