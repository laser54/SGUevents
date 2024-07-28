# bookmarks/tasks.py
from celery import shared_task

@shared_task
def print_text():
    message = "This text is printed every 30 seconds"
    with open("task_log.txt", "a") as log_file:
        log_file.write(f"{message}\n")
    print(message)
