import os


def format_data(data):
    """
    This function iterates through the provided dictionary and converts all values to string type.

    Args:
        data (dict): The dictionary to be formatted.

    :return:
        None

    Example:
        format_data({'key1': {'nested_key': 123, 'nested_list': [1, 2, 3]}, 'key2': [4, 5]})
    """
    for key, value in data.items():
        if isinstance(value, dict):
            format_data(value)
        if isinstance(value, list):
            for item in value:
                format_data(item)

        data[key] = str(value)


def is_subdirectory(subfolder, parent_folder):
    """
    Checks if a folder is a subdirectory of another folder.

    This function determines if 'subfolder' is a subdirectory of 'parent_folder'.

    Args:
        subfolder (str): The path of the potential subdirectory.
        parent_folder (str): The path of the parent directory.

    Returns:
        bool: True if 'subfolder' is a subdirectory of 'parent_folder',
                False otherwise.
    """
    subfolder = os.path.abspath(subfolder)
    parent_folder = os.path.abspath(parent_folder)

    common_path = os.path.commonpath([subfolder, parent_folder])

    return common_path == parent_folder
