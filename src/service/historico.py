import logging

from controller.api_helper import ApiError
from model.historico import query_all_historico, execute_create_historico, HistoricoHelper
from model.operador import query_one_operador


def find(empresa_id: int, produto_id: int):
    try:
        items = query_all_historico(empresa_id=empresa_id, produto_id=produto_id)
        return [HistoricoHelper.serialize(item) for item in items]
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def create(body: dict):
    try:
        operador = query_one_operador(empresa_id=body['empresaId'], usuario_id=body['usuarioId'])
        item = {
            'registroOperador': body['usuarioId'],
            'nomeOperador': operador.get('nome_usuario'),
            'nomeEstoque': body['nomeEstoque'],
            'quantidade': body['quantidade'],
            'operacao': body['quantidade'],
            'produtoId': body['produtoId'],
            'empresaId': body['empresaId']

        }
        execute_create_historico(item=item)
        return {}
    except Exception as ex:
        logging.error(ex)
        raise ApiError()
