from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

import json
from main.models import Cost


class CostCreate(View):

    def put(self, request, **kwargs):

        body = json.loads(request.body)
        plan = body['monthly_plan']
        body['monthly_plan'] = int(plan) if plan else 0
        cost = Cost(**body, user_id=request.user.id)
        cost.save()
        body['id'] = cost.id

        return JsonResponse(body)


class CostDelete(View):

    def put(self, request, **kwargs):
        cost_id = int(self.request.headers._store['referer'][1].split('/')[-1])
        cost = Cost.objects.filter(id=cost_id).first()
        cost.delete = True
        cost.save()
        return JsonResponse({'ok': True})
