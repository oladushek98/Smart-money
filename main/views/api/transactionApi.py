import json

from django.http import JsonResponse
from django.views import View
from datetime import datetime

from main.models import FinancialNode, Income, Account, Cost, Transaction


class GetTransactionSource(View):
    def get(self, request):
        income_source = list(
            Income.objects.filter(delete=False, user_id=request.user.id).all()
        )
        account_source = list(
            Account.objects.filter(delete=False, user_id=request.user.id).all()
        )
        res = list(map(lambda x: {'id': f'{x.currency}/{x.id}', 'name': x.name},
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
            id=pk).first() is not None else False

        res = list(map(lambda x: {'id': f'{x.currency}/{x.id}', 'name': x.name},
                       account_destination if is_income else cost_destination))

        return JsonResponse({'body': res if pk != 0 else []})


class CreateTransaction(View):
    def put(self, request):
        body = json.loads(request.body)
        transaction = Transaction()

        transaction.transaction_from = FinancialNode.objects.filter(
            id=int(body['transaction_from'])).first()
        transaction.transaction_to = FinancialNode.objects.filter(
            id=int(body['transaction_to'])).first()
        transaction.amount = int(body['amount'])
        transaction.data_from = datetime.strptime(body['date'],
                                                  '%d.%m.%Y').date()
        transaction.user = request.user
        transaction.save()
        body['id'] = transaction.id
        body['transaction_from'] = transaction.transaction_from.name
        body['transaction_to'] = transaction.transaction_to.name
        return JsonResponse({'ok': True, 'body': body})
