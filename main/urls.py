from django.urls import path, include

from main.views.api import incomeApi, accountApi, costApi, transactionApi, \
    convertApi
from main.views import index, authentication, user, income, account, cost, \
    transaction

urlpatterns = [
    path('', index.IndexView.as_view(), name='main'),
    path('auth/register/', authentication.RegisterView.as_view(),
         name='register'),
    path('auth/login/', authentication.LoginView.as_view(), name='login'),
    path('auth/logout/', authentication.LogoutView.as_view(), name='logout'),
    path('user', index.UserpageView.as_view(), name='userpage'),
    path('user/edit', user.UserUpdateBioView.as_view(), name='edit_user'),
    path('api/income/create', incomeApi.IncomeCreate.as_view(),
         name='create_income'),
    path('api/income/delete', incomeApi.IncomeDelete.as_view(),
         name='delete_income'),
    path('income/<int:pk>', income.IncomeUpdateView.as_view(),
         name='update_income'),
    path('api/account/create', accountApi.AccountCreate.as_view(),
         name='create_account'),
    path('account/<int:pk>', account.AccountUpdateView.as_view(),
         name='update_account'),
    path('api/account/delete', accountApi.AccountDelete.as_view(),
         name='delete_account'),
    path('api/cost/create', costApi.CostCreate.as_view(),
         name='create_cost'),
    path('cost/<int:pk>', cost.CostUpdateView.as_view(),
         name='update_cost'),
    path('api/cost/delete', costApi.CostDelete.as_view(),
         name='delete_cost'),
    path('api/transaction/getsourse',
         transactionApi.GetTransactionSource.as_view(),
         name='get_transaction_source'),
    path('api/transaction/getdest/<int:pk>',
         transactionApi.GetTransactionDestination.as_view(),
         name='get_transaction_destination'),
    path('api/transaction/create',
         transactionApi.CreateTransaction.as_view(),
         name='create_transaction'),
    path('api/convert',
         convertApi.Converter.as_view(),
         name='convert_currency'),
    path('transaction/<int:pk>',
         transaction.TransactionUpdateView.as_view(),
         name='transaction'),
    path('transaction/api/transaction/delete',
         transactionApi.DeleteTransaction.as_view(),
         name='delete_transaction'),
]
