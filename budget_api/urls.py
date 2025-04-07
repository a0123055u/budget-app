from django.urls import path, include

urlpatterns = [
    path('v1/', include('budget_api.api.v1.urls')),  # Include V1
    # path('v2/', include('budget_api.api.v2.urls')),  # Future V2 support

]
