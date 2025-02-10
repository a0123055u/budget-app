from django.urls import path
from .views import CategoryApi, UserTransactionListCreateAPIView, UserTransactionUpdateDestroyAPIView

urlpatterns = [
    path('income/expense/category/', CategoryApi.as_view()),
    path('transaction/user/', UserTransactionListCreateAPIView.as_view()),
    path('transaction/user/<str:transaction_id>', UserTransactionUpdateDestroyAPIView.as_view()),
]
