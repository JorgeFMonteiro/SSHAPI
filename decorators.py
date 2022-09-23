# TOOO: Harden this so if does not die if input params are completely incorrect
from functools import wraps

from flask import request, abort

from config import TOKEN


def check_input(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        input_params = ["user", "password", "host", "command"]
        request_dict = request.json
        for input_param in input_params:
            if request_dict.get(input_param) is None or request_dict.get(input_param) == "":
                #TODO: Should we return 403 here?
                return abort(403, description="Input parameter {parameter} is missing or incorrect".format(parameter=input_param))
        return f(*args, **kwargs)
    return decorated_function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request_token = request.headers.get('Token')
        if request_token is None or request_token != TOKEN:
            # TODO: Better error
            return  abort(403, description="Incorrect Token")
        return f(*args, **kwargs)
    return decorated_function