from django.contrib import admin

# Register your models here.
from budget_api.models import *

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(UserTransaction)

class UserAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs =  super().get_queryset(request).distinct()
        print(qs)  # Debug what is being returned
        return qs
