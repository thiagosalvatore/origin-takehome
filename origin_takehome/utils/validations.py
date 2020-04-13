from functools import wraps

from flask import request
from marshmallow import Schema
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest

from origin_takehome.utils.responses import badrequest


def check_body(schema):
    def real_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            application_json = "application/json"

            content_type = request.content_type

            if content_type != application_json:
                msg = f'Content-Type must be "{application_json}"'
                return badrequest(msg)

            try:
                r_json = request.get_json()
            except BadRequest:
                r_json = {}

            serial = schema if isinstance(schema, Schema) else schema()
            try:
                document = serial.load(r_json)
                kwargs["data"] = document
            except ValidationError as e:
                return badrequest(e.messages)

            return func(*args, **kwargs)

        return wrapper

    return real_decorator
