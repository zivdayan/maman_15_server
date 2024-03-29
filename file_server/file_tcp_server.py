import selectors
import socket
import logging
from file_server.file_server_request_handler import FileServerRequestHandler
from utils import create_files_dir

sel = selectors.DefaultSelector()


class FileTCPServer:
    """
    The main class defines the infastracture to handle TCP requests.
    """

    LOCALHOST_KEYWORD = 'localhost'
    MAX_CONNECTIONS = 100
    PORT_INFO_FILE_PATH = 'port.info'
    READ_ONLY_FILE_MODE = 'r'
    DEFAULT_PORT = 1234
    FILES_DIR_NAME = 'Files'

    def __init__(self, logger: logging.Logger, files_dir):
        self.logger: logging.Logger = logger
        self.port = FileTCPServer.read_server_port()
        self.max_connections = FileTCPServer.MAX_CONNECTIONS
        self.current_connections = {}
        self.files_dir = files_dir

    @staticmethod
    def read_server_port():
        try:
            with open(FileTCPServer.PORT_INFO_FILE_PATH, FileTCPServer.READ_ONLY_FILE_MODE) as f:
                return int(f.read())

        except Exception as e:
            return FileTCPServer.DEFAULT_PORT

    def accept(self, sock: socket.socket, mask):
        conn, addr = sock.accept()  # Should be ready
        self.logger.info(f"Accepted connection {conn} from {addr}")
        conn.setblocking(False)
        conn.settimeout(1)

        self.current_connections[conn.fileno()] = conn.getpeername()
        sel.register(conn, selectors.EVENT_READ, FileTCPServer.read)

    def close_connection(self, conn):
        try:
            connection_name = self.current_connections[conn.fileno()]
            self.logger.info('closing connection to {0}'.format(connection_name))
            del self.current_connections[conn.fileno()]
            sel.unregister(conn)
            conn.close()
        except Exception:
            self.logger.warning('Connection tried to be closed, although it was already closed')

    def read(self, conn: socket.socket, mask=None):
        data = bytearray()
        batch = 4096
        while True:
            try:
                packet = conn.recv(batch)
                if not packet:
                    break
                data.extend(packet)
            except socket.timeout:
                break

        if data:
            self.logger.debug(f"Received data ({len(data)}) {repr(data)} - to {conn} ")
            response = self.handle_request(data)
            conn.send(response)

            self.logger.debug(f"Sent data in size ({len(response)})")

            self.close_connection(conn)
        else:
            self.close_connection(conn)

    def handle_request(self, raw_request: bytearray) -> bytearray:
        response = FileServerRequestHandler(raw_request, self.files_save_path, self.logger).handle()
        binary_response = response.generate_binary_request()
        self.logger.debug('total response size ' + str(len(binary_response)))
        return binary_response

    def init_server(self, port, max_connections) -> socket.socket:
        """
        :param connections:number of unaccepted connections that the system will allow before refusing new connections.
        """
        sock = socket.socket()
        sock.bind((FileTCPServer.LOCALHOST_KEYWORD, port))
        sock.listen(max_connections)
        sock.settimeout(5)
        sock.setblocking(True)
        sel.register(sock, selectors.EVENT_READ, FileTCPServer.accept)
        return sock

    def start_connections_loop(self):
        self.logger.debug('Starting connection loop')
        while True:
            events = sel.select()
            for key, mask in events:
                callback = key.data
                try:
                    callback(self, key.fileobj, mask)
                except (ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError) as e:
                    self.close_connection(key.fileobj)
                except Exception as e:
                    self.logger.error(f"Internal server error occurred {e}")

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    @property
    def files_save_path(self):
        return self.files_dir + "\\" + self.FILES_DIR_NAME

    def start(self):
        self.socket = self.init_server(self.read_server_port(), self.MAX_CONNECTIONS)
        create_files_dir(path=self.files_dir, dir_name='Files')
        self.start_connections_loop()

    def stop(self):
        self.socket.close()
        self.logger.debug('TCP server closed successfully')
