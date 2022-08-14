from config import database


class HistoricoHelper:

    @staticmethod
    def serialize(item):
        return {
            'quantidade': item.get('quantidade'),
            'conta': item.get('conta'),
            'operacao': item.get('operacao'),
            'dataHora': item.get('data_hora'),
            'funcionarioId': item.get('funcionario_fk'),
            'materialId': item.get('material_fk'),
            'almoxarifadoId': item.get('almoxarifado_fk')
        }


def query_all(funcionario_id: str, material_id: str, almoxarifado_id: str):
    query = f"SELECT * from historico WHERE funcionario_fk = {funcionario_id} OR material_fk = {material_id} OR almoxarifado_fk = {almoxarifado_id}"
    return database.select_all(query=query)


def query_one(funcionario_id: str, material_id: str, almoxarifado_id: str):
    query = f"SELECT * from historico WHERE funcionario_fk = {funcionario_id} AND material_fk = {material_id} AND almoxarifado_fk = {almoxarifado_id}"
    return database.select_one(query=query)


def execute_create(item: dict):
    query = f" INSERT INTO almoxarifado (quantidade, conta, operacao, data_hora, funcionario_fk, material_fk, almoxarifado_fk) VALUES " \
            f" ('{item['quantidade']}', '{item['conta']}', '{item['operacao']}', '{item['dataHora']}', '{item['funcionarioId']}', " \
            f" '{item['materialId']}', '{item['almoxarifadoId']}'); "
    database.execute(query=query)


# def execute_update(item: dict):
#     query = f"UPDATE almoxarifado SET nome = '{item['nome']}', SET descricao = '{item['descricao']}'" \
#             f" WHERE empresa_fk = '{item['empresaId']}' AND id = {item['id']}"
#     database.execute(query=query)


# def execute_delete(empresa_id: str, almoxarifado_id: int):
#     query = f"DELETE FROM almoxarifado WHERE empresa_fk = '{empresa_id}' AND id = {almoxarifado_id}"
#     database.execute(query=query)
