import logging

from flask import make_response

from config import get_config
from controller.api_helper import ApiError, handler_exception, create_response, token_required
from service.operador import find, get_item, create, update, update_senha, remove

config = get_config()


@handler_exception
@token_required(tipos=['empresa'], validate_empresa=True)
def search(empresa_id: int, nome: str = None):
    logging.info('Listando Operadores')
    response = find(empresa_id=empresa_id, nome=nome)
    return create_response(response=response, status=200)


@handler_exception
@token_required(tipos=['empresa'], validate_empresa=True)
def get(empresa_id: int, operador_id: int):
    logging.info('Getting Operador')
    response = get_item(empresa_id=empresa_id, operador_id=operador_id)
    if response:
        return create_response(response=response, status=200)
    else:
        raise ApiError(error_code=404, error_message='Operador não encontrado')


@handler_exception
@token_required(tipos=['empresa'], validate_empresa=True, validate_situacao=True)
def post(empresa_id: int, body: dict):
    logging.info('Criando Operador')
    validate_request(body=body, created=True)
    body['empresaId'] = empresa_id
    response = create(body=body)
    return create_response(response=response, status=201)


@handler_exception
@token_required(tipos=['empresa'], validate_empresa=True)
def put(empresa_id: int, operador_id: int, body: dict):
    logging.info('Atualizando Operador')
    validate_request(body=body, created=False)
    body['empresaId'] = empresa_id
    body['id'] = operador_id
    response = update(body=body)
    return create_response(response=response, status=200)


@handler_exception
@token_required(tipos=['operador'], validate_operador=True)
def patch(empresa_id: int, operador_id: int, body: dict):
    logging.info('Atualizando senha Operador')
    if not body.get('senha') or len(body['senha']) > 50:
        ApiError(error_code=400, error_message='Senha invalida.')
    body['empresaId'] = empresa_id
    body['id'] = operador_id
    response = update_senha(body=body)
    return create_response(response=response, status=200)


@handler_exception
@token_required(tipos=['empresa'], validate_empresa=True)
def delete(empresa_id: int, operador_id: int):
    logging.info('Deletando Operador')
    response = remove(empresa_id=empresa_id, operador_id=operador_id)
    if response:
        return create_response(response={}, status=200)
    else:
        raise ApiError(error_code=404, error_message='Operador não encontrado')


def options(empresa_id: str):
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, token'
    return response


def options_id(empresa_id: str, operador_id: int):
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, token'
    return response


def validate_request(body: dict, created: bool):
    if created:
        if not body.get('senha') or len(body['senha']) > 50:
            ApiError(error_code=400, error_message='Senha invalida.')
    else:
        if body.get('senha') and len(body['senha']) > 50:
            ApiError(error_code=400, error_message='Senha invalida.')
    if not body.get('nomeUsuario') or len(body['nomeUsuario']) > 50:
        ApiError(error_code=400, error_message='NomeUsuario invalido.')
    if not body.get('tipoAcesso') or body['tipoAcesso'] not in ['total', 'modificar', 'leitura']:
        ApiError(error_code=400, error_message='TipoAcesso invalido.')
