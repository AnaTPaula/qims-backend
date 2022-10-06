from config import database


class EstoqueLoteHelper:

    @staticmethod
    def serialize(item):
        return {
            'estoqueId': item.get('estoque_fk'),
            'loteId': item.get('lote_fk'),
            'empresaId': item.get('empresa_fk'),
        }


class LoteHelper:

    @staticmethod
    def serialize(item):
        return {
            'id': item.get('id'),
            'codigoLote': item.get('codigo_lote'),
            'dataEntrada': item.get('data_entrada'),
            'dataValidade': item.get('data_validade'),
            'quantidade': item.get('quantidade'),
            'empresaId': item.get('empresa_fk')
        }


# TODO: mover para lote.py no model
def query_one_lote(empresa_id: int, lote_id: int):
    query = "SELECT * from lote l left join estoque_lote el on l.id = el.lote_fk WHERE l.empresa_fk = %s AND l.id = %s"
    return database.select_one(query=query, params=(empresa_id, lote_id,))


# TODO: mover para lote.py no model
def query_all_lote_by_produto_estoque(empresa_id: int, produto_estoque_id: int, tipo_armazenagem: str = None):
    query = "SELECT el.produto_estoque_fk, el.empresa_fk, l.id, l.codigo_lote, l.data_entrada, l.data_validade, " \
            "l.quantidade from estoque_lote el JOIN lote l ON el.lote_fk = l.id WHERE el.empresa_fk = %s " \
            "AND el.produto_estoque_fk = %s "
    if tipo_armazenagem:
        if tipo_armazenagem == 'FIFO':
            query += " ORDER BY l.data_entrada ASC"
        elif tipo_armazenagem == 'LIFO':
            query += " ORDER BY l.data_entrada DESC"
        elif tipo_armazenagem == 'FEFO':
            query += " ORDER BY l.data_validade ASC"
    return database.select_all(query=query, params=(empresa_id, produto_estoque_id))


# TODO: mover para lote.py no model
def execute_update_lote(item: dict):
    query = "UPDATE lote SET codigo_lote = %s, data_entrada = %s, data_validade = %s, quantidade = %s WHERE id = %s " \
            "AND empresa_fk = %s;"
    database.execute(query=query, params=(item['codigoLote'], item['dataEntrada'], item.get('dataValidade'),
                                          item['quantidade'], item['id'], item['empresaId'],))


# TODO: mover para lote.py no model
def execute_delete_lote(empresa_id: int, lote_id: int):
    query = "DELETE FROM lote WHERE empresa_fk = %s AND id = %s;"
    database.execute(query=query, params=(empresa_id, lote_id,))


def execute_create_estoque_lote(item: dict):
    query = "INSERT INTO estoque_lote (produto_estoque_fk, lote_fk, empresa_fk) VALUES " \
            "(%s, %s, %s);"
    database.execute(query=query, params=(item['produtoEstoqueId'], item['loteId'], item['empresaId'],))


def execute_delete_estoque_lote(empresa_id: str, lote_id: int, produto_estoque_id: int):
    query = f"DELETE FROM estoque_lote WHERE empresa_fk = %s AND lote_fk = %s AND produto_estoque_fk = %s"
    database.execute(query=query, params=(empresa_id, lote_id, produto_estoque_id))
