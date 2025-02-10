from django.contrib import admin

# Register your models here.
from budget_api.models import *

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(UserTransaction)
