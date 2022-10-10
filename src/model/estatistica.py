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
