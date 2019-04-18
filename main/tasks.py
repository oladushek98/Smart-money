import logging

from django.core import management
from Diplom.celery import app


@app.task
def update_currencies():

    management.call_command('update_currencies')