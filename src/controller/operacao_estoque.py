import logging

from flask import make_response

from config import get_config
from controller.api_helper import ApiError, handler_exception, create_response, token_required
from service.operacao_estoque import increase_estoque, decrease_estoque

config = get_config()


@handler_exception
@token_required(tipos=['operador'], acessos=['total', 'modificar'], validate_empresa=True, get_id=True)
def change(empresa_id: int, usuario_id: int, body: dict):
    logging.info('Alterando Estoques')
    validate_request(body=body)
    body['empresaId'] = empresa_id
    body['usuarioId'] = usuario_id
    if body['tipoOperacao'] == 'ENTRADA':
        response = increase_estoque(body=body)
    else:
        response = decrease_estoque(body=body)
    return create_response(response=response, status=200)


def options(empresa_id: int):
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, token'
    return response


def validate_request(body: dict):
    if body.get('tipoOperacao') not in ['ENTRADA', 'SAIDA']:
        ApiError(error_code=400, error_message='Tipo invalido.')
    if body.get('tipoOperacao') == 'ENTRADA':
        if not body.get('loteId') or not isinstance(body.get('loteId'), int):
            ApiError(error_code=400, error_message='Lote invalido.')
        if body.get('localizacao') and len(body['localizacao']) > 100:
            ApiError(error_code=400, error_message='Localizacao invalida.')

    if body.get('tipoOperacao') == 'SAIDA':
        if not body.get('quantidade') or body.get('quantidade') < 0:
            ApiError(error_code=400, error_message='Quantidade invalida.')

    if not body.get('produtoId') or not isinstance(body.get('produtoId'), int):
        ApiError(error_code=400, error_message='Produto invalido.')
    if not body.get('estoqueId') or not isinstance(body.get('estoqueId'), int):
        ApiError(error_code=400, error_message='Estoque invalido.')
