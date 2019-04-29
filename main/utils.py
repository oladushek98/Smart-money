import requests

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa


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
    result = amount*rate
    return result


def convert_from_byn(amount: int, currency: str):
    rate = get_value_currency(currency)
    result = amount/rate
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

    return round(result, 2)
