import logging

from controller.api_helper import ApiError
from model.relatorio import query_saida_produto, query_produto_quantidade, query_entrada_produto, query_estoque_quantidade


def saida_produto(body: dict):
    try:
        results = query_saida_produto(empresa_id=body['empresaId'])
        return results
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def entrada_produto(body: dict):
    try:
        results = query_entrada_produto(empresa_id=body['empresaId'])
        return results
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def estoque_quantidade(body: dict):
    try:
        results = query_estoque_quantidade(empresa_id=body['empresaId'])
        return results
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def produto_quantidade(body: dict):
    try:
        results = query_produto_quantidade(empresa_id=body['empresaId'])
        return results
    except Exception as ex:
        logging.error(ex)
        raise ApiError()
