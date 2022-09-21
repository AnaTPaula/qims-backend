from config import database


class EstoqueHelper:

    @staticmethod
    def serialize(item):
        return {
            'id': item.get('id'),
            'nome': item.get('nome'),
            'quantidade': item.get('quantidade'),
            'descricao': item.get('descricao'),
            'localizacao': item.get('localizacao_fk'),
            'produtoId': item.get('produto_fk'),
            'empresaId': item.get('empresa_fk')
        }


def query_all(empresa_id: str):
    query = f" SELECT * from almoxarifado WHERE empresa_fk = {empresa_id} "
    return database.select_all(query=query)


def query_one(empresa_id: str, id: int):
    query = f" SELECT * from estoque WHERE empresa_fk = {empresa_id} AND id = {id} "
    return database.select_one(query=query)


def execute_create(item: dict):
    query = f" INSERT INTO estoque (id, nome, quantidade, descricao, localizacao, produto_fk, empresa_fk) VALUES " \
            f" ('{item['id']}', '{item['nome']}', '{item['quantidade']}', '{item['descricao']}', '{item['localizacao']}') "\
            f" '{item['produtoId']}', '{item['empresaId']}'); "
    database.execute(query=query)


def execute_update(item: dict):
    query = f" UPDATE estoque SET nome = '{item['nome']}', quantidade = '{item['quantidade']}', " \
            f" localizacao = '{item['localizacao']}' " \
            f" WHERE produto_fk = '{item['produtoId']}' AND id = {item['id']} AND empresa_fk = {item['empresaId']} "
    database.execute(query=query)


def execute_delete(id: str, empresa_id: str, produto_id: str):
    query = f"DELETE FROM estoque WHERE id = {id} AND empresa_fk = {empresa_id} AND produto_fk = {produto_id}"
    database.execute(query=query)