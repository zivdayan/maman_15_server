from file_server.file_tcp_server import FileTCPServer
import logging
import os
import argparse
from utils import validate_dir_path
import logger_utils

logger = logging.getLogger(__name__)
logger_utils.init_logger(logger)

clients = dict()  # Global variable, contains all of the client's data

files_dir = os.getcwd()


def main():
    parser = argparse.ArgumentParser(
        prog='End-To-End encrypted files transmission',
        description='The program securely allows the user to transfer files easily and safely (using RSA and AES encryptions)')
    parser.add_argument('-p', '--path', type=validate_dir_path, default=files_dir,
                        help='The path in which new dir named Files will be created, and within the files will be saved')
    args = parser.parse_args()

    logger.info('Starting TCP Server')
    with FileTCPServer(logger=logger, files_dir=args.path) as server:
        server.start()


if __name__ == '__main__':
    main()
