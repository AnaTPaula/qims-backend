import logging

from flask import make_response

from config import get_config
from controller.api_helper import ApiError, handler_exception
from controller.api_helper import create_response
from service.funcionario import find, get_item, create, update, remove

config = get_config()


@handler_exception
def search(empresa_id: str):
    logging.info('Listando Funcionarios')
    response = find(empresa_id=empresa_id)
    return create_response(response=response, status=200)


@handler_exception
def get(empresa_id: str, funcionario_id: int):
    logging.info('Getting Funcionario')
    response = get_item(empresa_id=empresa_id, funcionario_id=funcionario_id)
    if response:
        return create_response(response=response, status=200)
    else:
        raise ApiError(error_code=404, error_message='Funcionario não encontrado')


@handler_exception
def post(empresa_id: str, body: dict):
    logging.info('Criando Funcionario')
    body['empresa_id'] = empresa_id
    response = create(body=body)
    return create_response(response=response, status=201)


@handler_exception
def put(empresa_id: str, funcionario_id: int, body: dict):
    logging.info('Atualizando Funcionario')
    body['empresa_id'] = empresa_id
    body['id'] = funcionario_id
    response = update(body=body)
    return create_response(response=response, status=200)


@handler_exception
def delete(empresa_id: str, funcionario_id: int):
    logging.info('Deletando Funcionario')
    response = remove(empresa_id=empresa_id, funcionario_id=funcionario_id)
    if response:
        return create_response(response={}, status=200)
    else:
        raise ApiError(error_code=404, error_message='Funcionario não encontrado')


def options(conta: str):
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type'
    return response


def options_id(conta: str, funcionario_id: int):
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type'
    return response
