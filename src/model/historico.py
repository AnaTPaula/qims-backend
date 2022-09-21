from config import database


class HistoricoHelper:

    @staticmethod
    def serialize(item):
        return {
            'operadorId': item.get('operador_fk'),
            'produtoId': item.get('material_fk'),
            'estoqueId': item.get('estoque_fk'),
            'quantidade': item.get('quantidade'),
            'empresaId': item.get('empresa_fk'),
            'operacao': item.get('operacao'),
            'dataHora': item.get('data_hora'),
        }


def query_all(empresa_id: str):
    query = f"SELECT * from historico WHERE empresa_fk = {empresa_id}"
    return database.select_all(query=query)


def query_one(operador_id: str, produto_id: str, estoque_id: str, empresa_id: str):
    query = f"SELECT * from historico WHERE operador_fk = {operador_id} AND produto_fk = {produto_id} AND estoque_fk = {estoque_id} AND empresa_fk = {empresa_id}"
    return database.select_one(query=query)


def execute_create(item: dict):
    query = f" INSERT INTO historico (quantidade, operacao, data_hora, operador_fk, produto_fk, estoque_fk, empresa_fk) VALUES " \
            f" ('{item['quantidade']}', '{item['operacao']}', '{item['dataHora']}', '{item['operadorId']}', " \
            f" '{item['produtoId']}', '{item['estpoqueId']}', '{item['empresaId']}'); "
    database.execute(query=query)


def execute_update(item: dict):
    query = f" UPDATE historico SET quantidade = '{item['quantidade']}', operacao = '{item['operacao']}', datahora = '{item['dataHora']}' " \
            f" WHERE operador_fk = {item['operadorId']} AND produto_fk = {item['produtoId']} AND " \
            f" estoque_fk = {item['estoqueId']} AND empresa_fk = {item['empresaId']}"
    database.execute(query=query)


def execute_delete(operador_id: str, produto_id: str, estoque_id: str, empresa_id: str):
    query = f" DELETE FROM almoxarifado WHERE operador_fk = {operador_id} AND produto_fk = {produto_id} AND " \
            f" estoque_fk = {estoque_id} AND empresa_fk = {empresa_id} "
    database.execute(query=query)
