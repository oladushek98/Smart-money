from django.db import models


ICON_LENGTH = 10
NAME_LENGTH = 30
CURRENCY_LENGTH = 3


class FinancialNode(models.Model):

    def __str__(self):
        return f'\'{self.name}\''

    icon = models.CharField(max_length=ICON_LENGTH, null=True, blank=True)
    name = models.CharField(max_length=NAME_LENGTH)
    currency = models.CharField(max_length=CURRENCY_LENGTH, null=True,
                                blank=True, verbose_name='валюта')
    delete = models.BooleanField(default=False)


# доходы
class Income(FinancialNode):
    def __str__(self):
        return f'Доходы : {super()}'

    monthly_plan = models.IntegerField(null=True, blank=True)


# счета
class Account(FinancialNode):
    def __str__(self):
        return f'Счет {"долговой" if self.is_debt_account else ""} : ' \
            f'{super()}'

    amount = models.IntegerField(null=True, blank=True)
    is_debt_account = models.BooleanField()
    take_into_balance = models.BooleanField()


# расходы
class Cost(FinancialNode):
    def __str__(self):
        return f'Расходы : {super()}'

    monthly_plan = models.IntegerField(null=True, blank=True)


# цель
class Goal(FinancialNode):
    def __str__(self):
        return f'Цели : {super()}'

    plan = models.IntegerField(null=True, blank=True)


# транзакция
class Transaction(models.Model):
    def __str__(self):
        return f'Из {self.transaction_from} в ' \
            f'{self.transaction_to} дата : {self.data_from}'

    transaction_from = models.ForeignKey(FinancialNode,
                                         related_name='source',
                                         on_delete=models.CASCADE)
    transaction_to = models.ForeignKey(FinancialNode,
                                       related_name='destination',
                                       on_delete=models.CASCADE)
    amount = models.IntegerField()
    data_from = models.DateField()
    data_to = models.DateField(null=True, blank=True)
    comment = models.CharField(max_length=100, default='')
