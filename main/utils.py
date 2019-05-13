import requests
import logging
import os

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, \
    ElementClickInterceptedException, WebDriverException

import datetime

from io import BytesIO

from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives, get_connection
from django.contrib.auth.models import User

from Diplom.settings import STATIC_URL

from xhtml2pdf import pisa

from Diplom import settings
from main.models import Income, Transaction, Account, Cost


class PDFConverter:

    @staticmethod
    def fetch_pdf_resources(uri, rel):
        path = 'main' + uri
        return path

    @staticmethod
    def render_to_pdf(template_src, context_dict={}):
        context_dict.update({'static': STATIC_URL})
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')),
                                result,
                                encoding='utf-8',
                                link_callback=PDFConverter.fetch_pdf_resources)

        if not pdf.err:
            return HttpResponse(result.getvalue(),
                                content_type='application/pdf')

        return None


class BankAccountIntegration:

    @staticmethod
    def get_accounts(login, password, user):
        # display = Display(visible=0, size=(800, 600))
        # display.start()

        alphabank = 'https://click.alfa-bank.by/webBank2/login.xhtml'
        # driver_path = os.path.join(os.getcwd(), 'main/geckodriver')

        # chrome_options = Options()
        # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN", "chromedriver")
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--no-sandbox')
        # webdriver = Chrome(executable_path='/app/.chromedriver/bin/chromedriver', chrome_options=chrome_options)
        webdriver = Chrome(r'/app/.chromedriver/bin/chromedriver')

        try:
            webdriver.set_window_size(1080, 720)
            webdriver.get(alphabank)
            print(webdriver.title)
            print(webdriver.page_source)

            el = WebDriverWait(webdriver, 1000).until(
                EC.presence_of_element_located((By.ID, 'frmLogin:login')))
            el.send_keys(login)

            el = WebDriverWait(webdriver, 1000).until(
                EC.presence_of_element_located((By.ID, 'frmLogin:password')))
            el.send_keys(password)

            btn = WebDriverWait(webdriver, 1000).until(
                EC.presence_of_element_located((By.ID, 'frmLogin:enterButton')))
            btn.click()

            url = webdriver.current_url
            print(url)
            if 'disconnect' in url:
                raise WebDriverException

            table = WebDriverWait(webdriver, 1000).until(
                EC.presence_of_element_located((By.ID, 'accountsTable_data')))

            print(table.text)

            temp = table.text
            temp = temp.replace('$', 'USD')
            temp = temp.replace('€', 'EUR')
            temp = temp.replace('Br', 'BYN')

            info = temp.split('\n')
            info_new = [subj for subj in info if subj != '']
            del info

            accounts = [(info_new[i],
                         round(float(info_new[i + 1].replace(',', '.'))),
                         info_new[i + 2])
                        for i in range(0, len(info_new), 3)]

            for account in accounts:
                Account.objects.update_or_create(user_id=user, name=account[0],
                                                 currency=account[2],
                                                 defaults={'user_id': user,
                                                           'is_debt_account': False,
                                                           'take_into_balance': True,
                                                           'name': account[0],
                                                           'currency': account[2],
                                                           'amount': account[1],
                                                           'delete': False})

            print(accounts)

            return True

        except NoSuchElementException:
            logging.warning('No such element!')
            return False

        except ElementClickInterceptedException:
            logging.warning('The element is blocked!')
            return False

        except WebDriverException:
            logging.warning('Disconnected!')
            return False

        finally:
            # display.stop()
            pass


class ReportSender:

    @staticmethod
    def send_report(subject, text):
        users = User.objects.filter(~Q(email=''))
        messages = []

        connection = get_connection()
        connection.open()

        for user in users:
            msg = EmailMultiAlternatives(subject=subject,
                                         body=f'Dear {user.username.title()}, {text}',
                                         to=[user.email])

            incomes = Income.objects.filter(user_id=user.id, delete=False)
            accounts = Account.objects.filter(user_id=user.id, delete=False)
            costs = Cost.objects.filter(user_id=user.id, delete=False)

            date = datetime.datetime.today()
            temp = date - datetime.timedelta(days=30)
            transactions = Transaction.objects.filter(data_from__gte=temp,
                                                      user_id=user.id).prefetch_related(
                'transaction_from',
                'transaction_to').all()

            context = {
                'transactions': transactions,
                'period': f', your report from {temp} to {date}',
                'user': f'Dear {user.username.title()}',
                'incomes': incomes,
                'costs': costs,
                'accounts': accounts
            }

            pdf = PDFConverter.render_to_pdf('report/report.html', context)

            # filename = f'Report_{user.username}_month_from_{temp}_to_{date}'
            # content = f'inline; filename=\'{filename}\''
            # pdf['Content-Disposition'] = content

            msg.attach_alternative(pdf.content, 'application/pdf')

            messages.append(msg)

        connection.send_messages(messages)
        connection.close()


def get_value_currency(currency: str):
    api_url = "http://www.nbrb.by/API/ExRates/Rates/"

    params = {
        "ParamMode": 2,
    }

    response = requests.get(api_url + currency, params)

    if response.status_code == 200:
        data = response.json()
        return data["Cur_OfficialRate"] / data["Cur_Scale"]

    else:
        raise ValueError("CURRENCY IS INCORRECT")


def convert_into_byn(amount: int, currency: str):
    rate = get_value_currency(currency)
    result = int(amount) * rate
    return result


def convert_from_byn(amount: int, currency: str):
    rate = get_value_currency(currency)
    result = int(amount) / rate
    return result


def convert_currency(amount: int, convert_from: str, convert_to: str):
    result = 0

    if convert_from != "BYN" and convert_to != "BYN":
        convert_from_into_byn = convert_into_byn(amount, convert_from)
        byn_into_convert_to = convert_from_byn(convert_from_into_byn,
                                               convert_to)
        result = byn_into_convert_to

    elif convert_from == "BYN" and convert_to == "BYN":
        result = amount

    elif convert_from != "BYN":
        convert_from_into_byn = convert_into_byn(amount, convert_from)
        result = convert_from_into_byn

    else:
        byn_into_convert_to = convert_from_byn(amount, convert_to)
        result = byn_into_convert_to

    return int(result)
