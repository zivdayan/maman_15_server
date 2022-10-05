from file_server.file_tcp_server import FileTCPServer


def init_server():
    pass


def main():
    with FileTCPServer() as server:
        server.start()


if __name__ == '__main__':
    main()
