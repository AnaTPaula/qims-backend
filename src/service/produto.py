import logging

from controller.api_helper import ApiError
from model.produto import ProdutoHelper, query_all_prd, execute_create_prd, execute_update_prd, \
    query_one_prd, execute_delete_prd
from werkzeug.exceptions import HTTPException


def find(empresa_id: int, nome: str):
    try:
        items = query_all_prd(empresa_id=empresa_id, nome=nome)
        return [ProdutoHelper.serialize(item) for item in items]
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def get_item(empresa_id: int, produto_id: int):
    try:
        item = query_one_prd(empresa_id=empresa_id, produto_id=produto_id)
        return ProdutoHelper.serialize(item) if item else {}
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def create(body: dict):
    if not is_unique(body=body):
        raise ApiError(error_code=400, error_message='Nome já existe.')
    item = {
        'nome': body['nome'],
        'preco': body['preco'],
        'descricao': body.get('descricao'),
        'unidade': body['unidade'],
        'empresaId': body['empresaId'],
        'estoqueMinimo': 0.0,
        'estoqueMaximo': 0.0,
        'pontoReposicao': 0.0
    }
    try:
        execute_create_prd(item=item)
        return {}
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def update(body: dict):
    if not is_unique(body=body):
        raise ApiError(error_code=400, error_message='Nome já existe.')
    try:
        item = query_one_prd(empresa_id=body['empresaId'], produto_id=body['id'])
        if item:
            item['nome'] = body['nome']
            item['preco'] = body['preco']
            item['descricao'] = body.get('descricao')
            item['unidade'] = body['unidade']
            item['estoqueMinimo'] = item['estoque_minimo']
            item['estoqueMaximo'] = item['estoque_maximo']
            item['pontoReposicao'] = item['ponto_reposicao']
            item['empresaId'] = body['empresaId']
            item['id'] = body['id']
            execute_update_prd(item=item)
            return {}
        else:
            raise ApiError(error_code=404, error_message='Produto não encontrado')
    except ApiError as err:
        raise err
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def remove(empresa_id: int, produto_id: int):
    try:
        item = query_one_prd(empresa_id=empresa_id, produto_id=produto_id)
        if not item:
            raise ApiError(error_code=404, error_message='Produto não encontrado')
        else:
            if item.get('quantidade') > 0:
                raise ApiError(error_code=412, error_message='Quantidade de produto é maior que zero')
            execute_delete_prd(empresa_id=empresa_id, produto_id=produto_id)
        return {}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def is_unique(body: dict):
    try:
        items = query_all_prd(empresa_id=body['empresaId'], nome=body['nome'])
        if body.get('id'):
            return False if items and int(body.get('id')) != items[0].get('id') else True
        else:
            return False if items else True
    except Exception as ex:
        logging.error(ex)
        raise ApiError()
