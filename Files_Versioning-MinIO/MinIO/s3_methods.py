from minio import Minio, S3Error
from minio.deleteobjects import DeleteObject
from urllib3.exceptions import MaxRetryError
from urllib3.util.timeout import Timeout
from urllib3.util.retry import Retry
from io import BytesIO
from enum import Enum
from logging import Logger, getLogger, Formatter, StreamHandler, DEBUG
from sys import stdout
from typing import Literal


# Some Errors which we handle and show upper:
class HandableS3Errors(Enum):
    # Error bucket specified:
    bucket_not_found = 'NoSuchBucket'
    # Doubling bucket (because we have root access):
    bucket_already_exists = 'BucketAlreadyOwnedByYou'
    # Trying to delete bucket with existed
    bucket_not_empty = 'BucketNotEmpty'
    # When getting non-existent object:
    object_not_found = 'NoSuchKey'
    # When non-unicode name > 255  or unicode name > 85 or having multiple '/' inside
    object_name_too_long_or_prohibited_chars = 'XMinioInvalidObjectName'


class HandableValueErrors(Enum):
    ''' Should be checked by in, not by == ! '''
    bucket_characters_incorrect \
        = 'Bucket name does not follow S3 standards.'
    bucket_name_too_small \
        = 'Bucket name cannot be less than 3 characters.'
    bucket_name_too_long \
        = 'Bucket name cannot be greater than 63 characters.'


# The API functions shouldn't use each other because of incorrect errors handling in other way
# Process only one entity with method (delete objects instead of delete objects) to make logs clear
class MinioClass:
    service_bucket = 'minioservicebucket'
    S3err_msg = 'S3 error occurred: '
    conn_err_msg = 'Connection error: {} not answering.'
    err_msg = 'Unexpected error: '
    not_active_msg = 'Client init was failed.'

    def __init__(self, endpoint: str, access_key: str, secret_key: str,
                 is_secure: bool = False, timeout: int = None, logger: Logger = None):
        try:
            str = ' not '
            self.inited_success = False
            default = getLogger('Minio client')
            default.setLevel(DEBUG)
            cons = StreamHandler(stream=stdout)
            cons.setFormatter(
                Formatter('%(asctime)s - %(name)s'
                          ' - %(levelname)s - %(message)s'))
            default.addHandler(cons)
            self.logger = logger if logger else default
            self.logger.info('Minio client starting.')

            self.endpoint = endpoint
            self.access_key = access_key
            self.secret_key = secret_key
            self.con = Minio(endpoint=endpoint,
                             access_key=access_key,
                             secret_key=secret_key,
                             secure=is_secure)
            self.con._http.connection_pool_kw['retries'] = Retry(total=5)
            if timeout:
                # Total is no more than 6 sec:
                self.con._http.connection_pool_kw['timeout'] = Timeout(total=timeout)
            if not self.check_connection():
                raise ConnectionError
            str = ' '
        except S3Error as e:
            self.logger.error(self.S3err_msg, e)
            raise S3Error
        except ConnectionError as e:
            self.logger.error(self.conn_err_msg.format(self.endpoint))
        except Exception as e:
            self.logger.error(self.err_msg, e)
            raise ConnectionError  # Probably connection too btw
        else:
            self.inited_success = True
        finally:
            self.logger.info(f'Minio client{str}started.')

    def __del__(self):
        self.logger.info('Minio client deleted.')

    def check_connection(self) -> bool:
        try:
            bucket = self.service_bucket
            self.con.bucket_exists(bucket)
            return True
        except:
            return False

    # Adding more info in exceptions needed
    # Starting with _ - private methods:
    def _process_errors(self, function: callable) -> any:
        ''' Returns result or throws one of that errors:
            ValueError(code: str | None), ConnectionError '''
        try:
            if self.inited_success:
                return function()
            raise ConnectionError  # Not to check if client inactive

        # Catching S3 errors:
        except S3Error as e:
            if e.code not in (el.value for el in HandableS3Errors):
                self.logger.error(f'{self.S3err_msg}', e)
                raise ValueError
            raise ValueError(e.code)

        # Catching value errors (minio uses them for
        # bucket names errors):
        except ValueError as e:
            # Because bucket name error text contains
            # bucket name in the end:
            if (el.value not in e.args[0] for el in HandableS3Errors):
                raise e
            self.logger.error(self.S3err_msg, e)
            raise ValueError

        # Checking connections errors:
        except (MaxRetryError, ConnectionError) as e:
            if not self.inited_success:
                # Inactive client:
                self.logger.error(self.not_active_msg)
            else:
                # Connection error:
                self.logger.error(self.conn_err_msg.format(self.endpoint))
            raise ConnectionError

        except Exception as e:
            self.logger.error(self.err_msg, e)
            raise Exception  # Probably connection

    def check_bucket(self, bucket: str) -> bool:
        return self._process_errors(
            lambda: self.con.bucket_exists(bucket)
        )

    # Change _check_connection if bucket funcs below rewrote!
    def add_bucket(self, bucket: str):
        self._process_errors(
            lambda: self.con.make_bucket(bucket)
                    if not self.con.bucket_exists(bucket)
                    else None  # To prevent errors
        )

    def delete_bucket(self, bucket: str):
        def f():
            if self.con.bucket_exists(bucket):
                objects = [
                    DeleteObject(o.object_name)
                    for o in self.con.list_objects(bucket_name=bucket,
                                                   recursive=True)
                ]
                for err in self.con.remove_objects(bucket, objects):
                    raise err
                self.con.remove_bucket(bucket)
        self._process_errors(f)

    # Not used
    def check_object(self, bucket: str, obj_name: str) -> bool:
        def f():
            try:
                self.con.stat_object(bucket, obj_name)
                return True
            except S3Error as e:
                if e.code == 'NoSuchKey':
                    return False
                else:
                    raise e
        return self._process_errors(f)

    def get_bucket_objects_info(self, bucket: str) -> \
            list[dict[Literal['name', 'date', 'size']]]:
        def f():
            objects_info_list = []
            objects_list = self.con.list_objects(bucket_name=bucket)
            for object in objects_list:
                result = dict(name=object.object_name,
                              date=str(object.last_modified)[:19],
                              size=object.size)
                objects_info_list.append(result)
            objects_info_list = sorted(objects_info_list,
                                       key=lambda d: d['date'])
            return objects_info_list[::-1]
        return self._process_errors(f)

    def get_object(self, bucket: str, obj_name: str) -> bytes:
        return self._process_errors(
            lambda: self.con.get_object(bucket_name=bucket,
                                        object_name=obj_name).read()
        )

    def add_object(self, bucket: str, obj_name: str, data: bytes):
        self._process_errors(
            lambda: self.con.put_object(bucket_name=bucket,
                                        object_name=obj_name,
                                        data=BytesIO(data),  # Important!
                                        length=len(data))
        )

    def delete_object(self, bucket: str, obj_name: str):
        self._process_errors(
            lambda: self.con.remove_object(bucket_name=bucket,
                                           object_name=obj_name)
        )

    # Not tested and not used:
    def delete_folder(self, bucket, folder: str):
        def f():
            objects = [
                DeleteObject(o.object_name)
                for o in self.con.list_objects(bucket_name=bucket,
                                               prefix=folder,
                                               recursive=True)
            ]
            for err in self.con.remove_objects(bucket, objects):
                raise err
        self._process_errors(f)


    # def delete_objects(self, bucket: str, obj_list: list[str]):
    #     def f():
    #         for err in self.con.remove_objects(bucket, [DeleteObject(object)
    #                                                     for object in obj_list]):
    #             raise err
    #     return self._process_errors(f)

    # def add_objects(self, bucket: str, objects_dict: dict[str, bytes]):
    #     self._process_errors(
    #         lambda: self.con.put_object(bucket_name=bucket,
    #                                     object_name=obj_name,
    #                                     data=BytesIO(data),
    #                                     length=len(data))
    #         for obj_name, data in objects_dict
    #     )