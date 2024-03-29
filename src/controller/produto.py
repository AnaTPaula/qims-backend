import logging

from flask import make_response

from config import get_config
from controller.api_helper import ApiError, handler_exception, create_response, token_required
from service.produto import find, get_item, create, update, remove

config = get_config()


@handler_exception
@token_required(tipos=['operador'], acessos=['total', 'modificar', 'leitura'], validate_empresa=True)
def search(empresa_id: int, nome: str = None):
    logging.info('Listando Produtos')
    response = find(empresa_id=empresa_id, nome=nome)
    return create_response(response=response, status=200)


@handler_exception
@token_required(tipos=['operador'], acessos=['total', 'modificar', 'leitura'], validate_empresa=True)
def get(empresa_id: int, produto_id: int):
    logging.info('Getting Produto')
    response = get_item(empresa_id=empresa_id, produto_id=produto_id)
    if response:
        return create_response(response=response, status=200)
    else:
        raise ApiError(error_code=404, error_message='Produto não encontrado')


@handler_exception
@token_required(tipos=['operador'], acessos=['total'], validate_empresa=True)
def post(empresa_id: str, body: dict):
    logging.info('Criando Produto')
    validate_request(body=body)
    body['empresaId'] = empresa_id
    response = create(body=body)
    return create_response(response=response, status=201)


@handler_exception
@token_required(tipos=['operador'], acessos=['total', 'modificar'], validate_empresa=True)
def put(empresa_id: int, produto_id: int, body: dict):
    logging.info('Atualizando Produto')
    validate_request(body=body)
    body['empresaId'] = empresa_id
    body['id'] = produto_id
    response = update(body=body)
    return create_response(response=response, status=200)


@handler_exception
@token_required(tipos=['operador'], acessos=['total'], validate_empresa=True)
def delete(empresa_id: int, produto_id: int):
    logging.info('Deletando Produto')
    response = remove(empresa_id=empresa_id, produto_id=produto_id)
    return create_response(response=response, status=200)


def options(empresa_id: str):
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, token'
    return response


def options_id(empresa_id: str, produto_id: int):
    response = make_response('{}', 200)
    response.headers['Access-Control-Allow-Origin'] = config.origin
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, DELETE, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, token'
    return response


def validate_request(body: dict):
    if not body.get('nome') or len(body['nome']) > 50:
        ApiError(error_code=400, error_message='Nome inválido.')
    if body.get('descricao') and len(body['descricao']) > 255:
        ApiError(error_code=400, error_message='Descrição inválida.')
    if not body.get('preco') or body.get('preco') < 0:
        ApiError(error_code=400, error_message='Preço inválido.')
    if not body.get('unidade') or len(body['unidade']) > 25:
        ApiError(error_code=400, error_message='Unidade inválida.')
    if body.get('estoqueMaximo') and body.get('estoqueMaximo') < 0:
        ApiError(error_code=400, error_message='Estoque Máximo inválido.')
    if body.get('estoqueMinimo') and body.get('estoqueMinimo') < 0:
        ApiError(error_code=400, error_message='Estoque Mínimo inválido.')
    if body.get('pontoReposicao') and body.get('pontoReposicao') < 0:
        ApiError(error_code=400, error_message='Ponto Reposição inválido.')

    if body.get('estoqueMaximo') and body.get('estoqueMinimo') and body.get('estoqueMaximo') <= body.get(
            'estoqueMinimo'):
        ApiError(error_code=400, error_message='Estoque máximo menor que estoque mínimo')
    if body.get('estoqueMaximo') and body.get('pontoReposicao') and body.get('estoqueMaximo') <= body.get(
            'pontoReposicao'):
        ApiError(error_code=400, error_message='Estoque máximo menor que ponto de reposição')
    if body.get('pontoReposicao') and body.get('estoqueMinimo') and body.get('pontoReposicao') <= body.get(
            'estoqueMinimo'):
        ApiError(error_code=400, error_message='Ponto reposição menor que estoque mínimo')
