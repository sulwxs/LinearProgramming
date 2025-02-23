import requests
import json

api_url = 'http://localhost:5000/solve'

data = {
    'c': [-3, -4],
    'A': [[1, 2], [2, 1]],
    'b': [6, 6]
}
'''c:[3,4],
A:[[1,0,1],[0,1,1]]
b:[4,3,5]
'''

response = requests.post(api_url, json=data)

if response.status_code == 200:
    result = response.json()
    print("求解成功！")
    print("最优解:", result['optimal_solution'])
    print("最小值:", result['optimal_value'])
else:
    print(f"请求失败，状态码: {response.status_code}")
    print("错误信息:", response.json())

def genCSV():
    import numpy as np
    import pandas as pd

    # Dimensions
    n = 7  # Number of variables and constraints

    # Objective function coefficients (c)
    c = np.around(np.random.rand(n)-0.5,3)

    # Coefficients of the constraints (A) - 15 constraints with 15 variables
    A = np.around(np.random.rand(n, n),3)

    # Right-hand side of the constraints (b)
    b = np.around(np.random.rand(n),3)

    # Prepare data for CSV
    data_c = pd.DataFrame(c, columns=['c'])
    data_A = pd.DataFrame(A, columns=[f'A{i + 1}' for i in range(n)])
    data_b = pd.DataFrame(b, columns=['b'])

    # Save to CSV
    file_path_c = './results/objective_function_c.csv'
    file_path_A = './results/constraints_matrix_A.csv'
    file_path_b = './results/constraints_b.csv'

    data_c.to_csv(file_path_c, index=False)
    data_A.to_csv(file_path_A, index=False)
    data_b.to_csv(file_path_b, index=False)

    file_path_c, file_path_A, file_path_b


genCSV()

