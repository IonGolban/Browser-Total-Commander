from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from services import dir_service, file_service
import json

app = Flask(__name__)

my_test_dir = r"C:\Users\Public\Desktop\garb_files"


@app.route('/')
def init_page():
    # start_dir_name = dir_service.get_start_dir()
    data = dir_service.get_all_from_path(my_test_dir)
    response_data = dict()
    response_data['panel_1'] = dict()
    response_data['panel_2'] = dict()
    response_data['panel_1']['path'] = my_test_dir
    response_data['panel_2']['path'] = my_test_dir
    response_data['panel_1']['data'] = data
    response_data['panel_2']['data'] = data

    print(response_data)
    return render_template('index.html', jsonData=response_data)


@app.route('/goto/<panel_change>/<main_dir_1>/<main_dir_2>/<goto_dir>', methods=["GET"])
def goto(panel_change, main_dir_1, main_dir_2, goto_dir):
    print(panel_change, main_dir_1, main_dir_2, goto_dir)
    data = dict()
    data['panel_1'] = dict()
    data['panel_2'] = dict()

    if panel_change == "panel1":
        new_main_dir_1, elements_panel1 = dir_service.get_all_from_dir(main_dir_1, goto_dir)
        print(new_main_dir_1, elements_panel1)
        data['panel_1']['path'] = new_main_dir_1
        data['panel_1']['data'] = elements_panel1
        data['panel_2']['path'] = main_dir_2
        data['panel_2']['data'] = dir_service.get_all_from_path(main_dir_2)
    else:
        new_main_dir_2, elements_panel2 = dir_service.get_all_from_dir(main_dir_2, goto_dir)
        data['panel_1']['path'] = main_dir_1
        data['panel_1']['data'] = dir_service.get_all_from_path(main_dir_1)
        data['panel_2']['path'] = new_main_dir_2
        data['panel_2']['data'] = elements_panel2

    return render_template('index.html', jsonData=data)


@app.route('/goto/<main_dir_1>/<main_dir_2>/', methods=["GET"])
def goto_root(main_dir_1, main_dir_2):
    print(main_dir_1, main_dir_2)
    data = dict()
    data['panel_1'] = dict()
    data['panel_2'] = dict()

    data['panel_1']['path'] = main_dir_1
    data['panel_1']['data'] = dir_service.get_all_from_path(main_dir_1)
    data['panel_2']['path'] = main_dir_2
    data['panel_2']['data'] = dir_service.get_all_from_path(main_dir_2)

    return render_template('index.html', jsonData=data)


@app.route('/rename/<main_dir_1>/<main_dir_2>/<old_name_path>/<new_name_path>', methods=["PUT"])
def rename(main_dir_1, main_dir_2, old_name_path, new_name_path):
    try:
        dir_service.rename(old_name_path, new_name_path)
    except Exception as e:
        print(e)
        return jsonify({'ok': False, 'message': str(e)})
    return jsonify({'ok': True, 'message': 'Data received successfully'})


@app.route('/copy/<main_dir_from_copy>/<main_dir_to_copy>', methods=["POST"])
def copy(main_dir_from_copy, main_dir_to_copy):
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
    print(main_dir_delete)
    data = request.get_json()
    elements_to_delete = data.get('elements', [])
    print(elements_to_delete)
    print(main_dir_delete)
    try:
        file_service.delete(main_dir_delete, elements_to_delete)
    except Exception as e:
        print(e)
        return jsonify({'ok': False, 'message': str(e)})
    return jsonify({'ok': True, 'message': 'Data received successfully'})


# return jsonify({'error': 'Invalid request'})

@app.route('/create/file/<main_dir_create>/<file_name>', methods=["POST"])
def create_file(main_dir_create, file_name):
    print(main_dir_create)
    print(file_name)
    try:
        file_service.create_file(main_dir_create, file_name)
    except Exception as e:
        print(e)
        return jsonify({'ok': False, 'message': str(e)})
    return jsonify({'ok': True, 'message': 'Data received successfully'})


@app.route('/create/dir/<main_dir_create>/<dir_name>', methods=["POST"])
def create_dir(main_dir_create, dir_name):
    print(main_dir_create)
    print(dir_name)
    try:
        dir_service.create_directory(main_dir_create, dir_name)
    except Exception as e:
        print(e)
        return jsonify({'ok': False, 'message': str(e)})
    return jsonify({'ok': True, 'message': 'Data received successfully'})


@app.route('/content/<main_dir_content>/<file_name>', methods=["GET"])
def get_content(main_dir_content, file_name):
    print(main_dir_content)
    print(file_name)
    try:
        content = file_service.get_content(main_dir_content, file_name)
    except Exception as e:
        print(e)
        return jsonify({'ok': False, 'message': str(e)})
    return jsonify({'ok': True, 'message': 'Data received successfully', 'content': content})


@app.route('/edit/content/<main_dir_content>/<file_name>', methods=["PUT"])
def edit_content(main_dir_content, file_name):
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
