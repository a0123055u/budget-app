from django.contrib.auth.models import User
from django.db import models

# Create your models her



class ExpensesCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'expense_categories'
    def __str__(self):
        return self.category

class ExpensesSubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(ExpensesCategory, related_name="expense_subcategories",on_delete=models.CASCADE)
    icon_expenses = models.ImageField(upload_to='icons/', default='default_icon.png')
    icon_url = models.CharField(max_length=255, default="")
    sub_category = models.CharField(max_length=255)
    class Meta:
        db_table = 'expenses_sub_categories'
    def __str__(self):
        return f"{self.category} - {self.sub_category}"


class Expense(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpensesCategory, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(ExpensesSubCategory, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField()
    class Meta:
        db_table = 'expenses'


class IncomeCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'income_categories'
    def __str__(self):
        return self.category


class IncomeSubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(IncomeCategory, related_name="income_subcategories" ,on_delete=models.CASCADE)
    icon_income = models.ImageField(upload_to='icons/', default='default_icon.png')
    icon_url = models.CharField(max_length=255, default="")
    sub_category = models.CharField(max_length=255)
    class Meta:
        db_table = 'income_sub_categories'
    def __str__(self):
        return f"{self.category} - {self.sub_category}"

class Income(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE, null=True, blank=True)
    sub_category = models.ForeignKey(IncomeSubCategory, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    class Meta:
        db_table = 'income'
