import logging
import re

from flask import make_response

from config import get_config
from controller.api_helper import ApiError, handler_exception, create_response, token_required
from service.empresa import find, get_item, create, update, remove, update_situacao

config = get_config()


@handler_exception
# @token_required(tipos=['administrador', 'empresa'], get_tipo=True)
def search(tipo: str = None, nome: str = None):
    logging.info('Listando Empresas')
    response = find(nome=nome)
    if tipo == 'empresa' and response:
        response = [{'id': response[0].get('id')}]
    return create_response(response=response, status=200)


@handler_exception
@token_required(tipos=['administrador', 'empresa'], validate_empresa=True)
def get(empresa_id: int):
    logging.info('Getting Empresa')
    response = get_item(empresa_id=empresa_id)
    if response:
        return create_response(response=response, status=200)
    else:
        raise ApiError(error_code=404, error_message='Empresa não encontrada')


@handler_exception
def post(body: dict):
    logging.info('Criando Empresa')
    validate_request(body=body, created=True)
    response = create(body=body)
    return create_response(response=response, status=201)


@handler_exception
@token_required(tipos=['administrador', 'empresa'], validate_empresa=True)
def put(empresa_id: int, body: dict):
    logging.info('Atualizando Empresa')
    validate_request(body=body, created=False)
    body['id'] = empresa_id
    response = update(body=body)
    return create_response(response=response, status=200)


@handler_exception
@token_required(tipos=['administrador'])
def put_situacao(empresa_id: int, body: dict):
    logging.info('Atualizando Situação Empresa')
    if body.get('situacaoConta') not in ['EM_ANALISE', 'APROVADO', 'REPROVADO', 'SUSPENSO']:
        ApiError(error_code=400, error_message='SituacaoConta invalida')
    body['id'] = empresa_id
    response = update_situacao(body=body)
    return create_response(response=response, status=200)


@handler_exception
@token_required(tipos=['administrador', 'empresa'], validate_empresa=True)
def delete(empresa_id: int):
    logging.info('Deletando Empresa')
    response = remove(empresa_id=empresa_id)
    if response:
        return create_response(response={}, status=200)
    else:
        raise ApiError(error_code=404, error_message='Empresa não encontrada')


def options():
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, token'
    return response


def options_id(empresa_id: int):
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, token'
    return response


def options_id_situacao(empresa_id: int):
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, token'
    return response


def validate_request(body: dict, created: bool):
    if created:
        if body.get('aceiteTermosUso') is None:
            ApiError(error_code=400, error_message='Aceite termos de uso inválidos.')
        if not body.get('senha') or len(body['senha']) > 50:
            ApiError(error_code=400, error_message='Senha inválida.')
        if not body.get('tipoArmazenagem') or body['tipoArmazenagem'] not in ['FIFO', 'FEFO', 'LIFO']:
            ApiError(error_code=400, error_message='Tipo de armazenagem inválida.')
    else:
        if body.get('senha') and len(body['senha']) > 50:
            ApiError(error_code=400, error_message='Senha inválida.')
    if not body.get('nomeUsuario') or len(body['nomeUsuario']) > 50:
        ApiError(error_code=400, error_message='Nome do usuário inválido.')
    if not body.get('razaoSocial') or len(body['razaoSocial']) > 50:
        ApiError(error_code=400, error_message='Razao social inválido.')
    if body.get('senha'):
        validate_password(senha=body['senha'])

def validate_password(senha: str):
    if len(senha) < 8:
        ApiError(error_code=400, error_message='A senha deve ter pelo menos 8 caracteres.')
    elif not re.search("[0-9]", senha):
        ApiError(error_code=400, error_message='A senha deve conter pelo menos 1 número.')
    elif not re.search("[a-z]", senha):
        ApiError(error_code=400, error_message='A senha deve ter pelo menos um caractere minúsculo.')
    elif not re.search("[A-Z]", senha):
        ApiError(error_code=400, error_message='A senha deve ter pelo menos um caractere maiúsculo.')
    elif senha.isalnum():
        ApiError(error_code=400, error_message='A senha deve conter pelo menos 1 caractere especial.')