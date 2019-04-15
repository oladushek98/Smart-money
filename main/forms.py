from django import forms
from django.forms import Form, ModelForm
from django.core.exceptions import ValidationError
from django.conf import settings

import json
import string
import os

from main.models import UserAdditionalInfo
from django.contrib.auth.models import User


class EditBioForm(Form):
    with open(os.path.join(settings.BASE_DIR, 'main/static/main/other/currencies.json')) as f:
        currencies = json.load(f)

    choices = []

    for k, v in currencies.items():
        choices.append((k, v))

    last_name = forms.CharField(label='Last name', max_length=50)
    first_name = forms.CharField(label='First name', max_length=50)
    email = forms.EmailField(label='E-mail', max_length=30)
    currency = forms.ChoiceField(choices=choices, initial='AUD')

    def clean_last_name(self):
        last = self.data.get('last_name')

        for i in range(len(last)):
            if last[i] not in set(string.ascii_lowercase).union(set(string.ascii_uppercase)):
                raise ValidationError('Only letters are allowed')

        return last

    def clean_first_name(self):
        first = self.data.get('first_name')

        for i in range(len(first)):
            if first[i] not in set(string.ascii_lowercase).union(set(string.ascii_uppercase)):
                raise ValidationError('Only letters are allowed')

        return first
