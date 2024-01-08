import os
import sys
import time

special_words = {"parent_dir": "..", "current_dir": ".", "Documents and Settings": "Users", "My Documents": "Documents"}


def create_directory(path, directory_name):
    """
    Creates a new directory within the specified path.

    :param path: str - The path to create the new directory.
    :param directory_name: str - The name of the new directory to create.

    :raises Exception: If the directory already exists or if remove is not possible.
    :return: None
     """
    if os.path.exists(os.path.join(path, directory_name)):
        raise Exception("Directory already exists")
    try:
        os.mkdir(os.path.join(path, directory_name))
    except Exception as e:
        print(e)
        sys.exit(1)


def delete_directory(path):
    """
    Deletes the specified directory.

    :param path: str - The path of the directory to delete.

    :raises Exception: If the directory does not exist.

    :return: None

     """
    if not os.path.exists(path):
        raise Exception("Directory does not exist")
    try:
        os.rmdir(path)
    except Exception as e:
        print(e)
        sys.exit(1)


def get_start_dir():
    """
    Retrieves the starting directory.
    It finds the path of the current script and then it goes up until it reaches the root directory.

    :return: str - The path of the starting directory.

    Example:
        get_start_dir()
    """
    director_curent_script = os.path.abspath(os.path.dirname(__file__))

    while not os.path.ismount(director_curent_script):
        director_curent_script = os.path.dirname(director_curent_script)

    return director_curent_script


def get_all_from_path(path):
    """
    Retrieves a list of elements dictionaries containing information about files and directories in specified path.
    Information about each element:
        - type: file or dir
        - name: the name of the file or directory
        - path: the path of the file or directory
        - size: the size of the file or <<DIR>> if it is a directory
        - extension: the extension of the file or empty string if it is a directory
        - date: the date of the last modification of the file or directory

    :param path: str - The path to retrieve elements from.

    :return: list - A list of dictionaries containing information about files and directories.
    """
    try:
        elements_list = os.listdir(path)
    except PermissionError as e:
        print("Permission denied")
        return []
    response_list = []
    for element in elements_list:
        # if not os.access(os.path.join(path, element), os.R_OK):
        #     continue

        response_el = dict()
        response_el["type"] = "dir" if os.path.isdir(os.path.join(path, element)) else "file"

        if response_el["type"] == "dir":
            print("dir ", element)
            response_el["size"] = "<<DIR>>"
            response_el["extension"] = ""
        else:
            response_el["extension"] = os.path.splitext(element)[1][1:].upper()
            response_el["size"] = os.path.getsize(os.path.join(path, element))

        response_el["name"] = element
        response_el["path"] = os.path.join(path, element)
        response_el["date"] = time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime(os.path.join(path, element))))
        response_list.append(response_el)

    main_dir_name = os.path.basename(path)
    print("main_dirname ", main_dir_name)
    return response_list


def get_all_from_dir(current_main_path, target_dir):
    """
    Retrieves a list of elements (files and directories) within a specified directory relative to the current path.

    :param current_main_path: str - The current main path.
    :param to_dir: str - The target directory within the current main path.

    :raises Exception: If the directory does not exist, or if the path is not a directory, or if permission is denied.

    :return: tuple - A tuple containing the updated main path and a list of elements.
    """
    if target_dir in special_words.keys():
        target_dir = special_words[target_dir]

    updated_main_path = os.path.abspath(os.path.join(current_main_path, target_dir))
    if not os.path.exists(updated_main_path):
        raise Exception("Directory does not exist")

    if not os.path.isdir(updated_main_path):
        raise Exception("Path is not a directory")

    if not os.access(updated_main_path, os.R_OK):
        raise Exception("You don't have permission to read this directory")

    elements_from_dir = get_all_from_path(updated_main_path)

    return updated_main_path, elements_from_dir


def rename(old_name_path, new_name_path):
    """
    Renames a file or directory.

    :param old_name_path: str - The path of the file or directory to rename.
    :param new_name_path: str - The new name or path of the file or directory.

    :return: None
    """
    print(old_name_path, new_name_path)
    if not os.path.exists(old_name_path):
        raise Exception("Path does not exist")

    if not os.access(old_name_path, os.W_OK):
        raise Exception("You don't have permission to rename this file")

    os.rename(old_name_path, new_name_path)


def check_path(path):
    """
    Checks if the given path exists.

    :param path: str - The path to check.

    :return: bool - True if the path exists, False otherwise.

    """
    if not os.path.exists(path):
        return False
    return True


def get_parent_path(path):
    """
    Retrieves the parent path of a given path.

    :param path: str - The path to get the parent path from.

    :return: str - The parent path of the given path.

    """
    return os.path.dirname(path)
