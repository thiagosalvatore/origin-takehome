from flask import abort, jsonify, make_response


def badrequest(message="bad request.", **kwargs):
    abort(make_response(jsonify(message=message, **kwargs), 400))
