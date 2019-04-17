from django.db.models import Sum, Q

from main.forms import IncomeForm
from main.models import Income, Transaction

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

    return {'INCOMES': incoms,
            'INCOME_CREATE_FORM': income_create_from}
