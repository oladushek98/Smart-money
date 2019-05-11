from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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
    user = models.ForeignKey(User,
                             related_name='financial_nodes',
                             on_delete=models.CASCADE,
                             default=0)
    create_on = models.DateField(default=timezone.now().date())


# доходы
class Income(FinancialNode):
    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'Доходы : {super().__str__()}'

    monthly_plan = models.IntegerField(null=True, blank=True)


# счета
class Account(FinancialNode):
    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'Счет {"долговой" if self.is_debt_account else ""} : ' \
            f'{super().__str__()}'

    amount = models.IntegerField(null=True, blank=True)
    is_debt_account = models.BooleanField()
    take_into_balance = models.BooleanField()


# расходы
class Cost(FinancialNode):
    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'Расходы : {super().__str__()}'

    monthly_plan = models.IntegerField(null=True, blank=True)


# цель
class Goal(FinancialNode):
    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'Цели : {super().__str__()}'

    plan = models.IntegerField(null=True, blank=True)


# транзакция
class Transaction(models.Model):
    class Meta:
        ordering = ['-data_from']

    @property
    def dict(self):
        return {
            'transaction_from': self.transaction_from,
            'transaction_to': self.transaction_to,
            'amount': self.amount,
            'choice_currency': self.choice_currency,
            'data_from': self.data_from,
        }

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
    delete = models.BooleanField(default=False)
    user = models.ForeignKey(User,
                             related_name='transaction',
                             on_delete=models.CASCADE,
                             null=True)
    choice_currency = models.CharField(max_length=3, default='BYN')


class UserAdditionalInfo(models.Model):

    currency = models.CharField(max_length=3, default='BYN')
    bank_login = models.CharField(max_length=50, null=True)
    bank_password = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(User,
                             related_name='additonal',
                             on_delete=models.CASCADE)

