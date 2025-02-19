import logging
import os

from flask import Flask, request, jsonify
from flask_cors import cross_origin, CORS
from scipy.optimize import linprog
import numpy as np

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'csv'}
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
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return jsonify({"message": "success"}), 200

    return jsonify({"error": "Invalid file type"}), 400

@app.route('/getfilelist', methods=['GET'])
def get_files():
    return jsonify( [{"name": file, "status": "成功", "progress": 100 } for file in os.listdir(app.config['UPLOAD_FOLDER'])]),200
    # return jsonify({"error": "error"}), 400

@app.route('/delete', methods=['GET'])
def delete_file():
    filename = request.args.get('filename', default='', type=str)
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

if __name__ == '__main__':

    app.run(debug=True)
