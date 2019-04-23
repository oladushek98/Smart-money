from django.db.models import Sum, Q

from main.forms import IncomeForm, TransactionForm, AccountForm, CostForm
from main.models import Income, Transaction, Account, Cost

ITEM_AMOUNT = 0


def processor(request):
    incoms = list(Income.objects.filter(delete=False,
                                        user_id=request.user.id).all())
    for incom in incoms:
        incom.amount = sum(map(lambda x: x.amount, incom.source.all()))

    income_create_from = IncomeForm()
    account_create_form = AccountForm()
    cost_create_form = CostForm()
    add_transaction = TransactionForm()

    accounts = list(Account.objects.filter(delete=False,
                                           user_id=request.user.id).all())

    for account in accounts:
        amount_plus = sum(map(lambda x: x.amount, account.destination.all()))
        amount_minus = sum(map(lambda x: x.amount, account.source.all()))

        account.amount += amount_plus - amount_minus

    costs = list(Cost.objects.filter(delete=False,
                                     user_id=request.user.id).all())

    for cost in costs:
        amount_plus = sum(map(lambda x: x.amount, cost.destination.all()))

        cost.amount = amount_plus if amount_plus is not None else 0

    transactions = list(
        Transaction.objects.filter(delete=False,
                                   user_id=request.user.id).all())

    return {'INCOMES': incoms,
            'ACCOUNTS': accounts,
            'COSTS': costs,
            'TRANSACTIONS': transactions[:9],
            'INCOME_CREATE_FORM': income_create_from,
            'ADD_TRANSACTION_FORM': add_transaction,
            'ACCOUNT_CREATE_FORM': account_create_form,
            'COST_CREATE_FORM': cost_create_form,
            'button_color': 'red lighten-2'}
