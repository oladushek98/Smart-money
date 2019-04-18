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
