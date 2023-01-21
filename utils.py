import os


def validate_dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def create_files_dir(path: str, dir_name: str):
    new_dir_path = path + "\\" + dir_name
    if not os.path.exists(new_dir_path):
        os.makedirs(new_dir_path)


def save_file(path: str, data: bytearray):
    with open(path, 'wb') as f:
        f.write(data)

def unpad_binary(data: bytearray, padding: bytearray):
    return data.strip(padding)