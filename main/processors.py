from main.models import Income


ITEM_AMOUNT = 0


def processor(request):

    incoms = list(Income.objects.filter(delete=False,
                                        user_id=request.user.id).all())

    return {'INCOMES': incoms}
