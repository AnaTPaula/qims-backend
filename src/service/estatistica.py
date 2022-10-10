import logging

from controller.api_helper import ApiError
from model.estatistica import count_all_produto, count_preco_total_produtos, count_all_estoque


def get_info(empresa_id: int):
    try:
        info = {
            'totalProdutos': count_all_produto(empresa_id=empresa_id).get('count'),
            'totalEstoque': count_all_estoque(empresa_id=empresa_id).get('count'),
            'totalPreco': count_preco_total_produtos(empresa_id=empresa_id).get('preco_total')
        }
        return info
    except Exception as ex:
        logging.error(ex)
        raise ApiError()
