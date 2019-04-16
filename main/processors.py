from main.models import Income
from main.models import Account


ITEM_AMOUNT = 0


def processor(request):

    incoms = list(Income.objects.filter(delete=False,
                                        user_id=request.user.id).all())

    accounts = list(Account.objects.filter(delete=False,
                                           user_id=request.user.id).all())

    return {'INCOMES': incoms, 'ACCOUNTS': accounts}
