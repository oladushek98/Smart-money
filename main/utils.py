import requests
import datetime

from io import BytesIO

from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

from xhtml2pdf import pisa

from main.models import Income, Transaction, Account, Cost


class PDFConverter:

    @staticmethod
    def render_to_pdf(template_src, context_dict={}):
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)

        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')

        return None


class ReportSender:

    @staticmethod
    def send_report():

        users = User.objects.filter(~Q(email=''))
        print(users)

        for user in users:

            msg = EmailMultiAlternatives('test', 'test', to=['vladislavpliska@mail.ru'])

            incomes = Income.objects.filter(user_id=user.id, delete=False)
            accounts = Account.objects.filter(user_id=user.id, delete=False)
            costs = Cost.objects.filter(user_id=user.id, delete=False)

            date = datetime.datetime.today()
            temp = date - datetime.timedelta(days=30)
            transactions = Transaction.objects.filter(data_from__gte=temp,
                                                      # data_from__year=temp.year,
                                                      user_id=user.id).prefetch_related('transaction_from',
                                                                                        'transaction_to').all()

            context = {
                'transactions': transactions,
                'period': f', your report from {temp} to {date}',
                'user': 'Vlad',
                'incomes': incomes,
                'costs': costs,
                'accounts': accounts
            }

            pdf = PDFConverter.render_to_pdf('report/report.html', context)

            msg.attach_alternative(pdf.content, 'application/pdf')
            msg.send()
        # send_mail(
        #     'just testing',
        #     'test',
        #     'drakulaxxl3@gmail.com',
        #     ['vladislavpliska@mail.ru'],
        #     fail_silently=False
        # )


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
    result = int(amount)*rate
    return result


def convert_from_byn(amount: int, currency: str):
    rate = get_value_currency(currency)
    result = int(amount)/rate
    return result


def convert_currency(amount: int, convert_from: str, convert_to: str):
    result = 0

    if convert_from != "BYN" and convert_to != "BYN":
        convert_from_into_byn = convert_into_byn(amount, convert_from)
        byn_into_convert_to = convert_from_byn(convert_from_into_byn, convert_to)
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
