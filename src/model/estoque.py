from config import database


class EstoqueHelper:

    @staticmethod
    def serialize(item):
        return {
            'id': item.get('id'),
            'nome': item.get('nome'),
            'descricao': item.get('descricao'),
            'empresaId': item.get('empresa_fk')
        }


def query_all_estoque(empresa_id: int, nome: str = None):
    query = " SELECT * from estoque WHERE empresa_fk = %s "
    if nome:
        query += " AND nome = %s;"
    params = (empresa_id, nome,) if nome else (empresa_id,)
    return database.select_all(query=query, params=params)


def query_one_estoque(empresa_id: int, estoque_id: int):
    query = "SELECT e.*, COALESCE(sum(pe.quantidade), 0) as quantidade from estoque e left join produto_estoque pe " \
            "on e.id = pe.estoque_fk WHERE e.empresa_fk = %s AND e.id = %s group by e.id;"
    return database.select_one(query=query, params=(empresa_id, estoque_id,))


def execute_create_estoque(item: dict):
    query = "INSERT INTO estoque (nome, descricao, empresa_fk) VALUES " \
            "(%s, %s, %s);"
    database.execute(query=query, params=(item['nome'], item.get('descricao'), item['empresaId'],))


def execute_update_estoque(item: dict):
    query = "UPDATE estoque SET nome = %s, descricao = %s WHERE id = %s AND empresa_fk = %s;"
    database.execute(query=query, params=(item['nome'], item.get('descricao'), item['id'], item['empresaId'],))


def execute_delete_estoque(empresa_id: int, estoque_id: int):
    query = "DELETE FROM estoque WHERE empresa_fk = %s AND id = %s;"
    database.execute(query=query, params=(empresa_id, estoque_id,))
