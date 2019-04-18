from django.http import JsonResponse
from django.views import View


class GetTransactionSource(View):
    def get(self, request):
        body = {}
        return JsonResponse(body)
