import logging

from django.core import management
from Diplom.celery import app

from main.utils import SeleniumHacks


@app.task
def update_currencies():

    management.call_command('update_currencies')


@app.task
def test():

    SeleniumHacks.test()
