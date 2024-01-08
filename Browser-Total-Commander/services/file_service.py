import copy
import os
import sys
import shutil
from services import dir_service
from services import utils


def copy_all(source_dir, destination_dir, elements, replace=False, delete_after=False, initial_dir=None):
    if not os.path.exists(source_dir):
        raise Exception("Source directory does not exist")
    if not os.path.exists(destination_dir):
        raise Exception("Destination directory does not exist")

    try:
        for element in elements:

            element_path = os.path.join(source_dir, element)
            dest_element_path = os.path.join(destination_dir, element)

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
                delete(initial_dir, [element])
    except Exception as e:
        print(e)
        raise Exception("Error while copying/move files : " + str(e))


def delete(source_dir, elements):
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


def delete_file(main_dir, file_name):
    path = os.path.join(main_dir, file_name)
    if not os.path.exists(path):
        raise Exception("File does not exist")
    try:
        os.remove(path)
    except Exception as e:
        print(e)
        sys.exit(1)


def create_file(path, file_name):
    if os.path.exists(os.path.join(path, file_name)):
        raise Exception("File already exists")
    try:
        with open(os.path.join(path, file_name), 'w') as file:
            file.write('')
    except Exception as e:
        print(e)
        raise Exception("Error while creating file" + str(e))


def get_content(path, file_name):
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
    try:
        with open(source_path, 'rb') as source_file:
            with open(destination_path, 'wb') as dest_file:
                dest_file.write(source_file.read())
    except IOError as e:
        print(f"Unable to copy file: {e}")
        raise Exception("Error while copying file" + str(e))
