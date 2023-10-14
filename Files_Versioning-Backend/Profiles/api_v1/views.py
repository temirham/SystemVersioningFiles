from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import auth
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, requires_csrf_token
from Site.general import require_csrf_cookie
from django.utils.decorators import method_decorator
from Site.exceptions import BadRequestError, StorageServerError, raise_params_error
from timeout_decorator import timeout, TimeoutError
from Site.settings import STORAGE_WAIT_TIMEOUT
from django.contrib.auth.models import User
# from .serializers import UserSerializer
from GRPC.protos import minio_pb2
from GRPC.client import stub
from Site.general import get_user_bucket


# Рассмотреть другие варианты для названий и огранизации файлов в minio


USER_ALREADY_EXISTS_MSG = 'User with that login already exists.'
PASSWORDS_DONT_MATCH_MSG = 'Password fields dont match.'
USER_SUCCESSFULLY_ADDED_MSG = 'User was successfully added.'
USER_SUCCESSFULLY_DELETED_MSG = 'User was successfully deleted.'


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    def get(self, request: Request):
        return Response({'success': 'CSRF cookie set.'})


# @method_decorator(require_csrf_cookie, name='post')
class AddUser(APIView):
    def post(self, request: Request):
        # Checking if all fields specified:
        raise_params_error(request, ["username", "password", "re_password"])

        username: str = request.data['username']
        password = request.data['password']

        # Checking if password fields match:
        if password != request.data['re_password']:
            raise BadRequestError({'error': PASSWORDS_DONT_MATCH_MSG})

        # Checking if user is new:
        if User.objects.filter(username=request.data['username']).exists():
            raise BadRequestError({'error': USER_ALREADY_EXISTS_MSG})

        grpc_user = minio_pb2.User(user=get_user_bucket(username))

        # Checking if bucket hash name unique (queries with hash cant cause value errors):
        try:
            status = stub.CheckUser(grpc_user)
        except TimeoutError:
            raise StorageServerError
        if not status.status:
            raise StorageServerError
        if status.response:
            raise BadRequestError({'error': USER_ALREADY_EXISTS_MSG})

        # Adding user:
        status = stub.AddUser(grpc_user)
        if not status.status:
            raise StorageServerError
        user = User(username=username)
        user.set_password(password)  # Should use this method to authomatic hashing work!
        user.save()
        return Response({'success': USER_SUCCESSFULLY_ADDED_MSG})


# @method_decorator(requires_csrf_token, name='dispatch')
class DeleteUser(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request: Request):
        user = User.objects.get(username=request.user.username)
        status = stub.DeleteUser(
            minio_pb2.User(user=get_user_bucket(user.username))
        )

        if not status.status:
            raise StorageServerError
        user.delete()
        return Response({'success': USER_SUCCESSFULLY_DELETED_MSG})


# class Logout(APIView):
#     authentication_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#
#     def post(self, request):
#         token = RefreshToken(request.data.get('refresh'))
#         token.blacklist()
#         return Response({'success': 'Successfully logged out.'})


# # Not used:
# class GetUserInfo(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#
#     def get(self, request: Request):
#         return Response({'data': UserSerializer(request.user).data})
#
#

