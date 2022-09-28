import logging

from flask import make_response

from config import get_config
from controller.api_helper import ApiError, handler_exception, create_response, token_required
from service.produto import find, create, update, remove, get_item

config = get_config()


@handler_exception
@token_required(tipos=['operador'], acessos=['total', 'modificar', 'leitura'], validate_empresa=True)
def search(empresa_id: str, nome: str = None):
    logging.info('Listando Produtos')
    response = find(empresa_id=empresa_id, nome=nome)
    return create_response(response=response, status=200)


@handler_exception
@token_required(tipos=['operador'], acessos=['total', 'modificar', 'leitura'], validate_empresa=True)
def get(empresa_id: str, produto_id: int, nome: str):
    logging.info('Getting Produto')
    response = get_item(empresa_id=empresa_id, produto_id=produto_id, nome=nome)
    if response:
        return create_response(response=response, status=200)
    else:
        raise ApiError(error_code=404, error_message='Almoxarifado não encontrado')


@handler_exception
@token_required(tipos=['operador'], acessos=['total'], validate_empresa=True)
def post(empresa_id: str, body: dict):
    logging.info('Criando Produto')
    validate_request(body=body)
    body['empresaId'] = empresa_id
    response = create(body=body)
    return create_response(response=response, status=201)


@handler_exception
@token_required(tipos=['operador'], acessos=['total', 'modificar'], validate_empresa=True)
def put(empresa_id: str, produto_id: int, body: dict):
    logging.info('Atualizando Produto')
    validate_request(body=body)
    body['empresaId'] = empresa_id
    body['id'] = produto_id
    response = update(body=body)
    return create_response(response=response, status=200)


@handler_exception
@token_required(tipos=['operador'], acessos=['total'], validate_empresa=True)
def delete(empresa_id: str, produto_id: int, nome: str):
    logging.info('Deletando Produto')
    response = remove(empresa_id=empresa_id, id=produto_id, nome=nome)
    if response:
        return create_response(response={}, status=200)
    else:
        raise ApiError(error_code=404, error_message='Produto não encontrado')


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