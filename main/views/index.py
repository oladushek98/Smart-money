from django.shortcuts import render

# Create your views here.
from django.views import View


class IndexView(View):
    def get(self, requset, **kwargs):
        return render(requset, 'index.html', context={})
