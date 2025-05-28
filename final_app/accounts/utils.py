from functools import wraps
from datetime import datetime, timedelta
from django.core.cache import cache
from django.http import JsonResponse

def rate_limit(max_requests=5, window_seconds=60):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            identifier = request.user.id if request.user.is_authenticated else request.META.get("REMOTE_ADDR")
            cache_key = f"rl:{identifier}"
            data = cache.get(cache_key, {"count": 0, "start_time": datetime.now()})

            now = datetime.now()
            elapsed = (now - data["start_time"]).total_seconds()

            print(f"[RateLimiter] {identifier} | Count: {data['count']} | Elapsed: {elapsed:.2f}s")

            if elapsed < window_seconds:
                if data["count"] >= max_requests:
                    print(f"[RateLimiter] BLOCKED - Too many requests from {identifier}")
                    return JsonResponse(
                        {"detail": "Rate limit exceeded. Try again later."},
                        status=429
                    )
                else:
                    data["count"] += 1
            else:
                data = {"count": 1, "start_time": now}

            cache.set(cache_key, data, timeout=window_seconds)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
