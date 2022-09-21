from config import database

class LoteHelper:

    @staticmethod
    def serialize(item):
        return {
            'id': item.get('id'),
            'codigoLote': item.get('codigo_lote'),
            'dataEntrada': item.get('data_entrada'),
            'dataValidade': item.get('data_validade'),
            'quantidade': item.get('quantidade'),
            'empresaId': item.get('empresa_fk'),
        }


def query_all(empresa_id: str):
    query = f"SELECT * from lote WHERE empresa_fk = {empresa_id}"
    return database.select_all(query=query)


def query_one(empresa_id: str, id: int):
    query = f"SELECT * from lote WHERE empresa_fk = {empresa_id} AND id = {id}"
    return database.select_one(query=query)


def execute_create(item: dict):
    query = f" INSERT INTO lote (id, codigo_lote, data_entrada, data_validade, quantidade, empresa_fk) VALUES " \
            f" ('{item['id']}', '{item['codigoLote']}', '{item['dataEntrada']}', '{item['dataValidade']}' " \
            f" '{item['quantidade']}', '{item['empresaId']}' "
    database.execute(query=query)


def execute_update(item: dict):
    query = f" UPDATE lote SET codigo_lote = '{item['codigoLote']}', data_entrada = '{item['dataEntrada']}', " \
            f" data_validade = '{item['davaValidade']}', quantidade = '{item['quantidade']}'" \
            f" WHERE id = '{item['id']}' AND empresa_fk = {item['empresaId']} "
    database.execute(query=query)


def execute_delete(empresa_id: str, id: str):
    query = f"DELETE FROM lote WHERE id = '{id}' AND empresa_fk = {empresa_id}"
    database.execute(query=query)