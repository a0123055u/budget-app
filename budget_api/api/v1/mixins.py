from django.core.cache import cache
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

class CacheResponseMixin:
    """
    Mixin to cache API responses based on request URL.
    """

    def get_cache_key(self, request):
        """
        You can customize how the cache key is generated based on request details.
        For example, you might want to use the request path, query parameters, etc.
        """
        return f"cache:{request.path}"

    def dispatch(self, request, *args, **kwargs):
        """
        Check if response is in cache before dispatching the request.
        """
        cache_key = self.get_cache_key(request)
        cached_response = cache.get(cache_key)
        print(f"Cache key: {cache_key}")
        print(f"Cached response: {cached_response}")
        if cached_response:
            return cached_response  # Return cached response

        # If not cached, proceed to generate the response
        response = super().dispatch(request, *args, **kwargs)
        print(f"Response: {response}")
        if isinstance(response, Response):
            print("CACHE SET")
            response.render()  # Render the response content
            cache.set(cache_key, response, timeout=60 * 15)

        # Cache the response after it's generated
        # cache.set(cache_key, response, timeout=60 * 1)  # Cache for 15 minutes

        return response
