from rest_framework.response import Response
from rest_framework.views import APIView
from .mixins import  CacheResponseMixin
from rest_framework import generics, permissions
from rest_framework import status
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from .permissions import IsOwnerOrReadOnly
from .serializers import IncomeCategorySerializer, ExpensesCategorySerializer, IncomeSerializer, ExpenseSerializer
from ...models import *
# clean up the imports and remove the commented out code from the previous steps

class IncomeStaticApi(generics.ListAPIView):
    queryset = IncomeCategory.objects.prefetch_related(
        'income_subcategories').all()  # Fetch categories with subcategories
    serializer_class = IncomeCategorySerializer
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # If you need to modify the response data before returning it
        response = super().get(request, *args, **kwargs)
        # Optionally you could log or modify the response data here
        return response

class ExpenseStaticApi(generics.ListAPIView):
    queryset = ExpensesCategory.objects.prefetch_related(
        'expense_subcategories').all()  # Fetch categories with subcategories
    serializer_class = ExpensesCategorySerializer
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated]


class IncomeListCreateAPIView(generics.CreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IncomeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class ExpenseListCreateAPIView(generics.CreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]






