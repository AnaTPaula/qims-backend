from config import database


def query_saida_produto(empresa_id: int):
    query = "select nome_produto as produto, sum(quantidade) as quantidade from historico where operacao = 'SAIDA'" \
            " and empresa_fk = %s group by nome_produto order by quantidade DESC"
    return database.select_all(query=query, params=(empresa_id,))


def query_entrada_produto(empresa_id: int):
    query = "select nome_produto as produto, sum(quantidade) as quantidade from historico where operacao = 'ENTRADA'" \
            " and empresa_fk = %s group by nome_produto order by quantidade DESC"
    return database.select_all(query=query, params=(empresa_id,))


def query_estoque_quantidade(empresa_id: int):
    query = "select e.nome as nome_estoque, e.descricao as descricao_estoque , p.nome as nome_produto," \
            " p.descricao as descricao_produto, pe.quantidade, p.unidade, p.preco from estoque e left join " \
            "produto_estoque pe on pe.estoque_fk = e.id join produto p on p.id = pe.produto_fk" \
            " where e.empresa_fk = %s order by pe.quantidade DESC"
    return database.select_all(query=query, params=(empresa_id,))


def query_produto_quantidade(empresa_id: int):
    query = "select p.nome as nome_produto, p.descricao as descricao_produto, coalesce(pe.quantidade, 0) " \
            "as quantidade, p.unidade, p.preco from produto p left join produto_estoque pe on pe.estoque_fk = p.id " \
            "where p.empresa_fk = %s order by pe.quantidade DESC"
    return database.select_all(query=query, params=(empresa_id,))