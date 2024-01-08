from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from services import dir_service, file_service
import json

app = Flask(__name__)

# my_test_dir = r"C:\Users\Public\Desktop\garb_files"


@app.route('/')
def init_page():
    """
    Initializes the page with data for two panels based on 'my_test_dir'.

    This route retrieves data using 'dir_service.get_all_from_path' for the start directory
    and constructs a response containing data for both 'panel_1' and 'panel_2'.
    It then renders the 'index.html' template with the constructed JSON data.

    :returns: str: HTML content rendered from 'index.html' template with JSON data for panels.
    """
    try:
        start_dir = dir_service.get_start_dir()
        data = dir_service.get_all_from_path(start_dir)

        response_data = {
            'panel_1': {'path': start_dir, 'data': data},
            'panel_2': {'path': start_dir, 'data': data}
        }

        print(response_data)
        return render_template('index.html', jsonData=response_data)
    except Exception as e:
        print(e)


@app.route('/goto/<main_dir_1>/<main_dir_2>/', methods=["GET"])
def goto(main_dir_1, main_dir_2):
    """
        Navigates to specified directories within the file manager.

        This route checks if the provided directories exist using 'dir_service.check_path'.
        If they don't exist, it retrieves their parent paths using 'dir_service.get_parent_path'.
        Then, it constructs data for both 'panel_1' and 'panel_2' based on the specified directories.
        Renders the 'index.html' template with the constructed JSON data.

        Args:
            main_dir_1 (str): The path to the directory for 'panel_1'.
            main_dir_2 (str): The path to the directory for 'panel_2'.

        :return: HTML content rendered from 'index.html' template with JSON data for panels.

        Errors:
            Exception: If an error occurs during data retrieval or rendering of the template and
            the user is redirected to the '/' route.
        """
    try:

        if not dir_service.check_path(main_dir_1):
            main_dir_1 = dir_service.get_parent_path(main_dir_1)
        if not dir_service.check_path(main_dir_2):
            main_dir_2 = dir_service.get_parent_path(main_dir_2)

        data = {
            'panel_1': {'path': main_dir_1, 'data': dir_service.get_all_from_path(main_dir_1)},
            'panel_2': {'path': main_dir_2, 'data': dir_service.get_all_from_path(main_dir_2)}
        }

        return render_template('index.html', jsonData=data)
    except Exception as e:
        return redirect(url_for('/'))


@app.route('/goto/<panel_change>/<main_dir_1>/<main_dir_2>/<goto_dir>', methods=["GET"])
def goto_dir(panel_change, main_dir_1, main_dir_2, goto_dir):
    """
          Navigates to a specific directory within a panel and updates the data accordingly.

          This route checks the 'panel_change' parameter to decide which panel needs an update
          based on the 'goto_dir' parameter. It retrieves data for either 'panel_1' or 'panel_2'
          dand updates the paths and data accordingly.
          Renders the 'index.html' template with the constructed JSON data.

          Args:
              panel_change (str): Indicates the panel to update ('panel1' or 'panel2').
              main_dir_1 (str): The path to the directory for 'panel_1'.
              main_dir_2 (str): The path to the directory for 'panel_2'.
              goto_dir (str): The directory to navigate within the panel.

          :return: HTML content rendered from 'index.html' template with updated JSON data for panels.

          Errors:
              Exception: If an error occurs during data retrieval, the user is redirected to the 'goto' route.
       """
    try:

        data = {'panel_1': {}, 'panel_2': {}}

        if panel_change == "panel1":
            new_main_dir_1, elements_panel1 = dir_service.get_all_from_dir(main_dir_1, goto_dir)
            data['panel_1'] = {'path': new_main_dir_1, 'data': elements_panel1}
            data['panel_2'] = {'path': main_dir_2, 'data': dir_service.get_all_from_path(main_dir_2)}
        else:
            new_main_dir_2, elements_panel2 = dir_service.get_all_from_dir(main_dir_2, goto_dir)
            data['panel_1'] = {'path': main_dir_1, 'data': dir_service.get_all_from_path(main_dir_1)}
            data['panel_2'] = {'path': new_main_dir_2, 'data': elements_panel2}

        return render_template('index.html', jsonData=data)
    except Exception as e:
        print(e)
        return redirect(url_for('goto', main_dir_1=main_dir_1, main_dir_2=main_dir_2))


@app.route('/rename/<main_dir_1>/<main_dir_2>/<old_name_path>/<new_name_path>', methods=["PUT"])
def rename(main_dir_1, main_dir_2, old_name_path, new_name_path):
    """
       Renames a file or directory within the specified directories.

       Args:
           main_dir_1 (str): The path to the directory where the file or directory exists for 'panel_1'.
           main_dir_2 (str): The path to the directory where the file or directory exists for 'panel_2'.
           old_name_path (str): The old name or path of the file or directory.
           new_name_path (str): The new name or path to rename the file or directory.

       :return dict: A JSON response indicating the success or failure of the renaming operation.
               - {'ok': True, 'message': 'Data received successfully'} if successful.
               - {'ok': False, 'message': 'Error message'} if an error occurs.
        """
    try:
        dir_service.rename(old_name_path, new_name_path)
    except Exception as e:
        print(e)
        return jsonify({'ok': False, 'message': str(e)})
    return jsonify({'ok': True, 'message': 'Data received successfully'})


@app.route('/copy/<main_dir_from_copy>/<main_dir_to_copy>', methods=["POST"])
def copy(main_dir_from_copy, main_dir_to_copy):
    """
   Copies files or directories from one location to another.

       This route is responsible for copying files or directories from 'main_dir_from_copy'
       to 'main_dir_to_copy'

   Args:
       main_dir_from_copy (str): The source directory path from where files or directories will be copied.
       main_dir_to_copy (str): The destination directory path to where files or directories will be copied.

   Body:
       elements (list): A list of files or directories to be copied.

   :return:
      dict: A JSON response indicating the success or failure of the copying operation.
          - {'ok': True, 'message': 'Data received successfully'} if successful.
              - {'ok': False, 'message': 'Error message'} if an error occurs.
          """
    if request.method == 'POST':

        if main_dir_to_copy == main_dir_from_copy:
            return jsonify({'ok': False, 'message': 'Invalid request, same directory'})

        data = request.get_json()
        elements_to_copy = data.get('elements', [])

        print(elements_to_copy)
        print(main_dir_from_copy, main_dir_to_copy)
        try:
            file_service.copy_all(main_dir_from_copy, main_dir_to_copy, elements_to_copy, replace=True,
                                  delete_after=False, initial_dir=main_dir_from_copy)
        except Exception as e:
            print(e)
            return jsonify({'ok': False, 'message': str(e)})
    return jsonify({'ok': True, 'message': 'Data received successfully'})


@app.route('/move/<main_dir_from_move>/<main_dir_to_move>', methods=["POST"])
def move(main_dir_from_move, main_dir_to_move):
    """
       Copies files or directories from one location to another.

           This route is responsible for moving files or directories from 'main_dir_from_copy'
           to 'main_dir_to_copy'.

       Args:
           main_dir_from_copy (str): The source directory path from where files or directories will be moved.
           main_dir_to_copy (str): The destination directory path to where files or directories will be moved.

       Body:
           elements (list): A list of files or directories to be moved.

       :return:
          dict: A JSON response indicating the success or failure of the moving operation.
              - {'ok': True, 'message': 'Data received successfully'} if successful.
                  - {'ok': False, 'message': 'Error message'} if an error occurs.
          """
    if main_dir_to_move == main_dir_from_move:
        return jsonify({'ok': False, 'message': 'Invalid request, same directory'})

    data = request.get_json()
    print(data)
    print(data)
    elements_to_move = data.get('elements', [])

    print(elements_to_move)
    print(main_dir_from_move, main_dir_to_move)
    try:
        file_service.copy_all(main_dir_from_move, main_dir_to_move, elements_to_move, replace=True,
                              delete_after=True, initial_dir=main_dir_from_move)
    except Exception as e:
        print("Exception: ", e)
        return jsonify({'ok': False, 'message': str(e)})

    return jsonify({'ok': True, 'message': 'Data received successfully'})


@app.route('/delete/<main_dir_delete>', methods=["DELETE"])
def delete(main_dir_delete):
    """
         Deletes files or directories from the specified directory.

            This route is responsible for deleting files or directories from 'main_dir_delete'.
            It receives a DELETE request containing a JSON payload with 'elements' to be deleted.

        Args:
            main_dir_delete (str): The directory path from where files or directories will be deleted.

        Body:
            elements (list): A list of files or directories to be deleted.

        :return:
            dict: A JSON response indicating the success or failure of the deleting operation.
                - {'ok': True, 'message': 'Data received successfully'} if successful.
                - {'ok': False, 'message': 'Error message'} if an error occurs.

    """
    print(main_dir_delete)
    data = request.get_json()
    elements_to_delete = data.get('elements', [])
    print(elements_to_delete)
    print(main_dir_delete)
    try:
        file_service.delete_all(main_dir_delete, elements_to_delete)
    except Exception as e:
        print(e)
        return jsonify({'ok': False, 'message': str(e)})
    return jsonify({'ok': True, 'message': 'Data received successfully'})


# return jsonify({'error': 'Invalid request'})

@app.route('/create/file/<dir>/<file_name>', methods=["POST"])
def create_file(dir, file_name):
    """
    Creates a new file within the specified directory.

        This route is responsible for creating a new file named 'file_name'
        within the directory specified by 'dir'.

    Args:
        dir (str): The path to the directory where the new file will be created.
        file_name (str): The name of the new file to be created.

    :return:
        dict: A JSON response indicating the success or failure of the file creation operation.
        - {'ok': True, 'message': 'Data received successfully'} if successful.
        - {'ok': False, 'message': 'Error message'} if an error occurs.
    """
    print(dir)
    print(file_name)
    try:
        file_service.create_file(dir, file_name)
    except Exception as e:
        print(e)
        return jsonify({'ok': False, 'message': str(e)})
    return jsonify({'ok': True, 'message': 'Data received successfully'})


@app.route('/create/dir/<dir>/<dir_name>', methods=["POST"])
def create_dir(dir, dir_name):
    """
    Creates a new directory within the specified directory.

        This route is responsible for creating a new directory named 'dir_name'
        within the directory specified by 'dir'.

    Args:
        dir (str): The path to the directory where the new directory will be created.
        dir_name (str): The name of the new directory to be created.

    :return:
        dict: A JSON response indicating the success or failure of the directory creation operation.
            - {'ok': True, 'message': 'Data received successfully'} if successful.
            - {'ok': False, 'message': 'Error message'} if an error occurs.

    """
    print(dir)
    print(dir_name)
    try:
        dir_service.create_directory(dir, dir_name)
    except Exception as e:
        print(e)
        return jsonify({'ok': False, 'message': str(e)})
    return jsonify({'ok': True, 'message': 'Data received successfully'})


@app.route('/content/<dir_content>/<file_name>', methods=["GET"])
def get_content(dir_content, file_name):
    """
    Retrieves the content of a specified file within the specified directory.

        This route is responsible for retrieving the content of the file named 'file_name'
        within the directory specified by 'main_dir_content'.

    Args:
        dir_content(str): The path to the directory where the file exists.
        file_name (str): The name of the file for which the content will be retrieved.

    :return:
        dict: A JSON response containing the retrieved content if successful.
            - {'ok': True, 'message': 'Data received successfully', 'content': content} if successful.
            - {'ok': False, 'message': 'Error message'} if an error occurs} if an error occurs.
    """
    print(dir_content)
    print(file_name)
    try:
        content = file_service.get_content(dir_content, file_name)
    except Exception as e:
        print(e)
        return jsonify({'ok': False, 'message': str(e)})
    return jsonify({'ok': True, 'message': 'Data received successfully', 'content': content})


@app.route('/edit/content/<main_dir_content>/<file_name>', methods=["PUT"])
def edit_content(main_dir_content, file_name):
    """
    Modifies the content of a specified file within the specified directory.

        This route is responsible for editing the content of the file named 'file_name'
        within the directory specified by 'main_dir_content'. It receives a PUT request
        containing a JSON payload with the updated 'content' for the file.

    Args:
        main_dir_content (str): The path to the directory where the file exists.
        file_name (str): The name of the file for which the content will be modified.

    :returns:
        dict: A JSON response indicating the success or failure of the content modification operation.
            - {'ok': True, 'message': 'Data received successfully'} if successful.
            - {'ok': False, 'message': 'Error message'} if an error occurs.
    """
    print(main_dir_content)
    print(file_name)
    data = request.get_json()
    content = data.get('content', '')
    try:
        file_service.edit_content(main_dir_content, file_name, content)
    except Exception as e:
        print(e)
        return jsonify({'ok': False, 'message': str(e)})
    return jsonify({'ok': True, 'message': 'Data received successfully'})


if __name__ == '__main__':
    from waitress import serve

    app.config['DEBUG'] = True
    serve(app, host="0.0.0.0", port=8080, debug=True)
