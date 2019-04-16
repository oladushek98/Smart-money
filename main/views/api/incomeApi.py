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
        income = Income(**body, user_id=request.user.id)
        income.save()

        return JsonResponse({'status': True})

