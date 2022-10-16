from config import database


class ProdutoEstoqueHelper:

    @staticmethod
    def serialize(item):
        return {
            'id': item.get('id'),
            'quantidade': item.get('quantidade'),
            'localizacao': item.get('localizacao'),
            'produtoId': item.get('produto_fk'),
            'estoqueId': item.get('estoque_fk'),
            'empresaId': item.get('empresa_fk')
        }

    @staticmethod
    def serialize_produto(item):
        return {
            'produtoId': item.get('produto_id'),
            'nomeProduto': item.get('nome_produto'),
            'empresaId': item.get('empresa_id'),
            'quantidade': item.get('quantidade'),
            'localizacao': item.get('localizacao'),
            'nomeEstoque': item.get('nome_estoque'),
        }

    @staticmethod
    def serialize_estoque(item):
        return {
            'estoqueId': item.get('estoque_id'),
            'nomeProduto': item.get('nome_produto'),
            'empresaId': item.get('empresa_id'),
            'quantidade': item.get('quantidade'),
            'localizacao': item.get('localizacao'),
            'nomeEstoque': item.get('nome_estoque'),
        }

def query_all_produto_estoque(empresa_id: int, produto_id: int):
    query = " SELECT * from produto_estoque WHERE empresa_fk = %s AND produto_fk = %s order by nome_produto"
    return database.select_all(query=query, params=(empresa_id, produto_id,))


def query_all_produto_estoque_for_produto(empresa_id: int, produto_id: int):
    query = "SELECT p.id as produto_id, p.nome as nome_produto, p.empresa_fk as empresa_id, " \
            "COALESCE(pe.quantidade, 0) as quantidade, pe.localizacao, e.nome as nome_estoque from produto p " \
            "left join produto_estoque pe on p.id = pe.produto_fk left join estoque e on pe.estoque_fk = e.id " \
            "WHERE p.empresa_fk = %s AND p.id = %s order by e.nome"
    return database.select_all(query=query, params=(empresa_id, produto_id,))


def query_all_produto_estoque_for_estoque(empresa_id: int, estoque_id: int):
    query = " SELECT e.id as estoque_id, p.nome as nome_produto, e.empresa_fk as empresa_id, " \
            "COALESCE(pe.quantidade, 0) as quantidade, pe.localizacao, e.nome as nome_estoque from estoque e " \
            "left join produto_estoque pe on e.id = pe.estoque_fk left join produto p on pe.produto_fk = p.id " \
            "WHERE e.empresa_fk = %s AND e.id = %s order by p.nome"
    return database.select_all(query=query, params=(empresa_id, estoque_id,))


def query_one_produto_estoque(empresa_id: int, produto_id: int, estoque_id: int):
    query = "SELECT * from produto_estoque WHERE empresa_fk = %s AND produto_fk = %s AND estoque_fk = %s;"
    return database.select_one(query=query, params=(empresa_id, produto_id, estoque_id,))


def execute_create_produto_estoque(item: dict) -> int:
    query = "INSERT INTO produto_estoque (quantidade, localizacao, produto_fk, estoque_fk, empresa_fk) VALUES " \
            "(%s, %s, %s, %s, %s) RETURNING id;"
    return database.execute_returning_id(query=query, params=(item['quantidade'], item['localizacao'],
                                                              item['produtoId'], item['estoqueId'], item['empresaId'],))


def execute_update_produto_estoque(item: dict):
    query = "UPDATE produto_estoque SET quantidade = %s, localizacao = %s WHERE estoque_fk = %s AND produto_fk = %s " \
            "AND empresa_fk = %s;"
    database.execute(query=query, params=(item['quantidade'], item.get('localizacao'),
                                          item['estoqueId'], item['produtoId'], item['empresaId'],))


def execute_delete_produto_estoque(empresa_id: int, produto_estoque_id: int):
    query = "DELETE FROM produto_estoque WHERE empresa_fk = %s AND id = %s;"
    database.execute(query=query, params=(empresa_id, produto_estoque_id,))
