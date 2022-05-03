from json import dumps

from flask import make_response


def create_response(response: dict, status: int):
    response = make_response(dumps(response), status)
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:4200'
    response.headers['Access-Control-Allow-Credentials'] = True
    return response
