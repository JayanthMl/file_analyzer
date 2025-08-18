import json

with open("test.json", "r") as file:
    data = json.load(file)
    for d in data:
        print(d)
        print()
