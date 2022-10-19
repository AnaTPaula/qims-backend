import logging

from flask import make_response

from config import get_config
from controller.api_helper import ApiError, handler_exception, create_response, token_required
from service.administrador import get_item, update

config = get_config()


@handler_exception
@token_required(tipos=['administrador'])
def get(administrador_id: int):
    logging.info('Getting Administrador')
    response = get_item(administrador_id=administrador_id)
    if response:
        return create_response(response=response, status=200)
    else:
        raise ApiError(error_code=404, error_message='Dado não encontrado')


@handler_exception
@token_required(tipos=['administrador'])
def put(administrador_id: int, body: dict):
    logging.info('Atualizando Administrador')
    validate_request(body=body, created=False)
    body['id'] = administrador_id
    response = update(body=body)
    return create_response(response=response, status=200)


def options_id(administrador_id: int):
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, token'
    return response


def validate_request(body: dict, created: bool):
    if created:
        if not body.get('senha') or len(body['senha']) > 50:
            ApiError(error_code=400, error_message='Senha inválida.')
    else:
        if body.get('senha') and len(body['senha']) > 50:
            ApiError(error_code=400, error_message='Senha inválida.')
    if not body.get('nomeUsuario') or len(body['nomeUsuario']) > 50:
        ApiError(error_code=400, error_message='Nome Usuário inválido.')
