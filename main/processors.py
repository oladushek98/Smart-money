from main.models import Income, Account, Cost


ITEM_AMOUNT = 0


def processor(request):

    incoms = list(Income.objects.filter(delete=False,
                                        user_id=request.user.id).all())

    accounts = list(Account.objects.filter(delete=False,
                                           user_id=request.user.id).all())

    costs = list(Cost.objects.filter(delete=False,
                                     user_id=request.user.id).all())

    return {'INCOMES': incoms, 'ACCOUNTS': accounts, 'COSTS': costs}
