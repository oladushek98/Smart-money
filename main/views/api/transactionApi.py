import json

from django.http import JsonResponse
from django.views import View

from main.models import FinancialNode, Income, Account, Cost


class GetTransactionSource(View):
    def get(self, request):
        income_source = list(
            Income.objects.filter(delete=False, user_id=request.user.id).all()
        )
        account_source = list(
            Account.objects.filter(delete=False, user_id=request.user.id).all()
        )
        res = list(map(lambda x: {'id': x.id, 'name': x.name},
                       income_source + account_source))
        return JsonResponse({'body': res})


class GetTransactionDestination(View):
    def get(self, request, pk):
        cost_destination = list(
            Cost.objects.filter(delete=False, user_id=request.user.id).all()
        )
        account_destination = list(
            Account.objects.filter(delete=False, user_id=request.user.id).all()
        )

        is_income = True if Income.objects.filter(
            id=pk).first() != None else False

        res = list(map(lambda x: {'id': x.id, 'name': x.name},
                       account_destination if is_income else cost_destination))

        return JsonResponse({'body': res if pk != 0 else []})
