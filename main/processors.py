from django.db.models import Sum, Q

from main.forms import IncomeForm, TransactionForm, AccountForm, CostForm
from main.models import Income, Transaction, Account, Cost

ITEM_AMOUNT = 0


def processor(request):
    incoms = list(Income.objects.filter(delete=False,
                                        user_id=request.user.id).all())
    for incom in incoms:
        incom.amount = Income.objects.annotate(
            sum_amount=Sum('source__amount',
                           filter=(
                               Q(source__transaction_from=incom)
                           ))).first().sum_amount
        if incom.amount is None:
            incom.amount = 0

    income_create_from = IncomeForm()
    account_create_form = AccountForm()
    cost_create_form = CostForm()
    add_transaction = TransactionForm()

    accounts = list(Account.objects.filter(delete=False,
                                           user_id=request.user.id).all())

    costs = list(Cost.objects.filter(delete=False,
                                     user_id=request.user.id).all())

    return {'INCOMES': incoms,
            'ACCOUNTS': accounts,
            'COSTS': costs,
            'INCOME_CREATE_FORM': income_create_from,
            'ADD_TRANSACTION_FORM': add_transaction,
            'ACCOUNT_CREATE_FORM': account_create_form,
            'COST_CREATE_FORM': cost_create_form}
