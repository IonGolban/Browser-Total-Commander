import os
import sys
import shutil


def copy_file(source_dir, destination_dir, file_name, replace=False):
    if not os.path.exists(source_dir):
        raise Exception("Source directory does not exist")
    if not os.path.exists(destination_dir):
        raise Exception("Destination directory does not exist")

    if not os.path.isfile(os.path.join(source_dir, file_name)):
        raise Exception("File does not exist in source directory")
    if os.path.isfile(os.path.join(destination_dir, file_name)) and not replace:
        raise Exception("File already exist in destination directory, you can replace it")

    try:
        shutil.copy(os.path.join(source_dir, file_name), destination_dir)
    except Exception as e:
        print(e)
        sys.exit(1)

def delete_file(path):
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
        sys.exit(1)



source_path = r"C:\Users\uig26544\Desktop\from_py_proj"
destination_path = r"C:\Users\uig26544\Desktop\to_py_proj"
file_name = "test.txt"

# copy_file(source_path, destination_path, file_name)
