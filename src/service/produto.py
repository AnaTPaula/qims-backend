import logging

from controller.api_helper import ApiError
from model.produto import ProdutoHelper, query_all_prd, execute_create_prd, execute_update_prd, \
    query_one_prd, execute_delete_prd


def find(empresa_id: str, nome: str):
    try:
        items = query_all_prd(empresa_id=empresa_id, nome=nome)
        return [ProdutoHelper.serialize(item) for item in items]
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def get_item(empresa_id: str, produto_id: int, nome: str):
    try:
        items = query_one_prd(empresa_id=empresa_id, id=produto_id, nome=nome)
        return [ProdutoHelper.serialize(item) for item in items]
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def create(body: dict):
    if not is_unique(body=body):
        raise ApiError(error_code=400, error_message='Nome já existe.')
    item = {
        'id': body['id'],
        'nome': body['nome'],
        'preco': body['preco'],
        'descricao': body['descricao'],
        'unidade': body['unidade'],
        'empresaId': body['empresaId'],
        'estoqueMinimo': body['estoqueMinimo'],
        'estoqueMaximo': body['estoqueMaximo'],
        'pontoReposicao': body['pontoReposicao']
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
        item = query_one_prd(empresa_id=body['empresaId'], id=body['id'], nome=body['nome'])
        if item:
            item['nome'] = body['nome']
            item['preco'] = body['preco']
            item['descricao'] = body['descricao']
            item['unidade'] = body['unidade']
            item['estoqueMinimo'] = body['estoqueMinimo']
            item['estoqueMaximo'] = body['estoqueMaximo']
            item['pontoReposicao'] = body['pontoReposicao']
            execute_update_prd(item=item)
        else:
            raise ApiError(error_code=404, error_message='Produto não encontrado')
        return {}
    except ApiError as err:
        raise err
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def remove(empresa_id: str, id: int, nome: str ):
    try:
        item = query_one_prd(empresa_id=empresa_id, id=id, nome=nome)
        if item:
            execute_delete_prd(empresa_id=empresa_id, id=id)
        return {}
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
