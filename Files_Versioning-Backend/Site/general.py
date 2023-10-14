from django.middleware.csrf import get_token, CsrfViewMiddleware
from rest_framework.authentication import CSRFCheck

from Site.exceptions import ForbiddenError
from rest_framework.exceptions import PermissionDenied
from hashlib import sha256
from rest_framework.response import Response

from rest_framework.views import APIView

def require_csrf_cookie(view_func):
    def wrapped_view(request, *args, **kwargs):
        # csrf_cookie = request.COOKIES.get('csrftoken', '')
        # print(csrf_cookie)
        # # print(CsrfViewMiddleware()._get_token(request))
        # r = CSRFCheck()
        # # get_response()
        # r.process_request(request)
        # reason = CsrfViewMiddleware().process_view(request, None, (), {})
        # if reason is not None:
        #     print()
        # if csrf_cookie != get_token(request):
        #     print('1')
        #     h = APIView()
        #     h.handle_exception(PermissionDenied)
        return view_func(request, *args, **kwargs)
    return wrapped_view


def get_user_bucket(username: str) -> str:
    return sha256(username.encode('utf-8')).hexdigest()[:32]
