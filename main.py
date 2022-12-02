from file_server.file_tcp_server import FileTCPServer
import logging

logging.basicConfig(format='%(asctime)s %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

clients = dict()  # Global variable, contains all of the client's data


def main():
    logger.info('Starting TCP Server')
    with FileTCPServer(logger=logger) as server:
        server.start()


if __name__ == '__main__':
    main()
