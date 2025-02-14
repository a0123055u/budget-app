import logging
from unicodedata import category

from rest_framework.response import Response
from rest_framework.views import APIView
from .mixins import  CacheResponseMixin
from rest_framework import generics, permissions
from rest_framework import status
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from .permissions import IsOwnerOrReadOnly
from .serializers import (UserTransactionSerializer, CategorySerializer)
#, IncomeSerializer, ExpenseSerializer)
from ...models import *
log = logging.getLogger(__name__)

# clean up the imports and remove the commented out code from the previous steps

class CategoryApi(generics.ListAPIView):
    queryset = Category.objects.prefetch_related(
        'subcategories').all()  # Fetch categories with subcategories
    serializer_class = CategorySerializer
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        queryset = Category.objects.prefetch_related('subcategories').all()
        category_type = self.request.query_params.get('category_type', None)
        if category_type:
            queryset = queryset.filter(category_type=str(category_type).lower())
        return queryset

class UserTransactionListCreateAPIView(generics.CreateAPIView):
    queryset = UserTransaction.objects.all()
    serializer_class = UserTransactionSerializer
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserTransactionUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserTransaction.objects.all()
    serializer_class = UserTransactionSerializer
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    lookup_field = 'transaction_id'






