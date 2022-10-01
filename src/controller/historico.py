import logging

from flask import make_response

from config import get_config
from controller.api_helper import handler_exception, create_response, token_required
from service.historico import find

config = get_config()


@handler_exception
@token_required(tipos=['operador'], acessos=['total', 'modificar', 'leitura'], validate_empresa=True)
def search(empresa_id: int, produto_id: int):
    logging.info('Listando Historico')
    response = find(empresa_id=empresa_id, produto_id=produto_id)
    return create_response(response=response, status=200)


def options_id(empresa_id: str, produto_id: int):
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, token'
    return response
