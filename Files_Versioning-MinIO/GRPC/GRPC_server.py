from grpc import server, RpcError, ssl_server_credentials, StatusCode
# Import should be absolute to allow importing from current __file__.
# Also, minio_pb2_grpc have minio_pb2 import inside,
# it should be changed to absolute after generation from .proto.
from GRPC.protos import minio_pb2, minio_pb2_grpc
from MinIO.s3_methods import MinioClass, HandableS3Errors, \
    HandableValueErrors
from concurrent.futures import ThreadPoolExecutor
from typing import TypedDict
from enum import Enum
from logging import Logger, getLogger, Formatter, StreamHandler, DEBUG
from sys import stdout


class GrpcConf(TypedDict):
    endpoint: str
    workers: int
    secure: bool
    crt_path: str
    key_path: str


class MinioConf(TypedDict):
    endpoint: str
    access_key: str
    secret_key: str
    secure: bool
    timeout: int


class HandableServicerErrors(Enum):
    object_characters_incorrect = 1
    request_params_not_specified = 2  # Not used but should be updated later


# Status codes errors mapping:  # Put in s3 methods in future
_S3_e = HandableS3Errors
_V_e  = HandableValueErrors
_HS_E = HandableServicerErrors
ERROR_CODES = {
    _S3_e.bucket_not_found.value:                   14040,  # First:
    _S3_e.bucket_already_exists.value:              14090,  #    1-bucket, 2-object
    _S3_e.object_not_found.value:                   24040,  # Next 3:
    _S3_e.                                                  #    Http code
    object_name_too_long_or_prohibited_chars.value: 24002,  # Last:
    _V_e.bucket_characters_incorrect.value:         14003,  #    1-short, 2-long
    _V_e.bucket_name_too_small.value:               14001,  #    3-incorr chars
    _V_e.bucket_name_too_long.value:                14002,  #
    _HS_E.object_characters_incorrect.value:        24003   # < - that one is used to hold prohibited chars
                                                      # from object_name_too_long_or_prohibited_chars.
                                                      # Minio uses / sep for folders, me using _ for version splitting.
                                                      # So that can be changed after using folders for versions store.
}


# To update _process_errors function as my lib
class MinioGRPCServicer(minio_pb2_grpc.MinioMethodsServicer):
    GRPCerr_msg = 'GRPC error: '
    not_active_msg = 'Servicer is inactive.'
    err_msg = 'Unexpected error: '
    name_version_sep = '_'

    # Add more info in exceptions and realise
    # Add putting logs from both to one file
    # Add switching function

    def __init__(self, grpc_conf: GrpcConf, minio_conf: MinioConf,
                 grpc_logger: Logger = None, minio_logger: Logger = None):
        try:
            _str = ' not '
            self.active = False
            default = getLogger('GRPC minio servicer')
            default.setLevel(DEBUG)
            cons = StreamHandler(stream=stdout)
            cons.setFormatter(
                Formatter('%(asctime)s - %(name)s'
                          ' - %(levelname)s - %(message)s'))
            default.addHandler(cons)
            self.logger = grpc_logger if grpc_logger else default
            self.logger.info('GRPC minio servicer starting.')

            self.endpoint = grpc_conf['endpoint']
            self.workers = grpc_conf['workers']
            self.secure = grpc_conf['secure']
            self.crt_path = grpc_conf['crt_path']
            self.key_path = grpc_conf['key_path']
            self.minio = MinioClass(minio_conf['endpoint'],
                                    minio_conf['access_key'],
                                    minio_conf['secret_key'],
                                    minio_conf['secure'],
                                    minio_conf['timeout'],
                                    minio_logger)
            if not self.minio.inited_success:
                raise ConnectionError
            if not self.secure:
                self.grpc_server = server(
                    ThreadPoolExecutor(max_workers=self.workers)
                )
                minio_pb2_grpc.add_MinioMethodsServicer_to_server(
                    self, self.grpc_server)
                self.grpc_server.add_insecure_port(self.endpoint)
            else:
                server_credentials = ssl_server_credentials(
                    [
                        (open(self.crt_path, 'rb').read(),
                         open(self.key_path, 'rb').read())
                    ]
                )
                server.add_secure_port(self.endpoint, server_credentials)
            self.grpc_server.start()
            _str = ' '
        except RpcError as e:
            self.logger.error(self.GRPCerr_msg, e)
        except ConnectionError:
            self.logger.error(f'Minio client inactive.')
        except Exception as e:
            self.logger.error(self.err_msg, e)
        else:
            self.active = True
        finally:
            self.logger.info(f'GRPC minio servicer{_str}started.')

    def __del__(self):
        try:
            del self.minio
            self.grpc_server.stop(grace=0)
        except:
            pass
        self.logger.info('GRPC server deleted.')

    # Lowercase - not a GRPC method:
    # def switch(self, is_on: bool):
    #     def f():
    #          self.grpc_server.start()
    #     self._process_error(f)

    def wait_termination(self):
        def f():
            try:
                self.logger.info('Starting waiting termination.')
                self.grpc_server.wait_for_termination()
            except KeyboardInterrupt:
                self.logger.info('Terminated.')
        self._process_error(f)

    # Starting with _ - private methods:
    def _check_connection(self):
        return self.minio.check_connection()

    def _obj_name(self, name: str, version: str) -> str:
        sep = self.name_version_sep
        if sep in (name or version) or '//' in (name or version):
            raise ValueError(HandableServicerErrors
                             .object_characters_incorrect.value)
        return name + self.name_version_sep + version

    def _obj_name_split(self, obj_name: str) -> list[str]:
        name, version = obj_name.split(self.name_version_sep)
        return name, version

    def _process_error(self, function: callable,
                       context=None) -> dict[str, any]:
        ''' returns [result, status] '''
        try:
            status = False
            if self.active:
                result = function()
            else:
                raise ConnectionError
        except ValueError as e:
            print(e)
            try:
                code = ERROR_CODES[e.args[0]]
            except KeyError:
                code = 400
        except ConnectionError:
            if not self.active:
                self.logger.error(self.not_active_msg)
            code = 408
        except Exception as e:
            code = 500
        else:
            status = True
            code = 200
        finally:
            try:  # To use it not only in GRPC functions
                context.set_code(StatusCode.OK)
            finally:
                return {'status':
                            minio_pb2.Status(status=status,
                                             status_code=code,
                                             response=result
                                             if status and isinstance(result, bool) else False),
                        'result': result if status else None}

    def CheckConnection(self, request, context):
        print('New request: CheckConnection')
        return self._process_error(
            lambda: self.minio.check_connection()
        )['status']

    def CheckUser(self, request, context):
        print('New request: CheckUser')
        return self._process_error(
            lambda: self.minio.check_bucket(request.user),
            context
        )['status']  # Uses response fild in Status object

    def AddUser(self, request, context):
        print('New request: Add User')
        return self._process_error(
            lambda: self.minio.add_bucket(request.user),
            context
        )['status']

    def DeleteUser(self, request, context):
        print('New request: Delete User')
        return self._process_error(
            lambda: self.minio.delete_bucket(request.user),
            context
        )['status']

    def GetFilesInfoList(self, request, context):
        print('New request: Get List')
        result = self._process_error(
            lambda: self.minio.get_bucket_objects_info(request.user),
            context
        )
        if result['result']:
            for file in result['result']:
                name, version = self._obj_name_split(file['name'])
                yield minio_pb2.FileInfoResponse(
                    name=name,
                    version=version,
                    date=file['date'],
                    status=result['status']
                )
        else:
            yield minio_pb2.FileInfoResponse(
                name='',   # To prevent attribute errors
                version='',
                date='',
                status=result['status']
            )

    def DownloadFileVersion(self, request, context):
        print('New request: Download FileVersion')
        result = self._process_error(
            lambda: self.minio.get_object(
                request.user,
                self._obj_name(request.name, request.version)
            ), context
        )
        return minio_pb2.FileResponse(data=result['result'],
                                      status=result['status'])

    def AddFileVersion(self, request, context):
        print('New request: Add FileVersion')
        return self._process_error(
            lambda: self.minio.add_object(
                request.user,
                self._obj_name(request.name, request.version),
                request.data
            ), context
        )['status']

    def DeleteFileVersion(self, request, context):
        print('New request: Delete Note')
        return self._process_error(
            lambda: self.minio.delete_object(
                request.user,
                self._obj_name(request.name, request.version)
            ), context
        )['status']

    def DeleteFile(self, request, context):
        def f():
            objects_info = self.minio.get_bucket_objects_info(request.user)
            for object in objects_info:
                if request.name == self._obj_name_split(object['name'])[0]:
                    self.minio.delete_object(request.user, object['name'])
        return self._process_error(f, context)['status']


# def _preprocess_request_args(self, props: dict) -> dict[str, any]:
#     new_args = {}
#     name = ''
#     version = ''
#     # Name and version are specified together one by one!:
#     for arg, value in props:
#         match arg:
#             case 'name':
#                 name = value
#             case 'version':
#                 version = value
#                 new_args['object_name'] = \
#                     self._obj_name(name, version)
#             case _:
#                 new_args[arg] = value
#     return new_args


    # def _process_error(self, function: callable, context, request=None,
    #                    *args) -> any:
    #     ''' returns [result, status] '''
    #     try:
    #         status = False
    #         props_dict = {}
    #         if request:
    #             for arg in args:
    #                 props_dict[arg] = eval(f'request.{arg}')
    #             props_dict = self._preprocess_request_args(props_dict)
    #         props_list = list(props_dict.values())
    #         result = function(*props_list)
    #     except ValueError as e:
    #         with HandableS3Errors as S3, HandableValueErrors as V:
    #             error_codes = {
    #                 S3.bucket_not_found: '401',
    #                 S3.bucket_already_exists: '-',
    #                 S3.object_not_found: '404',
    #                 S3.object_name_too_long: '-',
    #                 V.bucket_characters_incorrect: '-',
    #                 V.bucket_name_too_small: '-',
    #                 V.bucket_name_too_long: '-',
    #                 HandableServicerErrors
    #                 .object_characters_incorrect: '509'
    #             }
    #             try:
    #                 code = error_codes[e.args[0]]
    #             except IndexError:
    #                 code = 400
    #     except ConnectionError:
    #         code = 408
    #     except Exception:
    #         code = 500
    #     else:
    #         status = True
    #         code = 200
    #     finally:
    #         context.set_code(StatusCode.OK)
    #         return {'status': minio_pb2.Status(status=status,
    #                                            status_code=code),
    #                 'result': result if status else None}