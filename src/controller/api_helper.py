import logging
from json import dumps

from flask import make_response, abort
from werkzeug.exceptions import HTTPException


def create_response(response: dict, status: int):
    response = make_response(dumps(response), status)
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:4200'
    response.headers['Access-Control-Allow-Credentials'] = True
    return response


class ApiError(Exception):
    def __init__(self, error_code: int = 500, error_message: str = None):
        abort(error_code, description=error_message)


def handler_exception(func):
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except HTTPException as http_exception:
            raise http_exception
        except Exception as ex:
            logging.error(ex)
            raise ApiError()
        return response

    return wrapper
