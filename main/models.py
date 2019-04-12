from django.db import models


ICON_LENGTH = 10
NAME_LENGTH = 30
CURRENCY_LENGTH = 3


class FinancialNode(models.Model):
    icon = models.CharField(max_length=ICON_LENGTH, null=True, blank=True)
    name = models.CharField(max_length=NAME_LENGTH)
    currency = models.CharField(max_length=CURRENCY_LENGTH, null=True,
                                blank=True, verbose_name='валюта')
    delete = models.BooleanField(default=False)


# доходы
class Income(FinancialNode):
    monthly_plan = models.IntegerField(null=True, blank=True)


# счета
class Account(FinancialNode):
    amount = models.IntegerField(null=True, blank=True)
    is_debt_account = models.BooleanField()
    take_into_balance = models.BooleanField()


# расходы
class Cost(FinancialNode):
    monthly_plan = models.IntegerField(null=True, blank=True)


# цель
class Goal(FinancialNode):
    plan = models.IntegerField(null=True, blank=True)


# транзакция
class Transaction(models.Model):
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
