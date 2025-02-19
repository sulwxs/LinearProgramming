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
