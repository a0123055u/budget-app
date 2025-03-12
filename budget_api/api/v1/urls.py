from django.urls import path

from .login.interospect import introspect_token
from .views import CategoryApi, UserTransactionListCreateAPIView, UserTransactionUpdateDestroyAPIView, BalanceApi, \
    RegisterView

urlpatterns = [
    path('income/expense/category/', CategoryApi.as_view()),
    path('transaction/user/', UserTransactionListCreateAPIView.as_view()),
    path('transaction/user/<str:transaction_id>', UserTransactionUpdateDestroyAPIView.as_view()),
    path('introspect/', introspect_token),
    path('balance/', BalanceApi.as_view()),
    path('register/user/', RegisterView.as_view())
]
