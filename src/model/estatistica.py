from config import database


def count_all_produto(empresa_id: int):
    query = "SELECT count(*) as count from produto WHERE empresa_fk = %s "
    return database.select_one(query=query, params=(empresa_id,))


def count_all_estoque(empresa_id: int):
    query = "SELECT count(*) as count from estoque WHERE empresa_fk = %s "
    return database.select_one(query=query, params=(empresa_id,))


def count_preco_total_produtos(empresa_id: int):
    query = "select COALESCE(sum(preco*quantidade), 0) as preco_total from (" \
            "select p.preco, COALESCE(sum(pe.quantidade), 0) as quantidade from produto p left join " \
            "produto_estoque pe on p.id = pe.produto_fk where p.empresa_fk = %s group by p.id) valor"
    return database.select_one(query=query, params=(empresa_id,))


def query_last_historico(empresa_id: int):
    query = "select nome_operador as operador, nome_estoque as origem, nome_estoque_destino as destino, quantidade, " \
            "data_hora as timestamp, operacao, nome_produto as produto from historico " \
            "where empresa_fk = %s order by data_hora desc limit 10;"
    return database.select_all(query=query, params=(empresa_id,))


def query_produtos_estoque_maximo(empresa_id: int):
    query = "select p.nome as produto, COALESCE(sum(pe.quantidade),0) as quantidade, p.estoque_maximo as maximo " \
            "from produto p left join produto_estoque pe " \
            "on pe.produto_fk = p.id where p.empresa_fk = %s and p.estoque_maximo > 0 group by p.id " \
            "having COALESCE(sum(pe.quantidade),0) >= p.estoque_maximo;"
    return database.select_all(query=query, params=(empresa_id,))


def query_produtos_ponto_reposicao(empresa_id: int):
    query = "select p.nome as produto, COALESCE(sum(pe.quantidade),0) as quantidade, p.ponto_reposicao as reposicao " \
            "from produto p left join produto_estoque pe " \
            "on pe.produto_fk = p.id where p.empresa_fk = %s and p.ponto_reposicao > 0 group by p.id " \
            "having COALESCE(sum(pe.quantidade),0) <= p.ponto_reposicao " \
            "and COALESCE(sum(pe.quantidade),0) > p.estoque_minimo;"
    return database.select_all(query=query, params=(empresa_id,))


def query_produtos_estoque_minimo(empresa_id: int):
    query = "select p.nome as produto, COALESCE(sum(pe.quantidade),0) as quantidade, p.estoque_minimo as minimo " \
            "from produto p left join produto_estoque pe " \
            "on pe.produto_fk = p.id where p.empresa_fk = %s and p.estoque_minimo > 0 group by p.id " \
            "having COALESCE(sum(pe.quantidade),0) <= p.estoque_minimo;"
    return database.select_all(query=query, params=(empresa_id,))


def query_entrada_produtos(empresa_id: int):
    query = "select p.nome, qtd.quantidade from (select h.produto_fk, COALESCE(sum(h.quantidade),0) as quantidade " \
            "from historico h where h.empresa_fk = %s and h.operacao = 'ENTRADA' " \
            "group by h.produto_fk LIMIT 10) qtd inner join produto p on p.id = qtd.produto_fk;"
    return database.select_all(query=query, params=(empresa_id,))


def query_saida_produtos(empresa_id: int):
    query = "select p.nome, qtd.quantidade from (select h.produto_fk, COALESCE(sum(h.quantidade),0) as quantidade " \
            "from historico h where h.empresa_fk = %s and h.operacao = 'SAIDA' " \
            "group by h.produto_fk LIMIT 10) qtd inner join produto p on p.id = qtd.produto_fk;"
    return database.select_all(query=query, params=(empresa_id,))
