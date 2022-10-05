import struct


class FileServerResponse:
    def __init__(self, version, code, payload_size, payload):
        self.client_id = version
        self.code = code
        self.payload_size = payload_size
        self.payload = payload

    @classmethod
    def parse_binary_request(cls, raw_request):
        '''
             +----+-----+-------+------+----------+--------+
              | version  |  code  | payload_size | payload |
              -----------+--------+--------------+---------|
              |    1     |    2   |      4       | Variable|
              +----+-----+--------+--------------+----------+

       :return:


       '''

        try:

            client_id = None
            version = None
            code = None
            payload = None

            format = '<'  # Little endian annotation
            format += 'c'  # version
            format += 'B'  # code
            format += 'I'  # unsigned payload size
            payload_size = int(raw_request[20:24])  # extract payload size from raw request
            format += f"{payload_size}s"

            struct.unpack(format, client_id, version, code, payload_size, payload)

            return cls(client_id=client_id, version=version, code=code, payload_size=payload_size, payload=payload)

        except Exception:
            raise FileServerRequest.InvalidException


class InvalidRequest(Exception):
    """Base class for other exceptions"""
    pass


class UserAlreadyRegistered(Exception):
    """Base class for other exceptions"""
    pass
