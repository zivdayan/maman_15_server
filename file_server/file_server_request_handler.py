from structures.request import FileServerRequest
from typing import Callable, Dict


class FileServerRequestHandler:

    def __init__(self, raw_request):
        self.raw_request = raw_request

    def handle(self):
        request: FileServerRequest = FileServerRequest.parse_binary_request(self.raw_request)
        requested_function = self.request_to_function_mapping.get(request.code)

        requested_function()

    @property
    def request_to_function_mapping(self) -> Dict[Callable]:
        return {1100: self.register_user, 1101: self.send_public_key, 1103: self.send_file, 1104: self.valid_crc,
                1105: self.invalid_crc, 1106: self.invalid_crc_terminating}

    def register_user(self):
        pass

    def send_public_key(self):
        pass

    def send_file(self):
        pass

    def valid_crc(self):
        pass

    def invalid_crc(self):
        pass

    def invalid_crc_terminating(self):
        pass
