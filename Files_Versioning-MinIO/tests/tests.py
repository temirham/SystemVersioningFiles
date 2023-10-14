from MinIO.s3_methods import MinioClass
import grpc
from GRPC.protos import minio_pb2, minio_pb2_grpc
from google.protobuf.message import Message
from grpc._channel import _Rendezvous, _InactiveRpcError
from settings import set_logger


def minio_function_test(func: callable, *args: any,
                        returns_result: bool = False) -> any:
    print('result: ')
    br = '   '
    try:
        result = func(*args)
        print(br+str(result if returns_result else 'Success'))
        return result
    except ValueError as e:
        try:
            print(br+'S3 error: ' + e.args[0])
        except:
            print(br+f'Failed, unexpected S3 error: \n{br} ', e)
    except ConnectionError:
        print(br+'Connection error.')
    except Exception as e:
        print(br+f'Failed, unexpected error:\n{br} ', e)


def servicer_function_test(func: callable, *args: any,
                           returns_result: bool = False) -> any:
    print('result: ')
    br = '   '
    result = func(*args)
    try:
        match result:
            # For single messages:
            case Message():
                try:
                    # Status object:
                    status_msg = br+f'status: {result.status}, ' \
                                    f'code: {result.status_code}, '
                    if returns_result:
                        status_msg += f'value: {result.response}'
                    print(status_msg)
                except:
                    print(br+str(result.data))
                        # print(br+f'status: {result.status}, code: {result.status_code}')
            # For stream:
            case _Rendezvous():
                for sub_result in result:  # result is grpc object
                    print(br+ f'name: {sub_result.name}\n' +
                          br+f'file version: {sub_result.version}\n' +
                          br+ f'date: {sub_result.date}\n' +
                          br+f'status: {sub_result.status.status}, '+
                          f'code: {sub_result.status.status_code}',
                          end=br+f'\n----\n')

        return result
    except _InactiveRpcError:
        print(br+'Connection error.')
    except Exception as e:
        print(br+'Failed, unexpected error (probably on client side).'+e)


def test_minio(endnoint: str, acces_key: str, secret_key: str,
               bucket_name: str, object_name: str, logger: object = None):

    print('-------------- Minio test start--------------')
    minio = MinioClass(endnoint, acces_key,
                       secret_key, False, logger)

    print("-------------- AddBucket --------------")
    print('Bucket name: ' + bucket_name)
    minio_function_test(minio.add_bucket, bucket_name)

    print("-------------- CheckBucketExists (True) --------------")
    minio_function_test(minio.check_bucket,
                        bucket_name, returns_result=True)

    print("-------------- AddObject --------------")
    def add_file(_object_name):
        print('Adding file: ' + _object_name)
        with open(object_name, 'rb') as file:
            print('File text: ' + str(file.read()))
            file.seek(0)
            minio_function_test(minio.add_object, bucket_name,
                                _object_name,
                                file.read())
    add_file(object_name)

    print("-------------- CheckOjectExists (True) --------------")
    minio_function_test(minio.check_object, bucket_name,
                        object_name, returns_result=True)

    print("-------------- GetObjectsInfo --------------")
    def get_obj_info():
        minio_function_test(minio.get_bucket_objects_info,
                            bucket_name, returns_result=True)
    get_obj_info()

    print("-------------- DownloadObject --------------")
    loaded_file = object_name.split('.')
    result = minio_function_test(minio.get_object,
                                 bucket_name,
                                 object_name,
                                 returns_result=True)
    if result:
        new_name = loaded_file[-2] + '_minio_loaded.' + loaded_file[-1]
        print('Downloaded into: \n   ' + new_name)
        with open(new_name, 'wb') as file:
            file.write(result)


    print("-------------- DeleteObject --------------")
    minio_function_test(minio.delete_object,
                        bucket_name, object_name)

    print("-------------- CheckObjectExists (False) --------------")
    minio_function_test(minio.check_object, bucket_name,
                        object_name, returns_result=True)

    # print("-------------- DeleteFewObjects --------------")
    # object_name_1 = object_name + '1'
    # object_name_2 = object_name + '2'
    # add_file(object_name_1)
    # add_file(object_name_2)
    # # print('Deleting few objects:')
    # # minio_function_test(minio.delete_objects, bucket_name,
    # #                     [object_name_1, object_name_2])
    # # print('After deletion:')
    # # get_obj_info()

    print("-------------- DeleteBucket --------------")
    minio_function_test(minio.delete_bucket, bucket_name)

    print("-------------- CheckBucketExists (False) --------------")
    minio_function_test(minio.check_bucket,
                        bucket_name, returns_result=True)
    print("-------------- TestEnd --------------")
    del minio


def test_grpc_minio_servicer(endpoint: str, username: str,
                             filename: str, version: str, logger: object = None):

    print('\n\n--------- GRPC + Minio unit test start ---------')
    print('Grpc servicer should be running for test.')

    with grpc.insecure_channel(endpoint) as channel:
        stub = minio_pb2_grpc.MinioMethodsStub(channel)
        grpc_user = minio_pb2.User(user=username)
        grpc_file_req = minio_pb2.FileRequest(user=username,
                                              name=filename,
                                              version=version)

        print("-------------- AddUser --------------")
        servicer_function_test(stub.AddUser, grpc_user)

        print("-------------- CheckUser (True) --------------")
        servicer_function_test(stub.CheckUser, grpc_user, returns_result=True)

        print("-------------- AddFile --------------")
        with open(filename, 'rb') as file:
            print('Filename: ' + filename)
            print('File text: ' + str(file.read()))
            file.seek(0)
            servicer_function_test(stub.AddFileVersion,
                                   minio_pb2.FileAddRequest(user=username,
                                                            name=filename,
                                                            version=version,
                                                            data=file.read())
                                   )
        # input()
        print("-------------- GetFilesInfo --------------")
        servicer_function_test(stub.GetFilesInfoList, grpc_user)

        print("-------------- DownloadFile ---------------")
        print('Filename: ' + filename)
        loaded_file = filename.split('.')
        result = servicer_function_test(stub.DownloadFileVersion, grpc_file_req)
        if result:
            new_name = loaded_file[-2] + '_grpc_minio_loaded.' + loaded_file[-1]
            print('Downloaded into: \n   ' + new_name[0:])
            with open(new_name, 'wb') as file:
                file.write(result.data)

        print("-------------- DeleteFile --------------")
        servicer_function_test(stub.DeleteFileVersion, grpc_file_req)

        print("-------------- DeleteUser --------------")
        servicer_function_test(stub.DeleteUser, grpc_user)

        print("-------------- CheckUser (False)--------------")
        servicer_function_test(stub.CheckUser, grpc_user, returns_result=True)

        print("-------------- TestEnd --------------")

def run_tests():
    username = 'user1'
    filename = 'Mur-mur-mur.txt'
    version = '1'
    sep = '_'
    logger = set_logger('testing:',  # second is a class name
                        '%(asctime)s - %(message)s',
                        [['tests.log', 'info']])

    # test_minio('localhost:6000', 'minio', 'miniosecret',
    #            username, filename)
    test_grpc_minio_servicer('localhost:30000', username,
                             filename, version, logger)


if __name__ == '__main__':
    run_tests()
