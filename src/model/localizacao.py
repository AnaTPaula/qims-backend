from config import database


class localizacaoHelper:

    @staticmethod
    def serialize(item):
        return {
            'id': item.get('id'),
            'corredor': item.get('corredor'),
            'coluna': item.get('coluna'),
            'nivel': item.get('nivel'),
            'vagao': item.get('vagao')
        }


# def query_all(empresa_id: str, nome: str = None):
#     query = f"SELECT * from almoxarifado WHERE empresa_fk = {empresa_id}"
#     if nome:
#         query += f" AND nome = '{nome}'"
#     return database.select_all(query=query)


def query_one(id: str):
    query = f"SELECT * from localizacao WHERE id = {id}"
    return database.select_one(query=query)


def execute_create(item: dict):
    query = f" INSERT INTO localizacao (corredor, coluna, nivel, vagao ) VALUES " \
            f" ('{item['corredor']}', '{item['coluna']}', '{item['nivel']}', '{item['vagao']}'); "
    database.execute(query=query)


def execute_update(item: dict):
    query = f" UPDATE almoxarifado SET corredor = '{item['corredor']}', SET coluna = '{item['coluna']}', " \
            f" SET nivel = '{item['nivel']}', SET vagao = '{item['vagao']}' " \
            f" WHERE id = '{item['id']}'"
    database.execute(query=query)


def execute_delete(id: int):
    query = f"DELETE FROM localizacao WHERE id = '{id}' "
    database.execute(query=query)
