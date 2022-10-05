import selectors
import socket

sel = selectors.DefaultSelector()


class FileTCPServer:
    LOCALHOST_KEYWORD = 'localhost'
    MAX_CONNECTIONS = 100
    PORT_INFO_FILE_PATH = '../port.info'
    READ_ONLY_FILE_MODE = 'r'
    DEFAULT_PORT = 1234

    def __init__(self):
        self.port = FileTCPServer.read_server_port()
        self.max_connections = FileTCPServer.MAX_CONNECTIONS

    @staticmethod
    def read_server_port():

        try:
            with(FileTCPServer.PORT_INFO_FILENAME, FileTCPServer.READ_ONLY_FILE_MODE) as f:
                return int(f.read())

        except Exception:
            return FileTCPServer.DEFAULT_PORT

    @staticmethod
    def accept(sock, mask):
        conn, addr = sock.accept()  # Should be ready
        print('accepted', conn, 'from', addr)
        conn.setblocking(False)
        sel.register(conn, selectors.EVENT_READ, FileTCPServer.read)

    @staticmethod
    def read(conn, mask):
        data = conn.recv(1024)  # Should be ready
        if data:
            print('echoing', repr(data), 'to', conn)
            conn.send(data)  # Hope it won't block
        else:
            print('closing', conn)
            sel.unregister(conn)
            conn.close()

    @staticmethod
    def init_server(port, max_connections):
        """
        :param connections:number of unaccepted connections that the system will allow before refusing new connections.
        """

        sock = socket.socket()
        sock.bind((FileTCPServer.LOCALHOST_KEYWORD, port))
        sock.listen(max_connections)
        sock.setblocking(False)
        sel.register(sock, selectors.EVENT_READ, FileTCPServer.accept)

    def start_connections_loop(self):
        while True:
            events = sel.select()
            for key, mask in events:
                callback = key.data
            callback(key.fileobj, mask)

    def start(self):
        self.init_server()
        self.start_connections_loop()

    def stop(self):
        pass
