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


def query_all_prd(empresa_id: str, nome: str):
    query = " select * from produto where empresa_fk = %s "
    if nome:
        query += " AND nome = %s "
    params = (empresa_id, nome,) if nome else (empresa_id,)
    return database.select_all(query=query, params=params)


def query_one_prd(empresa_id: int, produto_id: int):
    query = " select * from produto where empresa_fk = %s and id = %s "
    return database.select_one(query=query, params=(empresa_id, produto_id,))


def execute_create_prd(item: dict):
    query = " INSERT INTO produto (nome, preco, descricao, unidade, empresa_fk, estoque_minimo, " \
            " estoque_maximo, ponto_reposicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    database.execute(query=query, params=(item['nome'], item['preco'], item['descricao'], item['unidade'],
                                          item['empresaId'], item['estoqueMinimo'], item['estoqueMaximo'],
                                          item['pontoReposicao']))


def execute_update_prd(item: dict):
    query = " UPDATE produto SET nome = %s, preco = %s, descricao = %s, unidade = %s, estoque_minimo = %s, " \
            " estoque_maximo = %s, ponto_reposicao = %s WHERE empresa_fk = %s AND id = %s "
    database.execute(query=query,
                     params=(item['nome'], item['preco'], item['descricao'], item['unidade'], item['estoqueMinimo'],
                             item['estoqueMaximo'], item['pontoReposicao'], item['empresaId'], item['id']))


def execute_delete_prd(empresa_id: int, produto_id: int):
    query = " DELETE FROM produto WHERE empresa_fk = %s AND id = %s "
    database.execute(query=query, params=(empresa_id, produto_id))
