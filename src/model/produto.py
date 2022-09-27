from config import database

class ProdutoHelper:

    @staticmethod
    def serialize(item):
        return {
            'id': item.get('id'),
            'nome': item.get('nome'),
            'preco': item.get('preco'),
            'descricao': item.get('descricao'),
            'unidade': item.get('unidade'),
            'empresaId': item.get('empresa_fk'),
            'estoqueMinimo': item.get('estoque_minimo'),
            'estoqueMaximo': item.get('estoque_maximo'),
            'pontoReposicao': item.get('ponto_reposicao')
        }


def query_all(empresa_id: str, nome: str):
    query = " SELECT p from produto p " \
            " WHERE p.empresa_fk = %s "
    if nome:
        query += " AND nome = %s"
    return database.select_all(query=query, params=(empresa_id, nome))


def query_one(empresa_id: str, id: str, nome):
    query = " SELECT p from produto p " \
            " WHERE empresa_fk = %s AND id = %s "
    if nome:
        query += " AND nome = %s"
    return database.select_one(query=query, params=(empresa_id, id, nome))


def execute_create(item: dict):
    query = " INSERT INTO produto (id, nome, preco, descricao, unidade, empresa_fk, estoque_minimo, " \
            " estoque_maximo, ponto_reposicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s); "
    database.execute(query=query, params=(item['id'], item['nome'], item['preco'], item['descricao'], item['unidade'],
                                          item['empresaId'], item['estoqueMinimo'], item['estoqueMaximo'], item['pontoReposicao']))


def execute_update(item: dict):
    query = " UPDATE produto SET nome = %s, preco = %s, descricao = %s, unidade = %s, estoque_minimo = %s, " \
            " estoque_maximo = s% WHERE empresa_fk = s% AND id = %s "
    database.execute(query=query, params=(item['nome'], item['preco'], item['descricao'], item['unidade'], item['estoqueMinimo'],
                                          item['estoqueMaximo'], item['empresaId'], item['id']))


def execute_delete(empresa_id: str, id: int):
    query = " DELETE FROM produto WHERE empresa_fk = %s AND id = %s "
    database.execute(query=query, params=(empresa_id, id))