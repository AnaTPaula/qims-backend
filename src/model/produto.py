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


def query_all(empresa_id: str):
    query = f"SELECT * from produto WHERE empresa_fk = {empresa_id}"
    return database.select_all(query=query)


def query_one(empresa_id: str, id: str):
    query = f"SELECT * from produto WHERE empresa_fk = {empresa_id} AND id = {id}"
    return database.select_one(query=query)


def execute_create(item: dict):
    query = f"INSERT INTO produto (id, nome, preco, descricao, unidade, empresa_fk, estoque_minimo," \
            f"estoque_maximo, ponto_reposicao ) VALUES " \
            f"('{item['id']}', '{item['nome']}', '{item['preco']}', '{item['descricao']}', '{item['unidade']}'," \
            f"'{item['empresaId']}', '{item['estoqueMinimo']}', '{item['estoqueMaximo']}', '{item['pontoReposicao']}');"
    database.execute(query=query)


def execute_update(item: dict):
    query = f" UPDATE produto SET nome = '{item['nome']}', preco = '{item['preco']}', descricao = '{item['descricao']}'," \
            f" unidade = '{item['unidade']}', estoque_minimo = '{item['estoqueMinimo']}', estoque_maximo = '{item['estoqueMaximo']}'"\
            f" WHERE empresa_fk = '{item['empresaId']}' AND id = {item['id']}"
    database.execute(query=query)


def execute_delete(empresa_id: str, id: int):
    query = f"DELETE FROM produto WHERE empresa_fk = '{empresa_id}' AND id = {id}"
    database.execute(query=query)