from rest_framework import serializers

from budget_api.models import Category, SubCategory, UserTransaction

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'category', 'description', 'subcategories', 'category_type']


class UserTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTransaction
        fields = ['transaction_id', 'transaction_type', 'category', 'sub_category', 'amount', 'description', 'date']


class UserTransactionSerializerClient(serializers.ModelSerializer):

    class Meta:
        model = UserTransaction
        fields = ['transaction_type', 'amount', 'description', 'date']

