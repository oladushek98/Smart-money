import requests


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


def convert_currency(amount: int, main: str, secondary: str):
    result = 0

    if main != "BYN" and secondary != "BYN":
        main_into_byn = convert_into_byn(amount, main)
        byn_into_secondary = convert_from_byn(main_into_byn, secondary)
        result = byn_into_secondary

    elif main == "BYN" and secondary == "BYN":
        result = amount

    elif main != "BYN":
        main_into_byn = convert_into_byn(amount, main)
        result = main_into_byn

    else:
        byn_into_secondary = convert_from_byn(amount, secondary)
        result = byn_into_secondary

    return round(result, 2)
