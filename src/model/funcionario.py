from config import database

class FuncionarioHelper:

    @staticmethod
    def serialize(item):
        return {
            'nomeUsuario': item.get('nme_usuario'),
            'acesso': item.get('acesso'),
            'empresaId': item.get('empresa_fk'),
            'usuarioId': item.get('usuario_fk')
        }


def query_all(usuario_id: str, nome: str = None):
    query = f"SELECT * from funcionario WHERE usuario_fk = {usuario_id}"
    if nome:
        query += f" AND nome_usuario = '{nome}'"
    return database.select_all(query=query)


def query_one(empresa_id: str, usuario_id: int):
    query = f"SELECT * from funcionario WHERE empresa_fk = {empresa_id} AND id = {usuario_id}"
    return database.select_one(query=query)


def execute_create(item: dict):
    query = f" INSERT INTO funcionario (nome_usuario, acesso, empresa_fk, usuario_fk," \
            f" aceite_termos_uso, usuario_fk)VALUES " \
            f" ('{item['nomeUsuario']}', '{item['acesso']}', '{item['empresaId']}', '{item['usuarioId']}'"
    database.execute(query=query)


def execute_update(item: dict):
    query = f" UPDATE funcionario SET nome_usuario = '{item['nomeUsuario']}', SET acesso = '{item['acesso']}', " \
            f" WHERE usuario_fk = '{item['usuarioID']}' "
    database.execute(query=query)


def execute_delete(usuario_fk: str):
    query = f"DELETE FROM funcionario WHERE usuario_fk = '{usuario_fk}'"
    database.execute(query=query)
