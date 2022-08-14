from config import database

class MaterialHelper:

    @staticmethod
    def serialize(item):
        return {
            'id': item.get('id'),
            'nome': item.get('nome'),
            'preco': item.get('preco'),
            'descricao': item.get('descricao'),
            'unidade': item.get('unidade'),
            'empresaId': item.get('empresa_fk')
        }


def query_all(empresa_id: str, nome: str = None):
    query = f"SELECT * from material WHERE empresa_fk = {empresa_id}"
    if nome:
        query += f" AND nome = '{nome}'"
    return database.select_all(query=query)


def query_one(empresa_id: str, almoxarifado_id: int):
    query = f"SELECT * from material WHERE empresa_fk = {empresa_id} AND id = {almoxarifado_id}"
    return database.select_one(query=query)


def execute_create(item: dict):
    query = f"INSERT INTO material (nome, preco, descricao, unidade, empresa_fk ) VALUES " \
            f"('{item['nome']}', '{item['preco']}', '{item['descricao']}'," \
            f"'{item['unidade']}', '{item['empresaId']}');"
    database.execute(query=query)


def execute_update(item: dict):
    query = f" UPDATE material SET nome = '{item['nome']}', SET preco = '{item['preco']}', " \
            f" SET descricao = '{item['descricao']}', SET unidade = '{item['unidade']}' " \
            f" WHERE empresa_fk = '{item['empresaId']}' AND id = {item['id']}"
    database.execute(query=query)


def execute_delete(empresa_id: str, material_id: int):
    query = f"DELETE FROM material WHERE empresa_fk = '{empresa_id}' AND id = {material_id}"
    database.execute(query=query)