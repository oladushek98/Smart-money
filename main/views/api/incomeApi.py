from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

import json
from main.models import Income


class IncomeCreate(View):

    def put(self, request, **kwargs):

        body = json.loads(request.body)
        plan = body['monthly_plan']
        body['monthly_plan'] = int(plan) if plan else 0
        income = Income(**body)
        income.user = request.user.id
        income.save()
        body['id'] = income.id

        return JsonResponse(body)


class IncomeDelete(View):

    def put(self, request, **kwargs):
        body = json.loads(request.body)
        income = Income.objects.filter(id=int(body['id'])).first()
        income.delete = True
        income.save()
        return JsonResponse({'ok': True})
