import os
from core.statics import resource_path


def write(msg: str, file_name: str = 'temp.txt'):
    with open(resource_path(file_name), mode='a+', encoding='utf-8') as f:
        f.write(msg)


def clear(file_name: str = 'temp.txt'):
    with open(resource_path(file_name), mode='a+', encoding='utf-8') as f:
        f.truncate(0)


def read(file_name: str = 'temp.txt'):
    file = open(resource_path(file_name), mode='r', encoding='utf-8')
    all_contents = file.read()
    file.close()
    return all_contents


def check_if_file_has_data(file_name: str = 'temp.txt'):
    f_path = resource_path(file_name)
    return os.path.isfile(f_path) and os.path.getsize(f_path) > 0
