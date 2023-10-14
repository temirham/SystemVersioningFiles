import traceback
from sys import exc_info
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException, ParseError, UnsupportedMediaType, \
    MethodNotAllowed, PermissionDenied, NotAuthenticated, AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken
from django.utils.encoding import force_str
from rest_framework.request import Request
from django.http import JsonResponse


ERROR_KEY = 'error'
REQUIRED_PARAM_MSG = 'This field is required.'


# For required params checking:
def check_request_params(request: Request, params: list[str],
                         segment: str = '') -> [bool, list[str]]:
    missed_params = []
    for param in params:
        if not segment:
            try:
                if not request.data[param]:
                    missed_params.append(param)
            except KeyError:
                missed_params.append(param)
        else:
            try:
                if not getattr(request, segment).get(param):
                    missed_params.append(param)
            except AttributeError:
                missed_params.append(param)
    return [len(missed_params) == 0, missed_params]


def raise_params_error(request: Request, params: list[str], segment: str = ''):
    str = REQUIRED_PARAM_MSG
    if segment:
        str = str[:-1] + ' in ' + segment + ' segment.'
    check = check_request_params(request, params, segment)
    if not check[0]:
        raise BadRequestError(
            {ERROR_KEY: {key: str for key in check[1]}}
        )


# Reformation to my format possible errors:
def django_not_found_handler(request, exception):
    return JsonResponse({'error': 'Wrong path was specified.'}, status=404)


def django_internal_error_handler(request, exception):
    return JsonResponse({'error': 'Server internal error.'}, status=500)


def drf_exceptions_handler(exc, context):
    _type = type(exc)
    if _type is ParseError or _type is UnsupportedMediaType:
        exc = BadRequestError()
        _type = type(exc)
    if _type is MethodNotAllowed:
        exc = InvalidMethodError
    elif _type is NotAuthenticated:
        exc = AuthenticatedError()
    elif (_type is InvalidToken) or (_type is AuthenticationFailed):
        exc = InvalidTokenError()
    elif _type is PermissionDenied:
        exc = ForbiddenError()
    elif (_type is not BadRequestError) and (_type is not StorageServerError):
        traceback.print_exception(_type, exc, exc.__traceback__)
        exc = InternalError()
    return exception_handler(exc, context)


class InvalidMethodError(MethodNotAllowed):
    def __init__(self, method, detail=None, code=None):
        super().__init__(method, detail, code)
        if detail is None:
            detail = {ERROR_KEY: force_str(self.default_detail).format(method=method)}


class AuthenticatedError(AuthenticationFailed):
    default_detail = {ERROR_KEY: 'Not authenticated.'}


class InvalidTokenError(AuthenticationFailed):
    default_detail = {ERROR_KEY: 'Given token is invalid or expired.'}


class ForbiddenError(PermissionDenied):
    default_detail = {ERROR_KEY: 'Resource is forbidden for you.'}


class InternalError(APIException):
    default_detail = {ERROR_KEY: 'Internal server error occupied.'}


# Raised requests:
class StorageServerError(APIException):
    status_code = 500
    default_detail = {ERROR_KEY: 'A problem has occurred on the storage server'}


class BadRequestError(APIException):
    status_code = 400
    default_detail = {ERROR_KEY: 'The request could not be understood by the '
                                 'server due to malformed syntax or incorrect content.'}


# # Not used:
# class CustomApiError(APIException):
#     def __init__(self, status_code: int = None,
#                  default_code: str = None,
#                  detail: str = None):
#         super().__init__()
#         if status_code:  self.status_code = status_code
#         if default_code:
#             self.default_code = default_code
#             print(default_code)
#
#         if detail:       self.detail = detail