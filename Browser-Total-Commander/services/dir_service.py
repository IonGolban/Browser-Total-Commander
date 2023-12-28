import os
import sys
import shutil
import time

special_words = {"parent_dir": "..", "current_dir": ".", "Documents and Settings": "Users", "My Documents": "Documents"}


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


def get_start_dir():
    director_curent_script = os.path.abspath(os.path.dirname(__file__))

    while not os.path.ismount(director_curent_script):
        director_curent_script = os.path.dirname(director_curent_script)

    return director_curent_script


def get_all_from_path(path):
    try:
        elements_list = os.listdir(path)
    except PermissionError as e:
        print("Permission denied")
        return []
    response_list = []
    for element in elements_list:
        if not os.access(os.path.join(path, element), os.R_OK):
            continue

        response_el = dict()
        response_el["type"] = "dir" if os.path.isdir(os.path.join(path, element)) else "file"

        if response_el["type"] == "dir":
            print("dir ", element)
            response_el["size"] = "<<DIR>>"
        else:
            response_el["size"] = os.path.getsize(os.path.join(path, element))

        response_el["name"] = element
        response_el["path"] = os.path.join(path, element)
        response_el["size"] = os.path.getsize(os.path.join(path, element))
        response_el["date"] = time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime(os.path.join(path, element))))
        response_list.append(response_el)

    main_dir_name = os.path.basename(path)
    print("main_dirname ", main_dir_name)
    return response_list


def get_all_from_dir(current_main_path, to_dir):
    if to_dir in special_words.keys():
        to_dir = special_words[to_dir]

    updated_main_path = os.path.abspath(os.path.join(current_main_path, to_dir))
    if not os.path.exists(updated_main_path):
        raise Exception("Directory does not exist")

    if not os.path.isdir(updated_main_path):
        raise Exception("Path is not a directory")

    if not os.access(updated_main_path, os.R_OK):
        raise Exception("You don't have permission to read this directory")

    elements_from_dir = get_all_from_path(updated_main_path)

    return updated_main_path, elements_from_dir


def rename(old_name_path, new_name_path):
    if not os.path.exists(old_name_path):
        raise Exception("Path does not exist")

    if not os.access(old_name_path, os.W_OK):
        raise Exception("You don't have permission to rename this file")

    os.rename(old_name_path, new_name_path)