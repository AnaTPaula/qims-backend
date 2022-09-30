from config import database


class EstoqueHelper:

    @staticmethod
    def serialize(item):
        return {
            'id': item.get('id'),
            'nome': item.get('nome'),
            'quantidade': item.get('quantidade'),
            'descricao': item.get('descricao'),
            'localizacao': item.get('localizacao'),
            'produtoId': item.get('produto_fk'),
            'empresaId': item.get('empresa_fk')
        }


def query_all_estoque(empresa_id: int):
    query = " SELECT * from estoque WHERE empresa_fk = %s;"
    return database.select_all(query=query, params=(empresa_id,))


def query_one_estoque(empresa_id: int, estoque_id: int):
    query = "SELECT * from estoque WHERE empresa_fk = %s AND id = %s;"
    return database.select_one(query=query, params=(empresa_id, estoque_id,))


def execute_create_estoque(item: dict):
    query = "INSERT INTO estoque (nome, quantidade, descricao, localizacao, produto_fk, empresa_fk) VALUES " \
            "(%s, %s, %s, %s, %s, %s);"
    database.execute(query=query, params=(item['nome'], item['quantidade'], item.get('descricao'), item['localizacao'],
                                          item['produtoId'], item['empresaId'],))


def execute_update_estoque(item: dict):
    query = "UPDATE estoque SET nome = %s, quantidade = %s, descricao = %s, localizacao = %s " \
            "WHERE id = %s AND empresa_fk = %s;"
    database.execute(query=query, params=(item['nome'], item['quantidade'], item.get('descricao'), item['localizacao'],
                                          item['id'], item['empresaId'],))


def execute_delete_estoque(estoque_id: int, empresa_id: int):
    query = "DELETE FROM estoque WHERE id = %s AND empresa_fk = %s;"
    database.execute(query=query, params=(estoque_id, empresa_id,))
