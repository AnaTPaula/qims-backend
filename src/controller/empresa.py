import logging

from flask import make_response

from config import get_config
from controller.api_helper import ApiError, handler_exception
from controller.api_helper import create_response
from service.empresa import find, get_item, create, update, remove

config = get_config()


@handler_exception
def search():
    logging.info('Listando Empresas')
    response = find()
    return create_response(response=response, status=200)


@handler_exception
def get(empresa_id: int):
    logging.info('Getting Empresa')
    response = get_item(empresa_id=empresa_id)
    if response:
        return create_response(response=response, status=200)
    else:
        raise ApiError(error_code=404, error_message='Empresa não encontrada')


@handler_exception
def post(body: dict):
    logging.info('Criando Empresa')
    response = create(body=body)
    return create_response(response=response, status=201)


@handler_exception
def put(empresa_id: int, body: dict):
    logging.info('Atualizando Empresa')
    body['id'] = empresa_id
    response = update(body=body)
    return create_response(response=response, status=200)


@handler_exception
def delete(empresa_id: int):
    logging.info('Deletando Empresa')
    response = remove(empresa_id=empresa_id)
    if response:
        return create_response(response={}, status=200)
    else:
        raise ApiError(error_code=404, error_message='Empresa não encontrada')


def options(conta: str):
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type'
    return response


def options_id(conta: str, empresa_id: int):
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type'
    return response
