import os
import sys
import shutil
from services import dir_service

def copy_file(source_path, destination_path):
    try:
        with open(source_path, 'rb') as source_file:
            with open(destination_path, 'wb') as dest_file:
                dest_file.write(source_file.read())
    except IOError as e:
        print(f"Unable to copy file: {e}")
        sys.exit(1)


def copy_all(source_dir, destination_dir, elements, replace=False, delete_after=False):
    if not os.path.exists(source_dir):
        raise Exception("Source directory does not exist")
    if not os.path.exists(destination_dir):
        raise Exception("Destination directory does not exist")

    try:
        for element in elements:
            element_path = os.path.join(source_dir, element)
            dest_element_path = os.path.join(destination_dir, element)

            if os.path.isdir(element_path):
                if not os.path.exists(dest_element_path):
                    os.makedirs(dest_element_path)
                sub_elements = os.listdir(element_path)
                copy_all(element_path, dest_element_path, sub_elements, replace=replace, delete_after=delete_after)
                if delete_after:
                    dir_service.delete_directory(element_path)
            elif os.path.isfile(element_path):
                if os.path.exists(dest_element_path) and not replace:
                    print(f"File {element} already exists in destination directory, skipping.")
                else:

                    copy_file(element_path, dest_element_path)
                    if delete_after:
                        delete_file(source_dir, element)
            else:
                print(f"Skipping element {element} because it is not a file or directory.")

            if delete_after:
                delete_file(source_dir, element)
    except Exception as e:
        print(e)
        raise Exception("Error while copying/move files")


def delete_all(source_dir, elements):
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
    try:
        with open(os.path.join(path, file_name), 'w') as file:
            file.write('')
    except Exception as e:
        print(e)


source_path = r"C:\Users\uig26544\Desktop\from_py_proj"
destination_path = r"C:\Users\uig26544\Desktop\to_py_proj"
file_name = "test.txt"

# copy_file(source_path, destination_path, file_name)
