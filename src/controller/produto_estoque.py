import logging

from flask import make_response

from config import get_config
from controller.api_helper import ApiError, handler_exception, create_response, token_required
from service.produto_estoque import get_produto_estoque_for_estoque, get_produto_estoque_for_produto

config = get_config()


@handler_exception
@token_required(tipos=['operador'], acessos=['total', 'modificar', 'leitura'], validate_empresa=True)
def search_produto(empresa_id: int, produto_id: int):
    logging.info('Listando estoques do produto')
    response = get_produto_estoque_for_produto(empresa_id=empresa_id, produto_id=produto_id)
    return create_response(response=response, status=200)


@handler_exception
@token_required(tipos=['operador'], acessos=['total', 'modificar', 'leitura'], validate_empresa=True)
def search_estoque(empresa_id: int, estoque_id: int):
    logging.info('Listando produtos do estoque')
    response = get_produto_estoque_for_estoque(empresa_id=empresa_id, estoque_id=estoque_id)
    return create_response(response=response, status=200)


def options_produto(empresa_id: str, produto_id):
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, token'
    return response


def options_estoque(empresa_id: str, estoque_id):
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, token'
    return response
