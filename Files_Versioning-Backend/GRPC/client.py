from grpc import insecure_channel, secure_channel
from grpc._channel import _InactiveRpcError
from GRPC.protos import minio_pb2_grpc, minio_pb2
from Site.settings import CONFIG
    # LOGGER


stub = None


def connect_storage():
    global stub
    endpoint = CONFIG.get('GRPC client', 'endpoint')
    if CONFIG.getboolean('GRPC client', 'secure'):
        channel = secure_channel(endpoint)
    else:
        channel = insecure_channel(endpoint)
    try:
        # LOGGER.info('Connecting to minio client by GRPC.')
        stub = minio_pb2_grpc.MinioMethodsStub(channel)
        query = stub.CheckConnection(minio_pb2.EmptyRequest())
        if query.status and query.response:
            pass
            # LOGGER.info('Client successfully connected.')
        else:
            raise ConnectionError
    except _InactiveRpcError as e:
        pass
        # LOGGER.error(f'Connection to {CONFIG("grpc_endpoint")} was failed.', e)
    except ConnectionError:
        pass
        # LOGGER.error(f'Testing minio client at was failed.')
    except Exception as e:
        print(type(e))
        # LOGGER.error('Connection failed with unexpected error:', e)


if __name__ == '__main__':
    connect_storage()
