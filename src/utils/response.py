from flask import jsonify


def json_response(message, status_code=200):
    resp = jsonify(message)
    resp.status_code = status_code
    return resp
