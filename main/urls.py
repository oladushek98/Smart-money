from django.urls import path, include

from main.views.api import incomeApi
from main.views import index, authentication, user, income

urlpatterns = [
    path('', index.IndexView.as_view(), name='main'),
    path('auth/register/', authentication.RegisterView.as_view(),
         name='register'),
    path('auth/login/', authentication.LoginView.as_view(), name='login'),
    path('auth/logout/', authentication.LogoutView.as_view(), name='logout'),
    path('user', index.UserpageView.as_view(), name='userpage'),
    path('user/<int:pk>/edit', user.UserUpdateBioView.as_view(),
         name='edit_user'),
    path('api/income/create', incomeApi.IncomeCreate.as_view(),
         name='create_income'),
    path('api/income/delete', incomeApi.IncomeDelete.as_view(),
         name='delete_income'),
    path('income/<int:pk>', income.IncomeUpdateView.as_view(),
         name='update_income'),
]
