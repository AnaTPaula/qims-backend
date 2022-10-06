import logging

from werkzeug.exceptions import HTTPException

from controller.api_helper import ApiError
from model.estoque import query_all_estoque, query_one_estoque, execute_create_estoque, execute_update_estoque, \
    execute_delete_estoque, EstoqueHelper


def find(empresa_id: int, nome: str = None):
    try:
        items = query_all_estoque(empresa_id=empresa_id, nome=nome)
        return [EstoqueHelper.serialize(item) for item in items]
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def get_item(empresa_id: int, estoque_id: int):
    try:
        item = query_one_estoque(empresa_id=empresa_id, estoque_id=estoque_id)
        return EstoqueHelper.serialize(item) if item else {}
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def create(body: dict):
    if not is_unique(body=body):
        raise ApiError(error_code=400, error_message='Nome já existe.')
    try:
        execute_create_estoque(item=body)
        return {}
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def update(body: dict):
    if not is_unique(body=body):
        raise ApiError(error_code=400, error_message='Nome já existe.')
    try:
        item = query_one_estoque(empresa_id=body['empresaId'], estoque_id=body['id'])
        item = EstoqueHelper.serialize(item) if item else None
        if item:
            item['nome'] = body['nome']
            item['descricao'] = body.get('descricao')
            execute_update_estoque(item=item)
        else:
            raise ApiError(error_code=404, error_message='Estoque não encontrado.')
        return {}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def remove(empresa_id: int, estoque_id: int):
    try:
        item = query_one_estoque(empresa_id=empresa_id, estoque_id=estoque_id)
        if not item:
            raise ApiError(error_code=404, error_message='Estoque não encontrado')
        else:
            if item.get('quantidade') > 0:
                raise ApiError(error_code=412, error_message='Quantidade do estoque é maior que zero')
            execute_delete_estoque(empresa_id=empresa_id, estoque_id=estoque_id)
        return item
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def is_unique(body: dict):
    try:
        items = query_all_estoque(empresa_id=body['empresaId'], nome=body['nome'])
        if body.get('id'):
            return False if items and int(body.get('id')) != items[0].get('id') else True
        else:
            return False if items else True
    except Exception as ex:
        logging.error(ex)
        raise ApiError()
