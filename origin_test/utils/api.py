from collections import OrderedDict

import simplejson
from flask import current_app, make_response
from flask_restplus import Api


def custom_output_json(data, code, headers=None):
    """
    We use this in order to use json as an output for all our APIs without having to worry about it on the code
    """
    settings = current_app.config.get("RESTPLUS_JSON", {})
    if current_app.debug:
        settings.setdefault("indent", 4)
    dumped = simplejson.dumps(data, **settings) + "\n"
    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp


class CustomAPI(Api):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.representations = OrderedDict([("application/json", custom_output_json)])
