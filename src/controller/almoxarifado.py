import logging

from controller.api_helper import create_response
from service.almoxarifado import find


def search(conta: str):
    logging.info('Listando Almoxarifados')
    response = find(conta=conta)
    return create_response(response=response, status=200)
