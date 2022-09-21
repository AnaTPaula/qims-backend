from config import database

class   EstoqueLoteHelper:

    @staticmethod
    def serialize(item):
        return {
            'estoqueId': item.get('estoque_fk'),
            'loteId': item.get('lote_fk'),
            'empresaId': item.get('empresa_fk'),
        }


def query_all(empresa_id: str):
    query = f"SELECT * from estoque_lote WHERE empresa_fk = {empresa_id}"
    return database.select_all(query=query)


def query_one(empresa_id: str, lote_id: int, estoque_id: str):
    query = f"SELECT * from estoque_lote WHERE empresa_fk = {empresa_id} AND lote_fk = {lote_id} AND estoque_fk = {estoque_id}"
    return database.select_one(query=query)


# def execute_create(item: dict):
#     query = f" INSERT INTO lote (id, codigo_lote, data_entrada, data_validade, quantidade, empresa_fk) VALUES " \
#             f" ('{item['id']}', '{item['codigoLote']}', '{item['dataEntrada']}', '{item['dataValidade']}' " \
#             f" '{item['quantidade']}', '{item['empresaId']}' "
#     database.execute(query=query)


# def execute_update(item: dict):
#     query = f" UPDATE lote SET codigo_lote = '{item['codigoLote']}', data_entrada = '{item['dataEntrada']}', " \
#             f" data_validade = '{item['davaValidade']}', quantidade = '{item['quantidade']}'" \
#             f" WHERE id = '{item['id']}' AND empresa_fk = {item['empresaId']} "
#     database.execute(query=query)


def execute_delete(empresa_id: str, lote_id: int, estoque_id: str):
    query = f"DELETE FROM lote_estoque WHERE empresa_fk = {empresa_id} AND lote_fk = {lote_id} AND estoque_fk = {estoque_id}"
    database.execute(query=query)