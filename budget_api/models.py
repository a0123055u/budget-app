from sqlite3.dbapi2 import Timestamp

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
# Create your models her

from django.db import models

class TimeStampedModel(models.Model):
    """Abstract base class that adds created_at and updated_at fields to models."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Category(TimeStampedModel):
    CATEGORY_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category_type = models.CharField(max_length=255, choices=CATEGORY_TYPES)
    class Meta:
        db_table = 'categories'
    def __str__(self):
        return self.category


class SubCategory(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, related_name="subcategories", on_delete=models.CASCADE)
    icon = models.ImageField(upload_to='icons/', default='default_icon.png')
    sub_category = models.CharField(max_length=255)
    class Meta:
        db_table = 'sub_categories'
    def __str__(self):
        return f"{self.category} - {self.sub_category}"


class UserTransaction(TimeStampedModel):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    transaction_id = models.CharField(max_length=20, unique=True, editable=False)
    transaction_type = models.CharField(max_length=255, choices=TRANSACTION_TYPES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateTimeField()
    class Meta:
        db_table = 'UserTransaction'

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            today = now().strftime('%Y%m%d')  # Get current date in YYYYMMDD format
            last_transaction = UserTransaction.objects.filter(transaction_id__startswith=f'TXN-{today}').order_by(
                '-id').first()

            # Extract the last number and increment it
            new_number = int(last_transaction.transaction_id[-4:]) + 1 if last_transaction else 1

            # Format: TXN-YYYYMMDD-XXXX
            self.transaction_id = f'TXN-{today}-{new_number:04d}'

        super().save(*args, **kwargs)

