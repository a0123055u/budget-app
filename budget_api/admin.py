from django.contrib import admin

# Register your models here.
from budget_api.models import ExpensesCategory, IncomeCategory, ExpensesSubCategory, IncomeSubCategory

admin.site.register(ExpensesCategory)
admin.site.register(ExpensesSubCategory)
admin.site.register(IncomeCategory)
admin.site.register(IncomeSubCategory)
