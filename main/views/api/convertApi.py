import json

from django.views import View
from django.http import JsonResponse
from main.utils import convert_currency


class Converter(View):

    def get(self, request, **kwargs):

        body = kwargs
        body['result'] = convert_currency(body['amount'], body['main'], body['secondary'])

        return JsonResponse(body)
