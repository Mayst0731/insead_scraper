import json


def read_from_json(file_name):
    with open(file_name) as f:
        lst = json.load(f)
    return lst


def write_to_json(lst,file_name):
    with open(file_name, 'w') as cp:
        json.dump(lst, cp,indent=4)



