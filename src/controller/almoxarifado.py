import logging

from flask import make_response

from config import get_config
from controller.api_helper import ApiError, handler_exception, create_response, token_required
from service.almoxarifado import find, get_item, create, update, remove

config = get_config()


@handler_exception
@token_required(tipos=['funcionario'], acessos=['total', 'modificar', 'leitura'], validate_empresa=True)
def search(empresa_id: str, nome: str = None):
    logging.info('Listando Almoxarifados')
    response = find(empresa_id=empresa_id, nome=nome)
    return create_response(response=response, status=200)


@handler_exception
@token_required(tipos=['funcionario'], acessos=['total', 'modificar', 'leitura'], validate_empresa=True)
def get(empresa_id: str, almoxarifado_id: int):
    logging.info('Getting Almoxarifado')
    response = get_item(empresa_id=empresa_id, almoxarifado_id=almoxarifado_id)
    if response:
        return create_response(response=response, status=200)
    else:
        raise ApiError(error_code=404, error_message='Almoxarifado não encontrado')


@handler_exception
@token_required(tipos=['funcionario'], acessos=['total'], validate_empresa=True)
def post(empresa_id: str, body: dict):
    logging.info('Criando Almoxarifado')
    validate_request(body=body)
    body['empresaId'] = empresa_id
    response = create(body=body)
    return create_response(response=response, status=201)


@handler_exception
@token_required(tipos=['funcionario'], acessos=['total', 'modificar'], validate_empresa=True)
def put(empresa_id: str, almoxarifado_id: int, body: dict):
    logging.info('Atualizando Almoxarifado')
    validate_request(body=body)
    body['empresaId'] = empresa_id
    body['id'] = almoxarifado_id
    response = update(body=body)
    return create_response(response=response, status=200)


@handler_exception
@token_required(tipos=['funcionario'], acessos=['total'], validate_empresa=True)
def delete(empresa_id: str, almoxarifado_id: int):
    logging.info('Deletando Almoxarifado')
    response = remove(empresa_id=empresa_id, almoxarifado_id=almoxarifado_id)
    if response:
        return create_response(response={}, status=200)
    else:
        raise ApiError(error_code=404, error_message='Almoxarifado não encontrado')


def options(empresa_id: str):
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, token'
    return response


def options_id(empresa_id: str, almoxarifado_id: int):
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, token'
    return response


def validate_request(body: dict):
    if not body.get('nome') or len(body['nome']) > 50:
        ApiError(error_code=400, error_message='Nome invalido.')
    if body.get('descricao') and len(body['descricao']) > 255:
        ApiError(error_code=400, error_message='Descrição invalida.')
