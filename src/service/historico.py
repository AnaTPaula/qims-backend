import logging

from controller.api_helper import ApiError
from model.historico import query_all_historico, execute_create_historico, HistoricoHelper


def find(empresa_id: int, produto_id: int):
    try:
        items = query_all_historico(empresa_id=empresa_id, produto_id=produto_id)
        return [HistoricoHelper.serialize(item) for item in items]
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def create(body: dict):
    try:
        execute_create_historico(item=body)
        return {}
    except Exception as ex:
        logging.error(ex)
        raise ApiError()
