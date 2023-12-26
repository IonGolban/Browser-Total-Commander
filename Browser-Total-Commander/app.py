from flask import Flask, render_template, request, redirect, url_for, session, flash
from services import dir_service, file_service
import json

app = Flask(__name__)


@app.route('/')
def init_page():
    main_dir_name = dir_service.get_main_dir()
    data = dir_service.get_all_from_dir(main_dir_name)
    response_data = dict()
    response_data['data'] = data
    response_data['main_dir_name'] = main_dir_name
    print(response_data)
    return render_template('index.html', jsonData=response_data)


@app.route('/dir/elements/<path>', methods=["GET"])
def gat_all_from_dir(path):
    data = dir_service.get_all_from_dir(path)
    response_data = dict()
    response_data['data'] = data
    response_data['main_dir_name'] = path

    return json.dumps(response_data)


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
