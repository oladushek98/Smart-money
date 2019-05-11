from django.db.models import Sum, Q

from main.forms import IncomeForm, TransactionCreateForm, AccountForm, CostForm
from main.models import Income, Transaction, Account, Cost
from main.utils import convert_currency

ITEM_AMOUNT = 0


def processor(request):

    return {'button_color': 'red lighten-2'}
