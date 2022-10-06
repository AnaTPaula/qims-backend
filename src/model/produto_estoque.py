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


def query_all_produto_estoque(empresa_id: int, produto_id: int):
    query = " SELECT * from produto_estoque WHERE empresa_fk = %s AND produto_fk = %s"
    return database.select_all(query=query, params=(empresa_id, produto_id,))


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
