import logging

from controller.api_helper import ApiError
from model.lote import LoteHelper, query_all_lote, execute_create_lote, execute_update_lote, query_one_lote,\
    execute_delete_lote


def find(empresa_id: int, codigo_lote: str):
    try:
        items = query_all_lote(empresa_id=empresa_id, codigo_lote=codigo_lote)
        return [LoteHelper.serialize(item) for item in items]
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def get_item(empresa_id: int, lote_id: int):
    try:
        item = query_one_lote(empresa_id=empresa_id, lote_id=lote_id)
        return LoteHelper.serialize(item) if item else {}
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def create(body: dict):
    if not is_unique(body=body):
        raise ApiError(error_code=400, error_message='Nome já existe.')
    item = {
        'codigoLote': body['codigoLote'],
        'dataEntrada': body['dataEntrada'],
        'dataValidade': body.get('dataValidade'),
        'quantidade': body['quantidade'],
        'empresaId': body['empresaId'],
    }
    try:
        execute_create_lote(item=item)
        return {}
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def update(body: dict):
    if not is_unique(body=body):
        raise ApiError(error_code=400, error_message='Nome já existe.')
    try:
        item = LoteHelper.serialize(query_one_lote(empresa_id=body['empresaId'], lote_id=body['id']))
        if item:
            item['codigoLote'] = body['codigoLote']
            item['dataEntrada'] = body['dataEntrada']
            item['dataValidade'] = body.get('dataValidade')
            item['quantidade'] = body['quantidade']
            # item['empresaId'] = body['empresaId']
            # item['id'] = body['id']
            execute_update_lote(item=item)
            return {}
        else:
            raise ApiError(error_code=404, error_message='Lote não encontrado')
    except ApiError as err:
        raise err
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def remove(empresa_id: int, lote_id: int):
    try:
        item = query_one_lote(empresa_id=empresa_id, lote_id=lote_id)
        if item:
            execute_delete_lote(empresa_id=empresa_id, lote_id=lote_id)
        return {}
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def is_unique(body: dict):
    try:
        items = query_all_lote(empresa_id=body['empresaId'], codigo_lote=body['codigoLote'])
        if body.get('id'):
            return False if items and int(body.get('id')) != items[0].get('id') else True
        else:
            return False if items else True
    except Exception as ex:
        logging.error(ex)
        raise ApiError()
