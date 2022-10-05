from file_server.file_tcp_server import FileTCPServer
from structures.request import FileServerRequest
from file_server.file_server_request_handler import FileServerRequestHandler
import logging

logging.basicConfig()

logger = logging.getLogger(__name__)


def init_server():
    pass


def main():
    # with FileTCPServer() as server:
    #     server.start()

    try:
        a = FileServerRequestHandler('blbla')
        a.init_db()

        a.request = FileServerRequest(123123, 1, 123, 123123, 'asdas')
        a.register_user()

    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    main()
