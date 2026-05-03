import jwt
from django.conf import settings
from django.http import JsonResponse
from functools import wraps

def authenticate_jwt(view_func):
    """Decorator to protect API routes using your existing JWT structure."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({'error': 'Access Denied. No token provided.'}, status=401)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            request.branch_id = payload['branchId']
            return view_func(request, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token Expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid Token'}, status=400)
    return wrapper