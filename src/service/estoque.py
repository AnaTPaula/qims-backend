import logging

from werkzeug.exceptions import HTTPException

from controller.api_helper import ApiError
from model.estoque import query_all_estoque, query_one_estoque, execute_create_estoque, execute_update_estoque, \
    execute_delete_estoque, EstoqueHelper


def find(empresa_id: int):
    try:
        items = query_all_estoque(empresa_id=empresa_id)
        return [EstoqueHelper.serialize(item) for item in items]
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def get_item(estoque_id: int, empresa_id: int):
    try:
        item = query_one_estoque(empresa_id=empresa_id, estoque_id=estoque_id)
        return EstoqueHelper.serialize(item) if item else {}
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def create(body: dict):
    try:
        body['quantidade'] = 0
        execute_create_estoque(item=body)
        return {}
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def update(body: dict):
    try:
        item = query_one_estoque(empresa_id=body['empresaId'], estoque_id=body['id'])
        item = EstoqueHelper.serialize(item) if item else None
        if item:
            item['nome'] = body['nome']
            item['quantidade'] = body['quantidade']
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


def remove(estoque_id: int, empresa_id: int):
    try:
        item = query_one_estoque(estoque_id=estoque_id, empresa_id=empresa_id)
        if item:
            execute_delete_estoque(estoque_id=estoque_id, empresa_id=empresa_id)
        return item
    except Exception as ex:
        logging.error(ex)
        raise ApiError()
