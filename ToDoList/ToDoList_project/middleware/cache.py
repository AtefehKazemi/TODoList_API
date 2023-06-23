from django.core.cache import cache

class CacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is cacheable (GET requests only)
        if request.method == 'GET':
            # cache key Generating
            cache_key = f"response:{request.get_full_path()}"
            # Getting the key's value
            cached_response = cache.get(cache_key)
            # Check if the response is cached or not
            if cached_response is None:
                print("****************no cache********************")
                # Call the view to generate the response
                response = self.get_response(request)
                # Cache the response for 5 minutes
                cache.set(cache_key, response, 300)
                return response
            print("****************from cache********************")
            # Else return cached_response
            return cached_response

        # Non-cacheable request, pass through to next middleware
        return self.get_response(request)