import logging

from django.core import management
from Diplom.celery import app
from django.urls import reverse_lazy

from main.utils import BankAccountIntegration


@app.task
def update_currencies():

    management.call_command('update_currencies')


@app.task
def bank_integration(login, password, user):

    BankAccountIntegration.get_accounts(login, password, user)
