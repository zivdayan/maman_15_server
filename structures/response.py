import struct


class FileServerResponse:
    def __init__(self, version, code, payload_size, payload):
        self.version = version
        self.code = code
        self.payload_size = payload_size
        self.payload = payload

    def generate_binary_request(self):
        '''
             +----+-----+-------+------+----------+--------+
              | version  |  code  | payload_size | payload |
              -----------+--------+--------------+---------|
              |    1     |    2   |      4       | Variable|
              +----+-----+--------+--------------+----------+

       :return:


       '''

        try:

            format = '<'  # Little endian annotation
            format += 'c'  # version
            format += 'H'  # code
            format += 'I'  # unsigned payload size
            format += f"{self.payload_size}s"

            if type(self.payload) is str:
                self.payload = self.payload.encode()

            print(f"payload = {self.payload}")
            return struct.pack(format, self.version, self.code, self.payload_size, self.payload)

        except Exception as e:
            print(str(e))
            raise FileServerResponse.InvalidException


class InvalidRequest(Exception):
    """Base class for other exceptions"""
    pass


class UserAlreadyRegistered(Exception):
    """Base class for other exceptions"""
    pass
