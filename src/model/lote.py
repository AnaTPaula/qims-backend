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


def query_all_lote(empresa_id: int):
    query = f" select * from lote where empresa_fk = %s "
    params = (empresa_id,)
    return database.select_all(query=query, params=params)


def query_one_lote(empresa_id: int, lote_id: int):
    query = f" SELECT * from lote WHERE empresa_fk = %s AND id = %s "
    params = (empresa_id, lote_id,)
    return database.select_one(query=query, params=params)


def execute_create_lote(item: dict):
    query = f" INSERT INTO lote (codigo_lote, data_entrada, data_validade, quantidade, empresa_fk) VALUES " \
            f" (%s, %s, %s, %s, %s) "
    params = (item['codigoLote'], item['dataEntrada'], item['dataValidade'], item['quantidade'], item['EmpresaId'],)
    database.execute(query=query, params=params)


def execute_update_lote(item: dict):
    query = " UPDATE lote SET codigo_lote = %s, data_entrada = %s, data_validade = %s, quantidade = %s " \
            " WHERE empresa_fk = %s AND id = %s "
    params = (item['codigoLote'], item['dataEntrada'], item['dataValidade'], item['quantidade'], item['empresaId'],
              item['id'],)
    database.execute(query=query, params=params)


def execute_delete_lote(empresa_id: int, lote_id: int):
    query = f" DELETE FROM lote WHERE id = %s AND empresa_fk = %s "
    params = (empresa_id, lote_id)
    database.execute(query=query, params=params)
