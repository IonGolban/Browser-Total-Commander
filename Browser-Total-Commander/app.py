from flask import Flask, render_template, request, redirect, url_for, session, flash
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


#
# @app.route('/dir/elements/<path>', methods=["GET"])
# def gat_all_from_dir(path):
#     data = dir_service.get_all_from_dir(path)
#     response_data = dict()
#     response_data['data'] = data
#     response_data['main_dir_name_1'] = path
#     response_data['main_dir_name_2'] = path
#
#     return json.dumps(response_data)

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


@app.route('/rename/<main_dir_1>/<main_dir_2>/<old_name_path>/<new_name_path>', methods=["GET"])
def rename(main_dir_1, main_dir_2, old_name_path, new_name_path):
    dir_service.rename(old_name_path, new_name_path)
    data = dict()
    data['panel_1'] = dict()
    data['panel_2'] = dict()
    data['panel_1']['path'] = main_dir_1
    data['panel_1']['data'] = dir_service.get_all_from_path(main_dir_1)
    data['panel_2']['path'] = main_dir_2
    data['panel_2']['data'] = dir_service.get_all_from_path(main_dir_2)

    return render_template('index.html', jsonData=data)


if __name__ == '__main__':
    from waitress import serve

    app.config['DEBUG'] = True
    serve(app, host="0.0.0.0", port=8080, debug=True)


def format_data(data):
    for key, value in data.items():
        if isinstance(value, dict):
            format_data(value)
        if isinstance(value, list):
            for item in value:
                format_data(item)

        data[key] = str(value)
