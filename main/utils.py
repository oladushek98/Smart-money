import requests
from selenium.webdriver.firefox.options import Options
from pyvirtualdisplay import Display
from selenium.webdriver import Firefox
from selenium.webdriver.support.wait import WebDriverWait

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


class SeleniumHacks:

    @staticmethod
    def test():
        # display = Display(visible=0, size=(800, 600))
        # display.start()

        webdriver = Firefox(executable_path='/home/oladushek/Documents/iTechArt courses/Smart-money/main/geckodriver')
        webdriver.get('https://click.alfa-bank.by/webBank2/login.xhtml')

        print(webdriver.title)
        WebDriverWait(webdriver, 1000)
        # el = webdriver.find_element_by_xpath('//*[@id="frmLogin:login"]')
        # el.send_keys('36845539')
        # el = webdriver.find_element_by_id('#frmLogin:password')
        # el.send_keys('MycatMisty1998')
        btn = webdriver.find_element_by_id('#frmLogin:enterButton')
        btn.click()

        print(webdriver.current_url)
        # display.stop()


        # print(response)


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
