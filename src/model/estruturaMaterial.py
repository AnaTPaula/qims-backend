from config import database


class EstruturaMaterialHelper:

    @staticmethod
    def serialize(item):
        return {
            'materialPaiId': item.get('material_pai_fk'),
            'materialFilhoId': item.get('material_filho_fk')
        }


# def query_all(empresa_id: str, nome: str = None):
#     query = f"SELECT * from almoxarifado WHERE empresa_fk = {empresa_id}"
#     if nome:
#         query += f" AND nome = '{nome}'"
#     return database.select_all(query=query)


def query_one(material_pai_fk: int, material_filho_fk: int):
    query = f"SELECT * from estruturaMaterial WHERE material_pai_fk = {material_pai_fk} AND material_filho_fk = {material_filho_fk}"
    return database.select_one(query=query)


def execute_create(item: dict):
    query = f"INSERT INTO estruturaMaterial (material_pai_fk, material_filho_fk) VALUES " \
            f"('{item['materialPaiId']}', '{item['materialFilhoId']}');"
    database.execute(query=query)


def execute_update(item: dict):
    query = f"UPDATE estruturaMaterial SET material_pai_fk = '{item['materialPaiId']}', SET material_filho_fk = '{item['materialFilhoId']}'" \
            f" WHERE material_pai_fk = '{item['materialPaiId']}' AND material_filho_fk = '{item['materialFilhoId']}'"
    database.execute(query=query)


def execute_delete(material_pai_fk: int, material_filho_fk: int):
    query = f"DELETE FROM estruturaMaterial WHERE material_pai_fk = {material_pai_fk} AND material_filho_fk = {material_filho_fk}"
    database.execute(query=query)