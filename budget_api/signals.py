from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ExpensesSubCategory, IncomeSubCategory


@receiver(post_save, sender=ExpensesSubCategory)
def expense_icon_url(sender, instance, **kwargs):
    if instance.icon_expenses:
        # Construct the absolute file URL
        instance.icon_url = f"{settings.MEDIA_URL}{instance.icon_expenses.name}"
        sender.objects.filter(pk=instance.pk).update(icon_url=instance.icon_url)


# do the same for IncomeCategory
@receiver(post_save, sender=IncomeSubCategory)
def income_icon_url(sender, instance, **kwargs):
    if instance.icon_income:
        # Construct the absolute file URL
        instance.icon_url = f"{settings.MEDIA_URL}{instance.icon_income.name}"
        sender.objects.filter(pk=instance.pk).update(icon_url=instance.icon_url)
