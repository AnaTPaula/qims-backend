import logging

from controller.api_helper import ApiError
from model.produto_estoque import query_all_produto_estoque_for_produto, query_all_produto_estoque_for_estoque, \
    ProdutoEstoqueHelper


def get_produto_estoque_for_produto(empresa_id: int, produto_id: int):
    try:
        items = query_all_produto_estoque_for_produto(empresa_id=empresa_id, produto_id=produto_id)
        return [ProdutoEstoqueHelper.serialize_produto(item) for item in items]
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def get_produto_estoque_for_estoque(empresa_id: int, estoque_id: int):
    try:
        items = query_all_produto_estoque_for_estoque(empresa_id=empresa_id, estoque_id=estoque_id)
        return [ProdutoEstoqueHelper.serialize_estoque(item) for item in items]
    except Exception as ex:
        logging.error(ex)
        raise ApiError()
