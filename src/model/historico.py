from config import database


class HistoricoHelper:

    @staticmethod
    def serialize(item):
        return {
            'historicoId': item.get('id'),
            'operador': item.get('nome_operador'),
            'registroOperador': item.get('registro_operador'),
            'produtoId': item.get('produto_fk'),
            'estoque': item.get('nome_estoque'),
            'estoqueDestino': item.get('nome_estoque_destino'),
            'quantidade': item.get('quantidade'),
            'empresaId': item.get('empresa_fk'),
            'operacao': item.get('operacao'),
            'dataHora': item.get('data_hora'),
        }


def query_all_historico(empresa_id: int, produto_id: int):
    query = "SELECT h.* from historico h WHERE empresa_fk = %s AND produto_fk = %s order by h.data_hora desc"
    return database.select_all(query=query, params=(empresa_id, produto_id,))


def query_one_historico(empresa_id: int, historico_id: int):
    query = "SELECT h.* from historico h WHERE empresa_fk = %s AND id = %s "
    return database.select_one(query=query, params=(empresa_id, historico_id,))


def execute_create_historico(item: dict):
    query = "INSERT INTO historico (registro_operador, nome_operador, nome_estoque, estoque_id, " \
            "nome_estoque_destino, estoque_id_destino, quantidade, operacao, nome_produto, produto_fk, empresa_fk)" \
            " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); "
    database.execute(query=query, params=(item['usuarioId'], item['nomeOperador'], item['nomeEstoque'],
                                          item['estoqueId'], item.get('nomeEstoqueDestino'),
                                          item.get('estoqueIdDestino'), item['quantidade'], item['operacao'],
                                          item['nomeProduto'], item['produtoId'], item['empresaId'],))


def execute_delete_historico(empresa_id: int, historico_id: int):
    query = "DELETE FROM historico WHERE empresa_fk = %s AND id = %s "
    params = (empresa_id, historico_id)
    database.execute(query=query, params=params)
