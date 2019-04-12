from django.urls import path, include

from main.views import index

urlpatterns = [
    path('', index.IndexView.as_view(), name='main'),
]