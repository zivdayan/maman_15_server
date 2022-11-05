import struct


class FileServerResponse:
    def __init__(self, version, code, payload_size, payload):
        self.version = version
        self.code = code
        self.payload_size = payload_size
        self.payload = payload

    @classmethod
    def generate_binary_request(cls, raw_request):
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
            payload_size = None

            format = '<'  # Little endian annotation
            format += 'c'  # version
            format += 'H'  # code
            format += 'I'  # unsigned payload size

            struct.pack(format, version, code, payload_size)

            return cls(client_id=client_id, version=version, code=code, payload_size=payload_size, payload=payload)

        except Exception:
            raise FileServerResponse.InvalidException


class InvalidRequest(Exception):
    """Base class for other exceptions"""
    pass


class UserAlreadyRegistered(Exception):
    """Base class for other exceptions"""
    pass
