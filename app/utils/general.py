import json
from functools import wraps

from fastapi import Request

from app.core import settings


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

def require_llm(_func):
    @wraps(_func)
    def wrapper(*args, **kwargs):
        if not settings.ENABLE_LLM_CALLS:
            return "LLM calls are disabled"
        return _func(*args, **kwargs)
    return wrapper
