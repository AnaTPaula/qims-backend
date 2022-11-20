import logging

from flask import make_response

from config import get_config
from controller.api_helper import ApiError, handler_exception, create_response, token_required
from service.operacao_estoque import increase_estoque, decrease_estoque, move_estoque, reverse_operacao

config = get_config()


@handler_exception
@token_required(tipos=['operador'], acessos=['total', 'modificar'], validate_empresa=True, get_id=True)
def change(empresa_id: int, usuario_id: int, body: dict):
    logging.info(f'Operacoes do Estoques :{body.get("tipoOperacao")}')
    validate_request(body=body)
    body['empresaId'] = empresa_id
    body['usuarioId'] = usuario_id
    if body['tipoOperacao'] == 'ENTRADA':
        increase_estoque(body=body)
    elif body['tipoOperacao'] == 'SAIDA':
        decrease_estoque(body=body)
    elif body['tipoOperacao'] == 'TRANSFERENCIA':
        move_estoque(body=body)
    elif body['tipoOperacao'] == 'ESTORNO':
        reverse_operacao(body=body)
    return create_response(response={}, status=200)


def options(empresa_id: int):
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, token'
    return response


def validate_request(body: dict):
    if body.get('tipoOperacao') not in ['ENTRADA', 'SAIDA', 'TRANSFERENCIA', 'ESTORNO']:
        ApiError(error_code=400, error_message='Tipo de operação inválida.')
    if body.get('tipoOperacao') in ['ENTRADA', 'SAIDA', 'TRANSFERENCIA']:
        if body.get('tipoOperacao') == 'ENTRADA':
            if not body.get('loteId') or not isinstance(body.get('loteId'), int):
                ApiError(error_code=400, error_message='Lote inválido.')
            if body.get('localizacao') and len(body['localizacao']) > 100:
                ApiError(error_code=400, error_message='Localizacao inválida.')

        if body.get('tipoOperacao') in ['SAIDA', 'TRANSFERENCIA']:
            if not body.get('quantidade') or body.get('quantidade') < 0:
                ApiError(error_code=400, error_message='Quantidade inválida.')

        if not body.get('produtoId') or not isinstance(body.get('produtoId'), int):
            ApiError(error_code=400, error_message='Produto inválido.')

        if body.get('tipoOperacao') in ['ENTRADA', 'SAIDA']:
            if not body.get('estoqueId') or not isinstance(body.get('estoqueId'), int):
                ApiError(error_code=400, error_message='Estoque inválido.')
        else:
            if not body.get('estoqueOrigemId') or not isinstance(body.get('estoqueOrigemId'), int):
                ApiError(error_code=400, error_message='Estoque de Origem inválido.')
            if not body.get('estoqueDestinoId') or not isinstance(body.get('estoqueDestinoId'), int):
                ApiError(error_code=400, error_message='Estoque de Destino inválido.')
            if body.get('estoqueOrigemId') == body.get('estoqueDestinoId'):
                ApiError(error_code=400, error_message='Os estoques devem ser diferentes.')
    else:
        if not body.get('historicoId') or not isinstance(body.get('historicoId'), int):
            ApiError(error_code=400, error_message='Histórico inválido.')
