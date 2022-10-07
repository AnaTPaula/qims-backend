import logging

from controller.api_helper import ApiError
from model.operador import query_all_operador, query_one_operador, execute_create_operador, execute_update_operador, \
    OperadorHelper
from model.usuario import UsuarioHelper, execute_create_user, execute_update_user, execute_delete_user
from werkzeug.exceptions import HTTPException


def find(empresa_id: int, nome: str = None):
    try:
        items = query_all_operador(empresa_id=empresa_id, nome=nome)
        return [OperadorHelper.serialize(item) for item in items]
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def get_item(operador_id: int, empresa_id: int):
    try:
        item = query_one_operador(empresa_id=empresa_id, usuario_id=operador_id)
        return OperadorHelper.serialize(item) if item else {}
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def create(body: dict):
    if not is_unique(body=body):
        raise ApiError(error_code=400, error_message='Nome já existe.')
    item = {
        'tipo': 'operador',
        'senha': UsuarioHelper.set_hash_password(body['senha']),
        'nomeUsuario': body['nomeUsuario'],
        'tipoAcesso': body['tipoAcesso'],
        'empresaId': body['empresaId']
    }
    try:
        user_id = execute_create_user(item=item)
    except Exception as ex:
        logging.error(ex)
        raise ApiError()
    try:
        item['id'] = user_id
        execute_create_operador(item=item)
        return {}
    except Exception as ex:
        logging.error(ex)
        execute_delete_user(usuario_id=user_id)
        raise ApiError()


def update(body: dict):
    if not is_unique(body=body):
        raise ApiError(error_code=400, error_message='Nome já existe.')
    try:
        item = query_one_operador(empresa_id=body['empresaId'], usuario_id=body['id'])
        item = OperadorHelper.serialize(item) if item else None
        if item:
            item['nomeUsuario'] = body['nomeUsuario']
            item['tipoAcesso'] = body['tipoAcesso']
            if body.get('senha'):
                item['senha'] = UsuarioHelper.set_hash_password(body['senha'])
                execute_update_user(item=item)
            execute_update_operador(item=item)
        else:
            raise ApiError(error_code=404, error_message='Usuário não encontrado.')
        return {}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def update_senha(body: dict):
    try:
        item = query_one_operador(empresa_id=body['empresaId'], usuario_id=body['id'])
        item = OperadorHelper.serialize(item) if item else None
        if item:
            if body.get('senha'):
                item['senha'] = UsuarioHelper.set_hash_password(body['senha'])
                execute_update_user(item=item)
        else:
            raise ApiError(error_code=404, error_message='Usuário não encontrado.')
        return {}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def remove(operador_id: int, empresa_id: int):
    try:
        item = query_one_operador(usuario_id=operador_id, empresa_id=empresa_id)
        if item:
            execute_delete_user(usuario_id=operador_id)
        return item
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def is_unique(body: dict):
    try:
        items = query_all_operador(empresa_id=body['empresaId'], nome=body['nomeUsuario'])
        if body.get('id'):
            return False if items and int(body.get('id')) != items[0].get('id') else True
        else:
            return False if items else True
    except Exception as ex:
        logging.error(ex)
        raise ApiError()
