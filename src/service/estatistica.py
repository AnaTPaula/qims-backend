import logging

from controller.api_helper import ApiError
from model.estatistica import count_all_produto, count_preco_total_produtos, count_all_estoque, query_last_historico, \
    query_produtos_estoque_maximo, query_produtos_estoque_minimo, query_produtos_ponto_reposicao, \
    query_entrada_produtos, query_saida_produtos, query_curva_abc, CurvaABCHelper


def get_info(empresa_id: int):
    try:
        info = {
            'totalProdutos': count_all_produto(empresa_id=empresa_id).get('count'),
            'totalEstoque': count_all_estoque(empresa_id=empresa_id).get('count'),
            'totalPreco': count_preco_total_produtos(empresa_id=empresa_id).get('preco_total'),
            'historico': query_last_historico(empresa_id=empresa_id),
            'estoqueMaximo': query_produtos_estoque_maximo(empresa_id=empresa_id),
            'estoqueMinimo': query_produtos_estoque_minimo(empresa_id=empresa_id),
            'pontoReposicao': query_produtos_ponto_reposicao(empresa_id=empresa_id),
            'entradaProduto': query_entrada_produtos(empresa_id=empresa_id),
            'saidaProduto': query_saida_produtos(empresa_id=empresa_id),
        }
        return info
    except Exception as ex:
        logging.error(ex)
        raise ApiError()


def get_curva_abc(empresa_id: int):
    try:
        return [CurvaABCHelper.serialize(item) for item in query_curva_abc(empresa_id=empresa_id)]
    except Exception as ex:
        logging.error(ex)
        raise ApiError()
