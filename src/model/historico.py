from config import database


class HistoricoHelper:

    @staticmethod
    def serialize(item):
        return {
            'operador': item.get('operador'),
            'produto': item.get('produto'),
            'estoque': item.get('estoque'),
            'quantidade': item.get('quantidade'),
            'empresaId': item.get('empresa_fk'),
            'operacao': item.get('operacao'),
            'dataHora': item.get('datahora'),
        }


def query_all_historico(empresa_id: int, produto_id: int):
    query = "SELECT o.nome_usuario as operador, p.nome as produto, e.nome as estoque, h.quantidade, h.empresa_fk, " \
            "h.operacao, h.data_hora from historico h JOIN operador o ON h.operador_fk = o.usuario_fk " \
            "JOIN produto p ON h.produto_fk = p.id JOIN estoque e ON h.estoque_fk = e.id " \
            "WHERE empresa_fk = %s AND produto_id = %s"
    return database.select_all(query=query, params=(empresa_id, produto_id,))


def execute_create_historico(item: dict):
    query = "INSERT INTO historico (quantidade, operacao, operador_fk, produto_fk, estoque_fk, empresa_fk) VALUES " \
            " (%s, %s, %s, %s, %s, %s); "
    database.execute(query=query, params=(item['quantidade'], item['operacao'], item['operadorId'],
                                          item['produtoId'], item['estoqueId'], item['empresaId']))
