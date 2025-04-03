import json
import logging
from datetime import timedelta, datetime
from unicodedata import category

from rest_framework.response import Response
from rest_framework.views import APIView
from .mixins import  CacheResponseMixin
from rest_framework import generics, permissions
from rest_framework import status
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from .permissions import IsOwnerOrReadOnly
from .serializers import (UserTransactionSerializer, CategorySerializer, UserTransactionSerializerClient,
                          PasswordResetRequestSerializer, PasswordResetConfirmSerializer)
#, IncomeSerializer, ExpenseSerializer)
from django.db.models import Sum
from ...models import *
from django.utils import timezone


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


class BalanceApi(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated]

    def _get_date_range(self, months_ago=0):
        today = timezone.now()
        first_day_of_current_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Last day of the previous month (the month we are in now, but minus one day)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)

        # For `months_ago` months, we need the first day of the month, `months_ago` months before
        start_date = last_day_of_previous_month.replace(day=1) - timedelta(days=30 * months_ago)

        # The end date is always the last day of the previous month
        end_date = last_day_of_previous_month

        return start_date, end_date

    def _get_balance(self, user, start_date, end_date):
        print(f"sdate: {start_date} edate: {end_date}")
        income = UserTransaction.objects.filter(user=user, transaction_type='income',
                                                date__range=[start_date, end_date]).aggregate(
            total_income=Sum('amount'))['total_income']
        expense = UserTransaction.objects.filter(user=user, transaction_type='expense',
                                                 date__range=[start_date, end_date]).aggregate(
            total_expense=Sum('amount'))['total_expense']
        return income - expense if income and expense else 0

    def get(self, request):
        user = request.user

        # Handle date range
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if start_date and end_date:
            balance = self._get_balance(user, start_date, end_date)
            all_tnx_users = UserTransaction.objects.filter(user=user,date__range=[start_date, end_date])
            all_tnx_users_json = UserTransactionSerializerClient(all_tnx_users, many=True)
            return Response({'balance': balance, 'transaction': json.dumps(all_tnx_users_json.data)}, status=status.HTTP_200_OK)

        # Handle predefined periods
        if request.GET.get('last_month'):
            start_date, end_date = self._get_date_range(1)
            balance = self._get_balance(user, start_date, end_date)
            all_tnx_users = UserTransaction.objects.filter(user=user, date__range=[start_date, end_date])
            all_tnx_users_json = UserTransactionSerializerClient(all_tnx_users, many=True)
            return Response({'balance': balance, 'transaction': json.dumps(all_tnx_users_json.data)}, status=status.HTTP_200_OK)

        if request.GET.get('last_three_months'):
            start_date, end_date = self._get_date_range(3)
            balance = self._get_balance(user, start_date, end_date)
            all_tnx_users = UserTransaction.objects.filter(user=user, date__range=[start_date, end_date])
            all_tnx_users_json = UserTransactionSerializerClient(all_tnx_users, many=True)
            return Response({'balance': balance, 'transaction': json.dumps(all_tnx_users_json.data)}, status=status.HTTP_200_OK)

        if request.GET.get('last_six_months'):
            start_date, end_date = self._get_date_range(6)
            balance = self._get_balance(user, start_date, end_date)
            all_tnx_users = UserTransaction.objects.filter(user=user, date__range=[start_date, end_date])
            all_tnx_users_json = UserTransactionSerializerClient(all_tnx_users, many=True)
            return Response({'balance': balance, 'transaction': json.dumps(all_tnx_users_json.data)}, status=status.HTTP_200_OK)

        if request.GET.get('last_year'):
            start_date, end_date = self._get_date_range(12)
            balance = self._get_balance(user, start_date, end_date)
            all_tnx_users = UserTransaction.objects.filter(user=user, date__range=[start_date, end_date])
            all_tnx_users_json = UserTransactionSerializerClient(all_tnx_users, many=True)
            return Response({'balance': balance, 'transaction': json.dumps(all_tnx_users_json.data)}, status=status.HTTP_200_OK)

        # Default to current month
        start_date = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        balance = self._get_balance(user, start_date, timezone.now())
        last_five_tnx = UserTransaction.objects.filter(user=user).order_by('-date')[:5]
        last_five_transactions = UserTransactionSerializerClient(last_five_tnx, many=True)
        return Response({'balance': balance, 'last_five_transaction' : json.dumps(last_five_transactions.data)}, status=status.HTTP_200_OK)



from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer



from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from oauth2_provider.models import AccessToken, Application
from django.contrib.auth.models import User
import datetime

class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        # Generate a unique token
        token = get_random_string(length=32)
        app = Application.objects.get(id=2)
        user = User.objects.get(email__exact=email)
        access_token = AccessToken.objects.create(
            user=user,
            token=token,
            application=app,
            expires=timezone.now() + datetime.timedelta(days=0.5),
            scope="password reset",
        )
        # Here you would save the token to the database associated with the user

        # Send the email
        send_mail(
            'Password Reset Request',
            f'Use this link to reset your password: http://localhost:3000/reset-password/{token}/',
            #  http://localhost:3000/reset/QP7mcqejh2N8cNxdEdeOEEPks2FYJTBW/
            'budgetapp@mailinator.com',
            [email],
            fail_silently=False,
        )
        return Response({'detail': 'Password reset link sent.'}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    def post(self, request, token, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data['new_password']
        token = self.kwargs.get("token")
        user = AccessToken.objects.filter(token=token)
        user_obj = User.objects.get(id=user[0].user.id)
        print(f"USER {user_obj}")
        user_obj.set_password(new_password)
        user_obj.save()
        AccessToken.objects.filter(token=token).delete()
        # Here you would retrieve the user associated with the token and update their password
        return Response({'detail': 'Password has been reset.'}, status=status.HTTP_200_OK)