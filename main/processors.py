from django.db.models import Sum, Q

from main.forms import IncomeForm, TransactionCreateForm, AccountForm, CostForm
from main.models import Income, Transaction, Account, Cost

ITEM_AMOUNT = 0


def processor(request):
    incoms = list(Income.objects.filter(delete=False,
                                        user_id=request.user.id).all())
    for incom in incoms:
        incom.amount = sum(
            map(lambda x: x.amount, incom.source.filter(delete=False).all()))

    income_create_from = IncomeForm()
    account_create_form = AccountForm()
    cost_create_form = CostForm()
    add_transaction = TransactionCreateForm()

    accounts = list(Account.objects.filter(delete=False,
                                           user_id=request.user.id).all())

    for account in accounts:
        amount_plus = sum(map(lambda x: x.amount,
                              account.destination.filter(delete=False).all()))
        amount_minus = sum(
            map(lambda x: x.amount, account.source.filter(delete=False).all()))

        account.amount += amount_plus - amount_minus

    costs = list(Cost.objects.filter(delete=False,
                                     user_id=request.user.id).all())

    for cost in costs:
        amount_plus = sum(map(lambda x: x.amount,
                              cost.destination.filter(delete=False).all()))

        cost.amount = amount_plus if amount_plus is not None else 0

    transactions = list(
        Transaction.objects.filter(delete=False,
                                   user_id=request.user.id).all()[:9])
    for transaction in transactions:
        transaction.data_from = transaction.data_from.__str__()

    return {'INCOMES': incoms,
            'ACCOUNTS': accounts,
            'COSTS': costs,
            'TRANSACTIONS': transactions,
            'INCOME_CREATE_FORM': income_create_from,
            'ADD_TRANSACTION_FORM': add_transaction,
            'ACCOUNT_CREATE_FORM': account_create_form,
            'COST_CREATE_FORM': cost_create_form,
            'button_color': 'red lighten-2'}
