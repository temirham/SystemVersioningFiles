from GRPC.GRPC_server import MinioGRPCServicer
from pathlib import Path
from config import Config
from logging import getLogger, Logger, ERROR, INFO, FileHandler, Formatter


def set_logger(logger_name: str, format: str,
               paths_level: list[list[str, str]]) -> Logger:
    logger = getLogger(logger_name)
    logger.setLevel(INFO)
    for path in paths_level:
        new_file_handler = FileHandler(path[0])
        new_file_handler.setLevel(ERROR if path[1].upper() == 'ERROR' else INFO) # ?
        new_file_handler.setFormatter(Formatter(format))
        logger.addHandler(new_file_handler)
    return logger


# f-strings to allow using path with ' ':
CONFIG = Config(f"{Path(__file__).resolve().parent / 'config.cfg'}")
LOGS_DIR = f"{Path(__file__).resolve().parent / 'logs'}/"


if __name__ == '__main__':
    logger = set_logger('GRPS_servicer',  # second is a class name
                        '%(asctime)s - %(levelname)s - %(message)s',
                        [[LOGS_DIR + 'servicer.log', 'INFO']])

    servicer = MinioGRPCServicer(
        {'endpoint': CONFIG['grpc_endpoint'],
         'workers': 10,
         'secure': False,
         'crt_path': '',
         'key_path': ''},
        {'endpoint':   CONFIG['minio_endpoint'],
         'access_key': CONFIG['minio_access_key'],
         'secret_key': CONFIG['minio_secret_key'],
         'secure': False,
         'timeout': 3}
    )

    servicer.wait_termination()



