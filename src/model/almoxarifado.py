from config import database


class AlmoxarifadoHelper:

    @staticmethod
    def serialize(item):
        return {
            'id': item.get('id'),
            'nome': item.get('nome'),
            'descricao': item.get('descricao'),
            'empresaId': item.get('empresa_fk')
        }


def query_all(empresa_id: str, nome: str = None):
    query = f"SELECT * from almoxarifado WHERE empresa_fk = {empresa_id}"
    if nome:
        query += f" AND nome = '{nome}'"
    return database.select_all(query=query)


def query_one(empresa_id: str, almoxarifado_id: int):
    query = f"SELECT * from almoxarifado WHERE empresa_fk = {empresa_id} AND id = {almoxarifado_id}"
    return database.select_one(query=query)


def execute_create(item: dict):
    query = f"INSERT INTO almoxarifado (nome, descricao, empresa_fk) VALUES " \
            f"('{item['nome']}', '{item['descricao']}', '{item['empresaId']}');"
    database.execute(query=query)


def execute_update(item: dict):
    query = f"UPDATE almoxarifado SET nome = '{item['nome']}', SET descricao = '{item['descricao']}'" \
            f" WHERE empresa_fk = '{item['empresaId']}' AND id = {item['id']}"
    database.execute(query=query)


def execute_delete(empresa_id: str, almoxarifado_id: int):
    query = f"DELETE FROM almoxarifado WHERE empresa_fk = '{empresa_id}' id = {almoxarifado_id}"
    database.execute(query=query)
