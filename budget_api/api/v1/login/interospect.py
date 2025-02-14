from django.http import JsonResponse
from oauth2_provider.models import AccessToken
from oauth2_provider.models import Application
from oauth2_provider.settings import oauth2_settings
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
import logging
import jwt

from budgetcore.settings import SECRET_KEY

logger = logging.getLogger(__name__)

@csrf_exempt
def introspect_token(request):
    """
    Custom introspection endpoint for validating the access token.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    token = request.POST.get('token', None)
    if not token:
        return JsonResponse({"error": "Missing token parameter"}, status=400)

    try:
        # Retrieve the AccessToken model for the provided token
        access_token = AccessToken.objects.get(token=token)

        # Check if the token has expired
        if access_token.expires > timezone.now():
            user_id = access_token.user.id
            encoded_user_id = jwt.encode({'user_id': user_id}, SECRET_KEY, algorithm='HS256')
            # Return introspection details
            data = {
                "active": True,
                "scope": access_token.scope,
                # "client_id": access_token.application.client_id,
                "user_id": encoded_user_id,
                "exp": access_token.expires.timestamp(),  # Expiry timestamp
                "iat": access_token.created.timestamp(),  # Issued at timestamp
            }
            return JsonResponse(data)

        else:
            return JsonResponse({"active": False}, status=200)

    except AccessToken.DoesNotExist:
        # Token not found
        return JsonResponse({"error": "Invalid token"}, status=400)