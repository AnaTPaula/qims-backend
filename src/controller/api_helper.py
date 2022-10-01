import logging
from datetime import datetime
from json import dumps

import jwt
from flask import make_response, abort, request
from werkzeug.exceptions import HTTPException

from config import get_config

config = get_config()


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
        except ApiError as api_error:
            raise api_error
        except Exception as ex:
            logging.error(ex)
            raise ApiError()
        return response

    return wrapper


def token_required(tipos: list = None, acessos: list = None, validate_empresa: bool = None,
                   validate_situacao: bool = None, validate_operador: bool = None, get_tipo: bool = False,
                   get_id: bool = False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            payload = validate_auth_token(jwt_payload=request.headers.get('token'),
                                          tipos=tipos,
                                          acessos=acessos,
                                          validate_empresa=validate_empresa,
                                          validate_situacao=validate_situacao,
                                          validate_operador=validate_operador,
                                          kwargs=kwargs)
            if get_tipo:
                kwargs['tipo'] = payload['tipo']
            if get_id:
                kwargs['usuario_id'] = payload['id']
            response = func(*args, **kwargs)
            return response

        return wrapper

    return decorator


def validate_auth_token(jwt_payload,
                        tipos,
                        validate_empresa,
                        acessos,
                        validate_situacao,
                        validate_operador,
                        kwargs):
    try:
        payload = jwt.decode(jwt_payload, config.secret, algorithms=['HS256', ])
        timestamp = int(datetime.utcnow().timestamp())
        if timestamp > payload['exp']:
            raise ApiError(error_code=401, error_message='Token expirado.')
        if tipos and payload['tipo'] not in tipos:
            raise ApiError(error_code=401, error_message='Não autorizado.')
        if validate_empresa and payload['tipo'] != 'administrador' and \
                payload.get('empresa', payload.get('id')) != int(kwargs['empresa_id']):
            raise ApiError(error_code=401, error_message='Não autorizado.')
        if validate_situacao and payload.get('situacao') not in ['APROVADO']:
            raise ApiError(error_code=401, error_message='Não autorizado.')
        if acessos and payload['acesso'] not in acessos:
            raise ApiError(error_code=401, error_message='Não autorizado.')
        if validate_operador and payload['tipo'] == 'operador' and payload['id'] != int(kwargs['operador_id']):
            raise ApiError(error_code=401, error_message='Não autorizado.')

        return payload
    except Exception as ex:
        logging.error(ex)
        raise ApiError(error_code=401, error_message='Não autorizado.')
