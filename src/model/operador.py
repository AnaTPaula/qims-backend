from config import database

class FuncionarioHelper:

    @staticmethod
    def serialize(item):
        return {
            'nomeUsuario': item.get('nome_usuario'),
            'acesso': item.get('acesso'),
            'empresaId': item.get('empresa_fk'),
            'usuarioId': item.get('usuario_fk')
        }


def query_all(empresa_id: str):
    query = f"SELECT * from operador WHERE empresa_fk = {empresa_id}"
    return database.select_all(query=query)


def query_one(empresa_id: str, usuario_id: int):
    query = f"SELECT * from operador WHERE empresa_fk = {empresa_id} AND usuario_fk = {usuario_id}"
    return database.select_one(query=query)


def execute_create(item: dict):
    query = f" INSERT INTO operador (nome_usuario, acesso, empresa_fk, usuario_fk)VALUES " \
            f" ('{item['nomeUsuario']}', '{item['acesso']}', '{item['empresaId']}', '{item['usuarioId']}'"
    database.execute(query=query)


def execute_update(item: dict):
    query = f" UPDATE operador SET nome_usuario = '{item['nomeUsuario']}', acesso = '{item['acesso']}', " \
            f" WHERE usuario_fk = '{item['usuarioID']}' AND empresa_fk = {item['empresaId']} "
    database.execute(query=query)


def execute_delete(usuario_fk: str, empresa_fk: str):
    query = f"DELETE FROM operador WHERE usuario_fk = '{usuario_fk}' AND empresa_fk = {empresa_fk}"
    database.execute(query=query)
