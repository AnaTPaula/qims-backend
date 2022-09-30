import logging

from werkzeug.exceptions import HTTPException

from controller.api_helper import ApiError
from model.empresa import EmpresaHelper, query_all_empresa, query_one_empresa, execute_create_empresa, \
    execute_update_empresa
from model.operador import query_all_operador
from model.usuario import UsuarioHelper, execute_create_user, execute_update_user, execute_delete_user, \
    execute_delete_batch_user


def find(nome: str):
    try:
        items = query_all_empresa(nome=nome)
        return [EmpresaHelper.serialize(item) for item in items]
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def get_item(empresa_id: int):
    try:
        item = query_one_empresa(usuario_id=empresa_id)
        return EmpresaHelper.serialize(item) if item else {}
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def create(body: dict):
    if not is_unique(body=body):
        raise ApiError(error_code=400, error_message='Nome já existe.')
    item = {
        'tipo': 'empresa',
        'senha': UsuarioHelper.set_hash_password(body['senha']),
        'nomeUsuario': body['nomeUsuario'],
        'situacaoConta': 'EM_ANALISE',
        'tipoArmazenagem': body['tipoArmazenagem'],
        'aceiteTermosUso': body['aceiteTermosUso'],
        'razaoSocial': body['razaoSocial']
    }
    try:
        user_id = execute_create_user(item=item)
    except Exception as ex:
        logging.error(ex)
        raise ApiError()

    try:
        item['id'] = user_id
        execute_create_empresa(item=item)
        return {}
    except Exception as ex:
        logging.error(ex)
        execute_delete_user(usuario_id=user_id)
        raise ApiError()


def update(body: dict):
    if not is_unique(body=body):
        raise ApiError(error_code=400, error_message='Nome já existe.')
    try:
        item = EmpresaHelper.serialize(query_one_empresa(usuario_id=body['id']))
        if item:
            item['nomeUsuario'] = body['nomeUsuario']
            item['razaoSocial'] = body['razaoSocial']
            if body.get('senha'):
                item['senha'] = UsuarioHelper.set_hash_password(body['senha'])
                execute_update_user(item=item)
            execute_update_empresa(item=item)
        else:
            raise ApiError(error_code=404, error_message='Usuário não encontrado.')
        return {}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def update_situacao(body: dict):
    try:
        item = query_one_empresa(usuario_id=body['id'])
        item = EmpresaHelper.serialize(item) if item else None
        if item:
            item['situacaoConta'] = body['situacaoConta']
            execute_update_empresa(item=item)
        else:
            raise ApiError(error_code=404, error_message='Usuário não encontrado.')
        return {}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def remove(empresa_id: int):
    try:
        item = query_one_empresa(usuario_id=empresa_id)
        if item:
            operadores = query_all_operador(empresa_id=empresa_id)
            operador_ids = [operador.get('id') for operador in operadores]
            if operador_ids:
                execute_delete_batch_user(usuario_ids=tuple(operador_ids))
            execute_delete_user(usuario_id=empresa_id)
        return item
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def is_unique(body: dict):
    try:
        items = query_all_empresa(nome=body['nomeUsuario'])
        if body.get('id'):
            return False if items and int(body.get('id')) != items[0].get('id') else True
        else:
            return False if items else True
    except Exception as ex:
        logging.error(ex)
        raise ApiError()
