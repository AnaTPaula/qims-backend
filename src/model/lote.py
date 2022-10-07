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
            'associado': True if item.get('produto_estoque_fk') else False,
        }


def query_all_lote(empresa_id: int, codigo_lote: str):
    query = "select l.*, produto_estoque_fk from lote l left join estoque_lote el on l.id = el.lote_fk " \
            "where l.empresa_fk = %s "
    if codigo_lote:
        query += " and codigo_lote = %s "
        params = (empresa_id, codigo_lote,)
    else:
        params = (empresa_id,)
    return database.select_all(query=query, params=params)


def query_one_lote(empresa_id: int, lote_id: int):
    query = "SELECT * from lote WHERE empresa_fk = %s AND id = %s "
    params = (empresa_id, lote_id,)
    return database.select_one(query=query, params=params)


def execute_create_lote(item: dict) -> int:
    query = "INSERT INTO lote (codigo_lote, data_entrada, data_validade, quantidade, empresa_fk) VALUES " \
            " (%s, %s, %s, %s, %s) RETURNING id;"
    params = (item['codigoLote'], item['dataEntrada'], item.get('dataValidade'), item['quantidade'], item['empresaId'],)
    return database.execute_returning_id(query=query, params=params)


def execute_update_lote(item: dict):
    query = "UPDATE lote SET codigo_lote = %s, data_entrada = %s, data_validade = %s, quantidade = %s " \
            " WHERE empresa_fk = %s AND id = %s "
    params = (item['codigoLote'], item['dataEntrada'], item.get('dataValidade'), item['quantidade'], item['empresaId'],
              item['id'],)
    database.execute(query=query, params=params)


def execute_delete_lote(empresa_id: int, lote_id: int):
    query = "DELETE FROM lote WHERE empresa_fk = %s AND id = %s "
    params = (empresa_id, lote_id)
    database.execute(query=query, params=params)
