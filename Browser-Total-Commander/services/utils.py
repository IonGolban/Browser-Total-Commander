import os


def format_data(data):
    for key, value in data.items():
        if isinstance(value, dict):
            format_data(value)
        if isinstance(value, list):
            for item in value:
                format_data(item)

        data[key] = str(value)


# def is_subdirectory(path, potential_parent):
#     path = os.path.realpath(path)
#     potential_parent = os.path.realpath(potential_parent)
#     relative = os.path.relpath(potential_parent, path)
#     return not (relative == os.pardir or relative.startswith(os.pardir + os.sep))

def is_subdirectory(subfolder, parent_folder):
    subfolder = os.path.abspath(subfolder)
    parent_folder = os.path.abspath(parent_folder)

    common_path = os.path.commonpath([subfolder, parent_folder])

    return common_path == parent_folder
