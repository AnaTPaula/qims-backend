import logging

from flask import make_response
from controller.api_helper import ApiError

from config import get_config
from controller.api_helper import handler_exception, create_response
from service.usuario import validate_access

config = get_config()


@handler_exception
def login(body: dict):
    logging.info('Autenticando usuario.')
    validate_request(body=body)
    response = validate_access(body=body)
    api_response = create_response(response=response['usuario'], status=200)
    api_response.headers['Token'] = response['token']
    api_response.headers['Access-Control-Expose-Headers'] = '*, Token'
    return api_response


def options():
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, Token'
    response.headers['Access-Control-Expose-Headers'] = '*, Token'
    return response


def validate_request(body: dict):
    if not body.get('tipo') or not body.get('senha') or not body.get('nomeUsuario'):
        ApiError(error_code=400, error_message='Campos invalidos.')
    if body['tipo'] not in ['administrador', 'empresa', 'operador']:
        ApiError(error_code=400, error_message='Tipo invalido.')
    if body['tipo'] == 'operador' and not body.get('nomeEmpresa'):
        ApiError(error_code=400, error_message='Nome da empresa invalida.')
    if len(body['senha']) > 50:
        ApiError(error_code=400, error_message='Senha ou nome de usuário invalida.')
    if len(body['nomeUsuario']) > 50:
        ApiError(error_code=400, error_message='Nome usuario invalido.')
