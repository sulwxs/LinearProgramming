import logging

from flask import Flask, request, jsonify
from flask_cors import cross_origin, CORS
from scipy.optimize import linprog
import numpy as np

app = Flask(__name__)
CORS(app)
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


if __name__ == '__main__':

    app.run(debug=True)
