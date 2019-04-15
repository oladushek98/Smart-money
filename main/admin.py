from django.contrib import admin
from main.models import FinancialNode, Income, Account, Cost, Goal, Transaction, UserAdditionalInfo


admin.site.register(FinancialNode)
admin.site.register(Income)
admin.site.register(Account)
admin.site.register(Cost)
admin.site.register(Goal)
admin.site.register(Transaction)
admin.site.register(UserAdditionalInfo)