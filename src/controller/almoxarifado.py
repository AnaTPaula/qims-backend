import logging

from controller.api_helper import ApiError, handler_exception
from controller.api_helper import create_response
from service.almoxarifado import find, get_item, create, update, remove


@handler_exception
def search(conta: str):
    logging.info('Listando Almoxarifados')
    response = find(conta=conta)
    return create_response(response=response, status=200)


@handler_exception
def get(conta: str, almoxarifado_id: int):
    logging.info('Getting Almoxarifado')
    response = get_item(conta=conta, almoxarifado_id=almoxarifado_id)
    if response:
        return create_response(response=response, status=200)
    else:
        raise ApiError(error_code=404, error_message='Almoxarifado não encontrado')


@handler_exception
def post(conta: str, body: dict):
    logging.info('Criando Almoxarifado')
    body['conta'] = conta
    response = create(body=body)
    return create_response(response=response, status=201)


@handler_exception
def put(conta: str, almoxarifado_id: int, body: dict):
    logging.info('Atualizando Almoxarifado')
    body['conta'] = conta
    body['id'] = almoxarifado_id
    response = update(body=body)
    return create_response(response=response, status=200)


@handler_exception
def delete(conta: str, almoxarifado_id: int):
    logging.info('Deletando Almoxarifado')
    response = remove(conta=conta, almoxarifado_id=almoxarifado_id)
    if response:
        return create_response(response={}, status=200)
    else:
        raise ApiError(error_code=404, error_message='Almoxarifado não encontrado')
