import json

from django.views import View
from django.http import JsonResponse
from main.utils import convert_currency


class Converter(View):

    def put(self, request, **kwargs):
        result = 0
        body = json.loads(request.body)

        for key in body.keys():
            item = body.get(key)
            result += convert_currency(item['amount'], item['convert_from'], item['convert_to'])

        body['result'] = result

        return JsonResponse(body)
