import requests
import json
import os

from django.conf import settings

from django.core.management.base import BaseCommand


class UpdateCurrenciesWithNBRBApi:
    ALL_CURRENCIES = r'http://www.nbrb.by/API/ExRates/Rates?Periodicity=0'
    HELP = r'Update currencies from NBRB API'
    FILE_URL = r'main/static/main/other/currencies.json'

    @classmethod
    def get_currencies(cls):
        currencies = requests.get(cls.ALL_CURRENCIES)

        if currencies.status_code == 200:
            content = currencies.json()
            to_json_file = {}

            with open(os.path.join(settings.BASE_DIR, cls.FILE_URL)) as f:
                for item in content:
                    to_json_file[item['Cur_Abbreviation']] = item['Cur_Abbreviation']

                json.dump(to_json_file, f, indent=4)

                f.close()


class Command(BaseCommand):

    help = UpdateCurrenciesWithNBRBApi.HELP

    def handle(self, *args, **options):

        try:

            UpdateCurrenciesWithNBRBApi.get_currencies()

            self.stdout.write('Currencies are updated!')

        except Exception as e:
            self.stdout.write(e.args)
