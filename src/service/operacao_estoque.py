import logging

from werkzeug.exceptions import HTTPException

from controller.api_helper import ApiError
from model.estoque import query_one_estoque
from model.estoque_lote import execute_create_estoque_lote, execute_delete_estoque_lote, \
    query_all_lote_by_produto_estoque, query_one_lote, execute_update_lote, execute_delete_lote, LoteHelper
from model.produto_estoque import query_one_produto_estoque, execute_create_produto_estoque, \
    execute_update_produto_estoque, execute_delete_produto_estoque, ProdutoEstoqueHelper
from model.produto import query_one_prd
from model.empresa import query_one_empresa


def increase_estoque(body: dict):
    try:
        # Pegar o lote que deseja adicionar
        lote = query_one_lote(empresa_id=body['empresaId'], lote_id=body['loteId'])
        if not lote:
            raise ApiError(error_code=404, error_message='Lote não encontrado.')
        # verifica se lote já não foi utilizado anteriormente
        if lote.get('produto_estoque_fk'):
            raise ApiError(error_code=400, error_message='Lote adicionado anteriormente.')

        # valida se estoque existe
        estoque = query_one_estoque(empresa_id=body['empresaId'], estoque_id=body['estoqueId'])
        if not estoque:
            raise ApiError(error_code=404, error_message='Estoque não encontrado.')

        # valida se produto existe
        produto = query_one_prd(empresa_id=body['empresaId'], produto_id=body['produtoId'])
        if not produto:
            raise ApiError(error_code=404, error_message='Produto não encontrado.')

        # Pegar o produto_estoque que receberá o lote
        produto_estoque = query_one_produto_estoque(empresa_id=body['empresaId'], produto_id=body['produtoId'],
                                                    estoque_id=body['estoqueId'])
        # Se produto_estoque não existe deve-se criar
        if not produto_estoque:
            produto_estoque = {
                'quantidade': 0.0,
                'localizacao': body['localizacao'],
                'produtoId': body['produtoId'],
                'estoqueId': body['estoqueId'],
                'empresaId': body['empresaId'],
            }
            produto_estoque['id'] = execute_create_produto_estoque(produto_estoque)
        else:
            produto_estoque = ProdutoEstoqueHelper.serialize(produto_estoque)

        # Adicionando lote ao produto_estoque
        produto_estoque['quantidade'] += lote['quantidade']
        execute_update_produto_estoque(item=produto_estoque)

        # criando associação entre o estoque do produto com o lote
        estoque_lote = {
            'produtoEstoqueId': produto_estoque['id'],
            'loteId': lote['id'],
            'empresaId': produto_estoque['empresaId']
        }
        execute_create_estoque_lote(item=estoque_lote)

        # TODO: gerar historico
        historico = {
            'usuarioId': body['usuarioId'],
            'estoqueId': body['estoqueId'],
            'quantidade': lote['quantidade'],
            'operacao': 'ENTRADA',
            'produtoId': body['produtoId'],
        }
        # execute_create_historico(item=historico)

        return {}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def decrease_estoque(body: dict):
    try:
        # Pegar o produto_estoque que terá a saida
        produto_estoque = query_one_produto_estoque(empresa_id=body['empresaId'], produto_id=body['produtoId'],
                                                    estoque_id=body['estoqueId'])
        if not produto_estoque:
            raise ApiError(error_code=404, error_message='Estoque do Produto não encontrado.')
        empresa = query_one_empresa(usuario_id=body['empresaId'])

        # Pegar a lista de lotes que podem ser utilizados ordenados por FIFO, FEFO ou LIFO
        lotes = query_all_lote_by_produto_estoque(empresa_id=body['empresaId'],
                                                  produto_estoque_id=produto_estoque.get('id'),
                                                  tipo_armazenagem=empresa.get('tipo_armazenagem'))

        # validando se o total dos lotes é maior que o valor que se deseja retirar
        total_lotes = sum(item['quantidade'] for item in lotes)
        if total_lotes < body['quantidade']:
            raise ApiError(error_code=400, error_message='Quantidade indisponível.')

        # removendo quantidade do produto_estoque
        produto_estoque['quantidade'] -= body['quantidade']

        # Reduzindo a quantidade dos lotes
        # caso um lote fique com zero deve-se deletar caso contrario deve-se apenas atualizar
        quantidade = body['quantidade']
        lotes_alterar = []
        lotes_deletar = []
        for lote in lotes:
            # se quantidade estiver zerada deve-se sair do loop
            if quantidade <= 0:
                break
            # se a quantidade é maior que o lote removemos o valor da quantidade e colocamos o lote na lista de delete
            if quantidade >= lote['quantidade']:
                lotes_deletar.append(lote)
                quantidade -= lote['quantidade']
            # se a quantidade é menor que o lote removemos o valor do lote e colocamos o lote na lista de update
            else:
                lote['quantidade'] -= quantidade
                quantidade = 0.0
                lotes_alterar.append(lote)

        # Altera os lotes
        for lote in lotes_alterar:
            execute_update_lote(item=LoteHelper.serialize(lote))

        # Deleta os lotes e sua associação
        for lote in lotes_deletar:
            execute_delete_estoque_lote(empresa_id=lote['empresa_fk'], lote_id=lote['id'],
                                        produto_estoque_id=produto_estoque['id'])
            execute_delete_lote(empresa_id=lote['empresa_fk'], lote_id=lote['id'])

        # caso a quantidade seja 0 ou menor deve deletar o produto_estoque, caso contrario somente atualizar
        if produto_estoque['quantidade'] <= 0:
            execute_delete_produto_estoque(empresa_id=produto_estoque['empresa_fk'],
                                           produto_estoque_id=produto_estoque['id'])
        else:
            execute_update_produto_estoque(item=ProdutoEstoqueHelper.serialize(produto_estoque))

        # TODO: gerar historico
        historico = {
            'usuarioId': body['usuarioId'],
            'estoqueId': body['estoqueId'],
            'quantidade': body['quantidade'],
            'operacao': 'SAIDA',
            'produtoId': body['produtoId'],
        }
        # execute_create_historico(item=historico)
        return {}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def move_estoque(body: dict):
    lote = {}  # TODO: get lotes por estoque origem ordem FIFO, FEFO, LIFO
    estoque_origem = {}  # TODO: get estoque by id
    estoque_destino = {}  # TODO: get estoque by id
    # TODO: validar se a quantidade pode ser movida.
    # TODO: diminuir do estoque origem a quantidade
    # TODO: adicionar do estoque destino a quantidade
    # TODO: verificar se lote(s) ja possui associacao com estoque(s) destino (um para cada)
    # TODO: caso true apenas adicione o valor no lote
    # TODO: caso false crie novo lote com o mesmo nome, usando a quantidade movida e crie uma entidade estoque_lote
    # TODO: reduzir o valor dos lotes necessarios
    # TODO: caso o(s) lote(s) fiquem zerados remover entidade associativa estoque_lote e remover lote
    # TODO: caso o(s) lote(s) ainda contenham valor, atualizar o lote com o novo valor
    # TODO: gerar historico se for duas linhas complica o estorno
