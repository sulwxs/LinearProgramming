import logging
import os
import re
import shutil
import time

import pandas as pd
from flask import Flask, request, jsonify, make_response, send_from_directory
from flask_cors import cross_origin, CORS
from pandas import DataFrame
from scipy.optimize import linprog
import numpy as np
import pandas
app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'csv'}
matrixs={}
filelists:DataFrame=None
@app.route("/")
def index():
    return "hello world"

@app.route('/solve', methods=['POST'])
def solve_lp():
    try:
        data = request.get_json()
        print(data)
        c = np.array(data['c'])
        A = np.array(data['A'])
        b = np.array(data['b'])

        result = linprog(c, A_ub=A, b_ub=b, method='highs')

        if result.success:
            return jsonify({
                'status': 'success',
                'optimal_value': result.fun,
                'optimal_solution': result.x.tolist()
            })
        else:
            return jsonify({
                'status': 'error',
                'message': result.message
            }), 400

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def sanitize_filename(filename: str) -> str:
    # 使用正则表达式仅保留字母、数字、下划线和连字符
    sanitized_filename = re.sub(r'[^a-zA-Z0-9_\-\.]', '', filename)
    return sanitized_filename



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        global filelists  # 确保对 DataFrame 进行全局修改
        existing_index = filelists.index[filelists['name'] == file.filename].tolist()

        if existing_index:
            # 如果文件已存在，则更新别名
            filelists.at[existing_index[0], 'alias'] = file.filename
        else:
            # 否则新增记录
            filelists.loc[len(filelists.index)] = [file.filename, file.filename]

        # 保存文件到服务器
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # **写入 CSV 以持久化存储**
        filelists.to_csv('filealias.csv', index=False)

        return jsonify({"message": "success"}), 200

    return jsonify({"error": "Invalid file type"}), 400

@app.route('/getfilelist', methods=['GET'])
def get_files():
    filename = os.path.join('.', 'filealias.csv')
    global filelists
    filelists=pd.read_csv(filename)
    return jsonify( [{"name": row.name,"alias": row.alias,"show":True,"read":False, "status": "success", "progress": 100 } for row in filelists.itertuples()]),200
    # return jsonify({"error": "error"}), 400

@app.route('/delete', methods=['GET'])
def delete_file():
    filename = request.args.get('filename', default='', type=str)
    filename=sanitize_filename(filename)
    if filename == '':
        return jsonify({"error": "没有这个文件"}), 400

    if allowed_file(filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filename):
            os.remove(filename)

        else:
            return jsonify({"error": "没有这个文件"}), 400
        return jsonify({"success": "ok"}), 200

    return jsonify({"error": "没有这个文件"}), 400


@app.route('/copy', methods=['GET'])
def copy_file():
    filename = request.args.get('filename', default='', type=str)

    if filename == '':
        return jsonify({"error": "没有这个文件"}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if os.path.exists(filepath):
        file_name_part, file_extension = os.path.splitext(filename)

        # 生成递增的副本文件名
        counter = 1
        while True:
            new_filename = f"{file_name_part}_{counter}{file_extension}"
            new_filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            if not os.path.exists(new_filepath):  # 找到一个不存在的文件名
                break
            counter += 1

        shutil.copy(filepath, new_filepath)
        return jsonify({"success": "ok", "file": {"name": new_filename,"alias": new_filename,"show":True,"read":False, "status": "success", "progress": 100 }}), 200
    else:
        return jsonify({"error": "没有这个文件"}), 400






@app.route('/rename', methods=['GET'])
def rename_file():
    filename = os.path.join('.', 'filealias.csv')
    global filelists
    filelists = pd.read_csv(filename)
    filename = request.args.get('filename', default='', type=str)
    file_new_alias = request.args.get('alias', default='', type=str)

    if not filename or not file_new_alias:
        return jsonify({"error": "参数错误"}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(filepath):
        return jsonify({"error": "文件不存在"}), 400




    if filename not in filelists['name'].values:
        return jsonify({"error": "文件未在 alias 列表中登记"}), 400

    filelists.loc[filelists['name'] == filename, 'alias'] = file_new_alias

    # **写回 CSV**
    filelists.to_csv('filealias.csv', index=False)

    return jsonify({"success": "ok"}), 200
@app.route('/download', methods=['GET'])
def download_file():
    filename = request.args.get('filename', default='', type=str)
    if filename == '':
        return jsonify({"error": "没有这个文件"}), 400
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "没有这个文件"}), 400
    response = make_response(
            send_from_directory(app.config['UPLOAD_FOLDER'], filename.encode('utf-8').decode('utf-8'), as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response






@app.route('/read_csv_matrix', methods=['GET'])
def read_csv_matrix():
    try:
        global matrixs
        filename = request.args.get('filename', default='', type=str)
        filename = sanitize_filename(filename)
        path='./uploads/' + filename
        if not os.path.exists(path):
            return jsonify({"error": "No such file"}), 400

        df = pd.read_csv(path)
        matrix = df.values.tolist()
        matrixs[filename]=matrix
        return jsonify({"matrix": matrix}),200
    except Exception as e:
        return jsonify({"error": f"{filename}文件格式错误，请检查后重新上传"}), 400




if __name__ == '__main__':

    app.run(debug=True)
