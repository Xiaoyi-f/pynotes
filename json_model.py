import json

data = {"name": "小明", "age": 18, "hobbies": ["篮球", "游戏"]}
json_str = json.dumps(data, ensure_ascii=False)
print(json_str)

data_py = json.loads(json_str)
print(data_py["name"], type(data_py))

with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

# with块的作用域归属于外一层作用域
with open("data.json", "r", encoding="utf-8") as file:
    py_data = json.load(file)

print(py_data)
