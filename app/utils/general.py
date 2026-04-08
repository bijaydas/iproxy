import json

from fastapi import Request


def pprint(data):
    if type(data) in [dict, list]:
        print(json.dumps(data, indent=4))
    else:
        print(data)

def get_headers(request: Request):
    return {
        "method": request.method,
        "url": request.url.path,
        "params": dict(request.query_params),
        "headers": dict(request.headers),
        "cookies": request.cookies,
    }
