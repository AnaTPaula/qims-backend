import logging

from flask import make_response

from config import get_config
from controller.api_helper import ApiError, handler_exception, create_response, token_required
from service.lote import find, get_item, create, update, remove

config = get_config()


@handler_exception
@token_required(tipos=['operador'], acessos=['total', 'modificar', 'leitura'], validate_empresa=True)
def search(empresa_id: int, codigo_lote: str = None):
    logging.info('Listando Lotes')
    response = find(empresa_id=empresa_id, codigo_lote=codigo_lote)
    return create_response(response=response, status=200)


@handler_exception
@token_required(tipos=['operador'], acessos=['total', 'modificar', 'leitura'], validate_empresa=True)
def get(empresa_id: int, lote_id: int):
    logging.info('Getting Lote')
    response = get_item(empresa_id=empresa_id, lote_id=lote_id)
    if response:
        return create_response(response=response, status=200)
    else:
        raise ApiError(error_code=404, error_message='Lote não encontrado')


@handler_exception
@token_required(tipos=['operador'], acessos=['total'], validate_empresa=True)
def post(empresa_id: int, body: dict):
    logging.info('Criando Lote')
    validate_request(body=body)
    body['empresaId'] = empresa_id
    response = create(body=body)
    return create_response(response=response, status=201)


@handler_exception
@token_required(tipos=['operador'], acessos=['total', 'modificar'], validate_empresa=True)
def put(empresa_id: int, lote_id: int, body: dict):
    logging.info('Atualizando Produto')
    validate_request(body=body)
    body['empresaId'] = empresa_id
    body['id'] = lote_id
    response = update(body=body)
    return create_response(response=response, status=200)


@handler_exception
@token_required(tipos=['operador'], acessos=['total'], validate_empresa=True)
def delete(empresa_id: int, lote_id: int):
    logging.info('Deletando Lote')
    response = remove(empresa_id=empresa_id, lote_id=lote_id)
    return create_response(response=response, status=200)


def options(empresa_id: str):
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, token'
    return response


def options_id(empresa_id: str, lote_id: int):
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, token'
    return response


def validate_request(body: dict):
    if not body.get('dataEntrada') or body.get('dataEntrada') < 0:
        ApiError(error_code=400, error_message='Data entrada inválidas.')
    if body.get('dataValidade') and body.get('dataValidade') < 0:
        ApiError(error_code=400, error_message='Data Validade inválida.')
    if not body.get('codigoLote') or len(body['codigoLote']) > 100:
        ApiError(error_code=400, error_message='Código inválido.')
    if not body.get('quantidade') and body.get('quantidade') < 0:
        ApiError(error_code=400, error_message='Quantidade inválida.')

