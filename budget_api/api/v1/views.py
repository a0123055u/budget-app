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
# clean up the imports and remove the commented out code from the previous steps

class CategoryApi(generics.ListAPIView):
    queryset = Category.objects.prefetch_related(
        'subcategories').all()  # Fetch categories with subcategories
    serializer_class = CategorySerializer
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # If you need to modify the response data before returning it
        response = super().get(request, *args, **kwargs)
        # Optionally you could log or modify the response data here
        return response

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






