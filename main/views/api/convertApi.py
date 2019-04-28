import json

from django.views import View
from django.http import JsonResponse
from main.utils import convert_currency


class Converter(View):

    def put(self, request, **kwargs):

        body = json.loads(request.body)
        body['result'] = convert_currency(body['amount'], body['main'], body['secondary'])

        return JsonResponse(body)
