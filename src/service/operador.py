import logging

from config import get_config
from controller.api_helper import ApiError
from model.operador import query_all, query_one, execute_create, execute_update, execute_delete, OperadorHelper
from model.usuario import UsuarioHelper


def find(empresa_id: str):
    try:
        items = query_all(empresa_id)
        return [item.serialize for item in items]
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def get_item(operador_id: int, empresa_id):
    try:
        item = query_one(operador_id, empresa_id)
        return item.serialize if item else {}
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def create(body: dict):
    if not is_unique(body=body):
        raise ApiError(error_code=400, error_message='Nome já existe.')
    try:
        execute_create(item=body)
        return {}
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def update(body: dict):
    if not is_unique(body=body):
        raise ApiError(error_code=400, error_message='Nome já existe.')
    try:
        item = query_one(empresa_id=body['empresaId'], usuario_id=body['usuarioId'])
        item['nomeUsuario'] = body['nomeUsuario']
        item['acesso'] = body['acesso']
        if body.get('senha'):
            item['senha'] = body['senha']
            UsuarioHelper.set_hash_password(item, body['senha'])
        execute_update(item=OperadorHelper.serialize(item))
        return {}
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def remove(usuario_id: int, empresa_id: str):
    try:
        item = query_one(usuario_id=usuario_id,empresa_id=empresa_id)
        if item:
            execute_delete(usuario_id, empresa_id)
        return item
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def is_unique(body: dict):
    try:
        items = query_all(empresa_id=body['empresaId'])
        if body.get('id'):
            return False if items and int(body.get('id')) != items[0].get('id') else True
        else:
            return False if items else True
    except Exception as ex:
        logging.error(ex)
        raise ApiError()
