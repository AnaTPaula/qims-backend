import logging

from werkzeug.exceptions import HTTPException

from controller.api_helper import ApiError
from model.administrador import AdministradorHelper, query_all_adm, execute_create_adm, execute_update_adm, \
    query_one_adm
from model.usuario import UsuarioHelper, execute_create_user, execute_delete_user, execute_update_user


def find():
    try:
        items = query_all_adm()
        return [AdministradorHelper.serialize(item) for item in items]
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def get_item(administrador_id: int):
    try:
        item = query_one_adm(usuario_id=administrador_id)
        return AdministradorHelper.serialize(item) if item else {}
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def create(body: dict):
    if not is_unique(body=body):
        raise ApiError(error_code=400, error_message='Nome já existe.')
    item = {
        'tipo': 'administrador',
        'senha': UsuarioHelper.set_hash_password(body['senha']),
        'nomeUsuario': body['nomeUsuario']
    }
    try:
        user_id = execute_create_user(item=item)
    except Exception as ex:
        logging.error(ex)
        raise ApiError()

    try:
        item['id'] = user_id
        execute_create_adm(item=item)
        return {}
    except Exception as ex:
        logging.error(ex)
        execute_delete_user(usuario_id=user_id)
        raise ApiError()


def update(body: dict):
    if not is_unique(body=body):
        raise ApiError(error_code=400, error_message='Nome já existe.')
    try:
        item = query_one_adm(usuario_id=body['id'])
        if item:
            item['nomeUsuario'] = body['nomeUsuario']
            if body.get('senha'):
                item['senha'] = UsuarioHelper.set_hash_password(body['senha'])
            execute_update_user(item=item)
            execute_update_adm(item=item)
        else:
            raise ApiError(error_code=404, error_message='Usuário não encontrado.')
        return {}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def remove(usuario_id: int):
    try:
        item = query_one_adm(usuario_id=usuario_id)
        if item:
            execute_delete_user(usuario_id=usuario_id)
        return item
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def is_unique(body: dict):
    try:
        items = query_all_adm(nome=body['nomeUsuario'])
        if body.get('id'):
            return False if items and int(body.get('id')) != items[0].get('id') else True
        else:
            return False if items else True
    except Exception as ex:
        logging.error(ex)
        raise ApiError()
