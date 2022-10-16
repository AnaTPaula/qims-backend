import logging

from flask import make_response

from config import get_config
from controller.api_helper import handler_exception, create_response, token_required
from service.estatistica import get_info

config = get_config()


@handler_exception
@token_required(tipos=['empresa'], validate_empresa=True)
def search(empresa_id: int, body: dict):
    logging.info('Getting informações da conta')
    response = get_info(empresa_id=empresa_id)
    return create_response(response=response, status=200)


def options_id(empresa_id: str):
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, token'
    return response
