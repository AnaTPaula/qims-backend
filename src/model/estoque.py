from config import database


class EstoqueHelper:

    @staticmethod
    def serialize(item):
        return {
            'id': item.get('id'),
            'quantidade': item.get('quantidade'),
            'almoxarifadoId': item.get('almoxarifado_fk'),
            'localizacaoId': item.get('localizacao_fk'),
            'materialId': item.get('material_fk')
        }


def query_all(almoxarifado_id: str):
    query = f"SELECT * from almoxarifado WHERE empresa_fk = {almoxarifado_id}"
    return database.select_all(query=query)


def query_one(almoxarifado_id: str, id: int):
    query = f"SELECT * from estoque WHERE empresa_fk = {almoxarifado_id} AND id = {id}"
    return database.select_one(query=query)


def execute_create(item: dict):
    query = f"INSERT INTO estoque (quantidade, almoxarifado_fk, localizacao_fk, material_fk) VALUES " \
            f"('{item['quantidade']}', '{item['almoxarifadoId']}', '{item['localizacaoId']}', '{item['materialId']}');"
    database.execute(query=query)


def execute_update(item: dict):
    query = f"UPDATE estoque SET quantidade = '{item['quantidade']}', SET almoxarifado_fk = '{item['almoxarifadoId']}'," \
            f"SET localizacao_fk = '{item['localizacaoId']}', SET material_fk = '{item['materialId']}'" \
            f" WHERE almoxarifado_fk = '{item['almoxarifadoId']}' AND id = {item['id']}"
    database.execute(query=query)


def execute_delete(id: int, almoxarifado_id: int):
    query = f"DELETE FROM estoque WHERE id = '{id}' AND almoxarifado_fk = {almoxarifado_id}"
    database.execute(query=query)