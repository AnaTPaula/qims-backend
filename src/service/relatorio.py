import logging
from pandas import DataFrame

from controller.api_helper import ApiError
from model.relatorio import query_saida_produto, query_produto_quantidade, query_entrada_produto, query_estoque_quantidade


def saida_produto(body: dict):
    try:
        results = query_saida_produto(empresa_id=body['empresaId'])
        data = {}
        for item in results:
            for k, v in item.items():
                if data.get(k):
                    data.get(k).append(v)
                else:
                    data[k] = [v]
        return DataFrame.from_dict(data=data)
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def entrada_produto(body: dict):
    try:
        results = query_entrada_produto(empresa_id=body['empresaId'])
        data = {}
        for item in results:
            for k, v in item.items():
                if data.get(k):
                    data.get(k).append(v)
                else:
                    data[k] = [v]
        return DataFrame.from_dict(data=data)
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def estoque_quantidade(body: dict):
    try:
        results = query_estoque_quantidade(empresa_id=body['empresaId'])
        data = {}
        for item in results:
            for k, v in item.items():
                if data.get(k):
                    data.get(k).append(v)
                else:
                    data[k] = [v]
        return DataFrame.from_dict(data=data)
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def produto_quantidade(body: dict):
    try:
        results = query_produto_quantidade(empresa_id=body['empresaId'])
        data = {}
        for item in results:
            for k, v in item.items():
                if data.get(k):
                    data.get(k).append(v)
                else:
                    data[k] = [v]
        return DataFrame.from_dict(data=data)
    except Exception as ex:
        logging.error(ex)
        raise ApiError()
