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
        body['take_into_balance'] = True if is_take == '1' else False
        account = Account(**body, user_id=request.user.id)
        account.save()
        body['id'] = account.id

        return JsonResponse(body)


class AccountDelete(View):

    def put(self, request, **kwargs):
        body = json.loads(request.body)
        income = Account.objects.filter(id=int(body['id'])).first()
        income.delete = True
        income.save()
        return JsonResponse({'ok': True})
