import os
import sys
import shutil


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
    return os.listdir(path)
