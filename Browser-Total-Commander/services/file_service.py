import copy
import os
import sys
import shutil
from services import dir_service
from services import utils


def copy_all(source_dir, destination_dir, elements, replace=False, delete_after=False, initial_dir=None):
    """
    Copies all specified elements from a source directory to a destination directory.
    If the element is a directory, it will copy all its content recursively.
    If the element is a file and it already exists in the destination directory
        -> replace == True: The file will be copied and the existing file will be replaced.
        -> replace == False: The file will not be copied.
    If delete_after == True, the source elements will be deleted after copying (Move operation).

    :param source_dir: str - The source directory path.
    :param destination_dir: str - The destination directory path.
    :param elements: list - List of elements (files/directories) to be copied.
    :param replace: bool - Whether to replace existing files in the destination directory (default: False).
    :param delete_after: bool - Whether to delete the source elements after copying (default: False).
    :param initial_dir: str - The initial directory path (default: None).

    :raises Exception: If there's an error while copying/moving files.
    :raises Exception: If the destination directory does not exist.
    :raises Exception: If the source directory does not exist.
    :raises Exception: If the source directory is the same as the destination directory.
    :raises Exception: If the source directory is a subdirectory of the destination directory.

    :return: None
        """
    if not os.path.exists(source_dir):
        raise Exception("Source directory does not exist")
    if not os.path.exists(destination_dir):
        raise Exception("Destination directory does not exist")

    for element in elements:
        element_path = os.path.join(source_dir, element)
        if not os.path.exists(element_path):
            raise Exception("Element does not exist" + str(os.path.join(source_dir, element)))
        if utils.is_subdirectory( destination_dir, element_path):
            raise Exception("Cannot copy/move directory into itself")
    try:
        for element in elements:

            element_path = os.path.join(source_dir, element)
            dest_element_path = os.path.join(destination_dir, element)
            if not os.path.exists(element_path):
                raise Exception("Element does not exist")

            if os.path.isdir(element_path):
                if element_path == destination_dir or utils.is_subdirectory(dest_element_path, element_path):
                    raise Exception("Cannot copy/move directory into itself")
                if not os.path.exists(dest_element_path):
                    os.makedirs(dest_element_path)
                sub_elements = os.listdir(element_path)
                copy_all(copy.deepcopy(element_path), copy.deepcopy(dest_element_path), sub_elements, replace=replace,
                         delete_after=delete_after, initial_dir=initial_dir)
            elif os.path.isfile(element_path):
                if os.path.exists(dest_element_path) and not replace:
                    print(f"File {element} already exists in destination directory, skipping.")
                else:
                    copy_file(element_path, dest_element_path)
            else:
                print(f"Skipping element {element} ")
            if delete_after:
                delete_all(initial_dir, [element])
    except Exception as e:
        print(e)
        raise Exception("Error while copying/move files : " + str(e))


def delete_all(source_dir, elements):
    """
    Deletes specified elements (files or directories) from the source directory.

    :param source_dir: str - The source directory path.
    :param elements: list - List of elements (files/directories) to be deleted.

    :raises Exception: If there's an error while deleting files.
    :raises Exception: If the source directory does not exist.


    :return: None
        """
    if not os.path.exists(source_dir):
        raise Exception("Source directory does not exist")

    try:
        for element in elements:
            element_path = os.path.join(source_dir, element)
            if os.path.isdir(element_path):
                shutil.rmtree(element_path)
            elif os.path.isfile(element_path):
                os.remove(element_path)
            else:
                print(f"Skipping element {element} because it is not a file or directory.")
    except Exception as e:
        print(e)
        raise Exception("Error while deleting files")


def delete_file(path):
    """
    Deletes the specified element from the specified path.
    :param path: str - The path of the element to delete.
    :return: None
    :raises Exception: If the element does not exist.

    """

    if not os.path.exists(path):
        raise Exception("File does not exist")
    try:
        os.remove(path)
    except Exception as e:
        print(e)
        sys.exit(1)


def create_file(path, file_name):
    """
    Creates an empty file in the specified directory.

    :param path: str - The directory path where the file will be created.
    :param file_name: str - The name of the file to be created.

    :raises Exception: If the file already exists or there's an error while creating the file.
    :raises
    :return: None
    """
    if os.path.exists(os.path.join(path, file_name)):
        raise Exception("File already exists")
    try:
        with open(os.path.join(path, file_name), 'w') as file:
            file.write('')
    except Exception as e:
        print(e)
        raise Exception("Error while creating file" + str(e))


def get_content(path, file_name):
    """
    Retrieves the content of a file.

    :param path: str - The directory path where the file exists.
    :param file_name: str - The name of the file to retrieve content from.

    :raises Exception: If the file does not exist
    :raises Exception: Not a file
    :raises Exception: Error while reading the file.

    :return: str - The content of the file.
    """
    if not os.path.exists(os.path.join(path, file_name)):
        raise Exception("File does not exist")
    if not os.path.isfile(os.path.join(path, file_name)):
        raise Exception("Not a file")
    try:
        with open(os.path.join(path, file_name), 'r') as file:
            return file.read()
    except Exception as e:
        print(e)
        raise Exception("Error while reading file" + str(e))


def edit_content(dir, file_name, content):
    """
    Edits the content of a file.

    :param dir: str - The directory path where the file exists.
    :param file_name: str - The name of the file to edit.
    :param content: str - The new content to be written to the file.

    :raises Exception: Error while editing the file.
    :raises Exception: If the file does not exist
    :raises Not a file
    :return: None
        """
    if not os.path.exists(os.path.join(dir, file_name)):
        raise Exception("File does not exist")
    if not os.path.isfile(os.path.join(dir, file_name)):
        raise Exception("Not a file")
    try:
        with open(os.path.join(dir, file_name), 'w') as file:
            file.write(content)
    except Exception as e:
        print(e)
        raise Exception("Error while editing file" + str(e))


def copy_file(source_path, destination_path):
    """
    Copies a file from the source path to the destination path.

    :param source_path: str - The source file path.
    :param destination_path: str - The destination file path.

    :raises Exception: If there's an error while copying the file.

    :return: None
    """
    try:
        with open(source_path, 'rb') as source_file:
            with open(destination_path, 'wb') as dest_file:
                dest_file.write(source_file.read())
    except IOError as e:
        print(f"Unable to copy file: {e}")
        raise Exception("Error while copying file" + str(e))
