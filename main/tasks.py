import logging

from smtplib import SMTPException
from django.core import management
from Diplom.celery import app
from main.utils import BankAccountIntegration

from main.utils import ReportSender


@app.task
def update_currencies():

    management.call_command('update_currencies')


@app.task
def send_reports():
    try:
        subject = 'Monthly reports about your statement'
        text = 'here is your report! If there is any mistake - please, contact us back!'

        ReportSender.send_report(subject, text)
        logging.info('Emails are sent!')

    except SMTPException:
        logging.warning('Some mistake here!')



@app.task
def bank_integration(login, password, user):
    BankAccountIntegration.get_accounts(login, password, user)
