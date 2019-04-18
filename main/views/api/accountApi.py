from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

import json
from main.models import Account


class AccountCreate(View):

    def put(self, request, **kwargs):

        body = json.loads(request.body)
        body['is_debt_account'] = False
        amount = body['amount']
        body['amount'] = int(amount) if amount else 0
        is_take = body['take_into_balance']
        body['take_into_balance'] = False if is_take == 'false' else True
        account = Account(**body, user_id=request.user.id)
        account.save()
        body['id'] = account.id

        return JsonResponse(body)


class AccountDelete(View):

    def put(self, request, **kwargs):
        account_id = int(self.request.headers._store['referer'][1].split('/')[-1])
        account = Account.objects.filter(id=account_id).first()
        account.delete = True
        account.save()
        return JsonResponse({'ok': True})
