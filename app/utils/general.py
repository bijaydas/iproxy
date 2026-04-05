import json


def pprint(data):
    if type(data) in [dict, list]:
        print(json.dumps(data, indent=4))
    else:
        print(data)