from rest_framework import serializers

from budget_api.models import IncomeCategory, IncomeSubCategory, ExpensesSubCategory, ExpensesCategory, Income


class IncomeSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeSubCategory
        fields = '__all__'

class IncomeCategorySerializer(serializers.ModelSerializer):
    income_subcategories = IncomeSubCategorySerializer(many=True, read_only=True)
    class Meta:
        model = IncomeCategory
        fields = ['id', 'category', 'description', 'income_subcategories']

class ExpenseSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpensesSubCategory
        fields = '__all__'

class ExpensesCategorySerializer(serializers.ModelSerializer):
    expense_subcategories = ExpenseSubCategorySerializer(many=True, read_only=True)
    class Meta:
        model = ExpensesCategory
        fields = ['id', 'category', 'description', 'expense_subcategories']

class IncomeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Income
        fields = ['id', 'user', 'category', 'sub_category', 'amount', 'description', 'date']


class ExpenseSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Income
        fields = ['id', 'user', 'category', 'sub_category', 'amount', 'description', 'date']


