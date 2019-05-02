from django import forms
from django.forms import Form
from django.core.exceptions import ValidationError
from django.conf import settings
from bootstrap_datepicker_plus import DatePickerInput

import json
import string
import os
import datetime


class EditBioForm(Form):
    with open(os.path.join(settings.BASE_DIR,
                           'main/static/main/other/currencies.json'), 'r') as f:
        currencies = json.load(f)

    choices = []

    for k, v in currencies.items():
        choices.append((k, v))

    last_name = forms.CharField(label='Last name', max_length=50)
    first_name = forms.CharField(label='First name', max_length=50)
    email = forms.EmailField(label='E-mail', max_length=30)
    currency = forms.ChoiceField(choices=choices)

    def clean_last_name(self):
        last = self.data.get('last_name')

        for i in range(len(last)):
            if last[i] not in set(string.ascii_lowercase).union(
                    set(string.ascii_uppercase)):
                raise ValidationError('Only letters are allowed')

        return last

    def clean_first_name(self):
        first = self.data.get('first_name')

        for i in range(len(first)):
            if first[i] not in set(string.ascii_lowercase).union(
                    set(string.ascii_uppercase)):
                raise ValidationError('Only letters are allowed')

        return first


class IncomeForm(Form):
    with open(os.path.join(settings.BASE_DIR,
                           'main/static/main/other/currencies.json'), 'r') as f:
        currencies = json.load(f)

    choices = []

    for k, v in currencies.items():
        choices.append((k, v))

    name = forms.CharField(label='Название', max_length=50)
    monthly_plan = forms.IntegerField(label='Планирую получать в месяц')
    currency = forms.ChoiceField(choices=choices, label='Валюта')


class AccountForm(Form):
    with open(os.path.join(settings.BASE_DIR,
                           'main/static/main/other/currencies.json'), 'r') as f:
        currencies = json.load(f)

    choices = []

    for k, v in currencies.items():
        choices.append((k, v))

    name = forms.CharField(label='Название', max_length=50)
    amount = forms.IntegerField(label='Сейчас на счете')
    currency = forms.ChoiceField(choices=choices, label='Валюта')
    take_into_balance = forms.BooleanField(label='Учитывать в общем балансе?')


class CostForm(Form):
    with open(os.path.join(settings.BASE_DIR,
                           'main/static/main/other/currencies.json'), 'r') as f:
        currencies = json.load(f)

    choices = []

    for k, v in currencies.items():
        choices.append((k, v))

    name = forms.CharField(label='Название', max_length=50)
    monthly_plan = forms.IntegerField(label='Планируете тратить в месяц')
    currency = forms.ChoiceField(choices=choices, label='Валюта')


class TransactionCreateForm(Form):
    transaction_from = forms.ChoiceField(choices=[])
    transaction_to = forms.ChoiceField(choices=[])
    choice_currency = forms.ChoiceField(choices=[])
    amount = forms.IntegerField()
    data_from = forms.DateField(widget=forms.SelectDateWidget)


class ReportGenerationForm(Form):

    period_choices = [('day', 'Day'),
                      ('week', 'Week'),
                      ('month', 'Month'),
                      ('year', 'Year'),
                      ('whole', 'Whole history')]

    node_objects = [('incomes', 'Incomes'),
                    ('accounts', 'Accounts'),
                    ('costs', 'Costs')]

    period = forms.ChoiceField(choices=period_choices, widget=forms.RadioSelect)
    nodes = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=node_objects,
    )


class TransactionUpdateForm(Form):
    transaction_from = forms.CharField(disabled=True, label='из',
                                       required=False)
    transaction_to = forms.CharField(disabled=True, label='в', required=False)
    choice_currency = forms.CharField(disabled=True, label='валюта',
                                      required=False)
    amount = forms.IntegerField(label='сумма')
    data_from = forms.DateField(widget=forms.SelectDateWidget, disabled=True,
                                label='дата', required=False)
