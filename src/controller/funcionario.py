import logging

from flask import make_response

from config import get_config
from controller.api_helper import ApiError, handler_exception, create_response, token_required
from service.funcionario import find, get_item, create, update, remove

config = get_config()


@handler_exception
@token_required(tipos=['empresa'], validate_empresa=True)
def search(empresa_id: str, nome: str = None):
    logging.info('Listando Funcionarios')
    response = find(empresa_id=empresa_id, nome=nome)
    return create_response(response=response, status=200)


@handler_exception
@token_required(tipos=['empresa'], validate_empresa=True)
def get(empresa_id: str, funcionario_id: int):
    logging.info('Getting Funcionario')
    response = get_item(empresa_id=empresa_id, funcionario_id=funcionario_id)
    if response:
        return create_response(response=response, status=200)
    else:
        raise ApiError(error_code=404, error_message='Funcionario não encontrado')


@handler_exception
@token_required(tipos=['empresa'], validate_empresa=True, validate_situacao=True)
def post(empresa_id: str, body: dict):
    logging.info('Criando Funcionario')
    validate_request(body=body, created=True)
    body['empresaId'] = empresa_id
    response = create(body=body)
    return create_response(response=response, status=201)


@handler_exception
@token_required(tipos=['empresa'], validate_empresa=True)
def put(empresa_id: str, funcionario_id: int, body: dict):
    logging.info('Atualizando Funcionario')
    validate_request(body=body, created=False)
    body['empresaId'] = empresa_id
    body['id'] = funcionario_id
    response = update(body=body)
    return create_response(response=response, status=200)


@handler_exception
@token_required(tipos=['empresa'], validate_empresa=True)
def delete(empresa_id: str, funcionario_id: int):
    logging.info('Deletando Funcionario')
    response = remove(empresa_id=empresa_id, funcionario_id=funcionario_id)
    if response:
        return create_response(response={}, status=200)
    else:
        raise ApiError(error_code=404, error_message='Funcionario não encontrado')


def options(empresa_id: str):
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, token'
    return response


def options_id(empresa_id: str, funcionario_id: int):
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
    if not body.get('acesso') or body['acesso'] not in ['total', 'modificar', 'leitura']:
        ApiError(error_code=400, error_message='Acesso invalido.')
