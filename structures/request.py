import struct


class FileServerRequest:
    BASE_REQUEST_LENGTH = 23

    def __init__(self, client_id, version, code, payload_size, payload):
        self.client_id = client_id
        self.version = version
        self.code = code
        self.payload_size = payload_size
        self.payload = payload

    @classmethod
    def parse_binary_request(cls, raw_request):
        '''
             +----+-----+-------+------+----------+----------+
              |client_id | version |  code  | payload_size | payload |
              +----+-----+-------+------+----------+----------+
              |    16    |     1   |    2   |      4       | Variable |
              +----+-----+-------+------+----------+----------+

       :return:


       '''

        try:
            base_request = raw_request[:FileServerRequest.BASE_REQUEST_LENGTH]
            client_id = None
            version = None
            code = None
            payload = None
            payload_size = None

            format = '<'  # Little endian annotation
            format += '16s'  # client_id
            format += 'c'  # version
            format += 'H'  # code
            format += 'I'  # unsigned payload size

            client_id, version, code, payload_size = struct.unpack(format, base_request)

            payload = raw_request[
                      FileServerRequest.BASE_REQUEST_LENGTH:FileServerRequest.BASE_REQUEST_LENGTH + payload_size]

            return cls(client_id=client_id, version=version, code=code, payload_size=payload_size, payload=payload)

        except Exception:
            raise InvalidRequest


class InvalidRequest(Exception):
    """Base class for other exceptions"""
    pass


class UserAlreadyRegistered(Exception):
    """Base class for other exceptions"""
    pass
