import os
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from two_factor.urls import urlpatterns as tf_urls
from two_factor.views import LoginView
from two_factor.admin import AdminSiteOTPRequired
## for OTP enforce
admin.site.__class__ = AdminSiteOTPRequired


urlpatterns = [
    ## for OTP enforce
    path('', include(tf_urls)),
    # Two-factor URLs before admin
    path('admin/', admin.site.urls),
    # Other URLs (API, OAuth, etc.)
    path('budget/api/', include('budget_api.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]


if settings.DEBUG:
    urlpatterns += static('/icons/', document_root=os.path.join(settings.BASE_DIR, 'icons'))
