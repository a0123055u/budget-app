from django.urls import path
from .views import IncomeStaticApi, ExpenseStaticApi, IncomeListCreateAPIView, IncomeRetrieveUpdateDestroyAPIView, \
    ExpenseListCreateAPIView

urlpatterns = [
    path('income/', IncomeListCreateAPIView.as_view()),
    path('income/<int:pk>/', IncomeRetrieveUpdateDestroyAPIView.as_view()),
    path('income/category/', IncomeStaticApi.as_view()),
    path('expense/', ExpenseListCreateAPIView.as_view()),
    path('expense/<int:pk>/', ExpenseListCreateAPIView.as_view()),
    path('expense/category/', ExpenseStaticApi.as_view()),
]
