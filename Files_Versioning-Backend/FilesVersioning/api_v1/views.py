from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from Site.exceptions import BadRequestError, StorageServerError, \
                               raise_params_error, REQUIRED_PARAM_MSG
from GRPC.protos import minio_pb2
from GRPC.client import stub
from io import BytesIO
from Site.general import get_user_bucket


FORM_FILE_FILD_REQUIRED = {'file': 'This field is required in form data.'}
FILENAME_TOO_LONG       = 'Too long file name. Needed less then non-unicode: 250, unicode: 80.',
FILENAME_WRONG_CHARS    = 'Incorrect file name characters. The "_" and multiple "/" are prohibited.'


FILES_STORAGE_MESSAGES = {
    24002: FILENAME_TOO_LONG,
    24003: FILENAME_WRONG_CHARS,
}


# @method_decorator(csrf_protect, name='dispatch')
class GetFileVersionsInfo(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request: Request):
        files_list = []
        versions_info = stub.GetFilesInfoList(
            minio_pb2.User(user=get_user_bucket(request.user.username))
        )
        for version in versions_info:
            if not version.status.status:
                raise StorageServerError
            matching_file = next((file for file in files_list
                                  if file['name'] == version.name), None)
            if matching_file:
                matching_file['versions'][version.version] = version.date
            elif version.name:
                files_list.append({'name': version.name,
                                   'versions': {version.version: version.date}})
        return Response({'data': files_list})


# @method_decorator(csrf_protect, name='dispatch')
class AddFileVersion(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request: Request):
        # Checking if all fields specified:
        # raise_params_error(request, ['file'], type='FILES')
        file = request.FILES.get('file')  # To put attention on form data using
        if not file:
            raise BadRequestError({'error': FORM_FILE_FILD_REQUIRED})

        user_bucket = get_user_bucket(request.user.username)

        # Getting last file version:
        last_version = 0
        versions_info = stub.GetFilesInfoList(minio_pb2.User(user=user_bucket))
        for version in versions_info:  # Minimum one object guaranteed
            if not version.status.status:
                raise StorageServerError
            if version.name == file.name:
                last_version = max(last_version, int(version.version))

        # Adding new version:
        status = stub.AddFileVersion(
            minio_pb2.FileAddRequest(user=user_bucket,
                                     name=file.name,
                                     version=str(last_version + 1),
                                     data=file.read())
        )
        print(status.status_code)
        if status.status:
            return Response({'success': 'File version successfully added.'})
        else:
            try:
                raise BadRequestError({'error': FILES_STORAGE_MESSAGES[status.status_code]})
            except KeyError:
                raise StorageServerError


# @method_decorator(csrf_protect, name='dispatch')
class DeleteFileVersion(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request: Request):
        # Checking all fields specified:
        raise_params_error(request, ['name', 'version'])

        status = stub.DeleteFileVersion(
            minio_pb2.FileRequest(user=get_user_bucket(request.user.username),
                                  name=request.data['name'],
                                  version=str(request.data['version']))
        )
        if status.status:
            return Response({'success': 'File version successfully deleted.'})
        else:
            try:
                raise BadRequestError({'error': FILES_STORAGE_MESSAGES[status.status_code]})
            except KeyError:
                raise StorageServerError


# @method_decorator(csrf_protect, name='dispatch')
class DownloadFileVersion(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request: Request):
        # Checking all fields specified:
        raise_params_error(request, ['name', 'version'])
        name = request.data['name']
        version = request.data['version']

        file = stub.DownloadFileVersion(
            minio_pb2.FileRequest(user=get_user_bucket(request.user.username),
                                  name=name,
                                  version=str(version))
        )
        if file.status.status:
            filename = name.split('.')[-2] + f'({version})' + name.split('.')[-1]
            return FileResponse(BytesIO(file.data), filename=filename, as_attachment=True)
        else:
            try:
                raise BadRequestError({'error': FILES_STORAGE_MESSAGES[file.status.status_code]})
            except KeyError:
                raise StorageServerError


# @method_decorator(csrf_protect, name='dispatch')
class DeleteFile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request: Request):
        # Checking all fields specified:
        raise_params_error(request, ['name'])

        status = stub.DeleteFile(
            minio_pb2.FileRequest(user=get_user_bucket(request.user.username),
                                  name=request.data['name'])
        )
        if status.status:
            return Response({'success': 'File successfully deleted.'})
        else:
            try:
                raise BadRequestError({'error': FILES_STORAGE_MESSAGES[status.status_code]})
            except KeyError:
                raise StorageServerError

# try:
# file = File.objects.get(file_id=file_id)
# filename = Soft.objects.get(soft_id=file.soft_id.soft_id).name.replace(' ', '_')
# filename += '_' + file.platform_id.name + '_' + file.architecture + \
#             '.' + file.path.name.split('.')[1]
# return FileResponse(open(VERSION_STORAGE / file.path.name, 'rb'), filename=filename, as_attachment=True)/

