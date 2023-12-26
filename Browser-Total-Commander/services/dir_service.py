import os
import sys
import shutil
import time


def create_directory(path, directory_name):
    try:
        os.mkdir(os.path.join(path, directory_name))
    except Exception as e:
        print(e)
        sys.exit(1)


def delete_directory(path):
    try:
        os.rmdir(path)
    except Exception as e:
        print(e)
        sys.exit(1)


def get_main_dir():
    director_curent_script = os.path.abspath(os.path.dirname(__file__))

    while not os.path.ismount(director_curent_script):
        director_curent_script = os.path.dirname(director_curent_script)

    return director_curent_script


def get_all_from_dir(path):
    elements_list = os.listdir(path)
    response_list = list()
    for element in elements_list:
        response_el = dict()
        response_el["name"] = element
        response_el["path"] = os.path.join(path, element)
        response_el["size"] = os.path.getsize(os.path.join(path, element))
        response_el["date"] = time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime(os.path.join(path, element))))
        response_el["type"] = "dir" if os.path.isdir(os.path.join(path, element)) else "file"
        response_list.append(response_el)

    return response_list
