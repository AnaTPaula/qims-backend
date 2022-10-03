import logging

from werkzeug.exceptions import HTTPException

from controller.api_helper import ApiError
from model.estoque import query_all_estoque, query_one_estoque, execute_create_estoque, execute_update_estoque, \
    execute_delete_estoque, EstoqueHelper
from model.produto import query_one_prd


def find(empresa_id: int, produto_id: int, nome: str = None):
    try:
        items = query_all_estoque(empresa_id=empresa_id, produto_id=produto_id, nome=nome)
        return [EstoqueHelper.serialize(item) for item in items]
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def get_item(empresa_id: int, produto_id: int, estoque_id: int):
    try:
        item = query_one_estoque(empresa_id=empresa_id, produto_id=produto_id, estoque_id=estoque_id)
        return EstoqueHelper.serialize(item) if item else {}
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def create(body: dict):
    try:
        body['quantidade'] = 0.0
        produto = query_one_prd(empresa_id=body['empresaId'], produto_id=body['produtoId'])
        if produto:
            execute_create_estoque(item=body)
        else:
            raise ApiError(error_code=404, error_message='Produto não encontrado.')
        return {}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def update(body: dict):
    try:
        item = query_one_estoque(empresa_id=body['empresaId'], produto_id=body['produtoId'], estoque_id=body['id'])
        item = EstoqueHelper.serialize(item) if item else None
        if item:
            item['nome'] = body['nome']
            item['localizacao'] = body['localizacao']
            if body.get('descricao'):
                item['descricao'] = body['descricao']
            execute_update_estoque(item=item)
        else:
            raise ApiError(error_code=404, error_message='Estoque não encontrado.')
        return {}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def remove(empresa_id: int, produto_id: int, estoque_id: int):
    try:
        item = query_one_estoque(empresa_id=empresa_id, produto_id=produto_id, estoque_id=estoque_id)
        if item:
            execute_delete_estoque(empresa_id=empresa_id, produto_id=produto_id, estoque_id=estoque_id)
        return item
    except Exception as ex:
        logging.error(ex)
        raise ApiError()
