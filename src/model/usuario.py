from config import database

class UsuarioHelper:

    @staticmethod
    def serialize(item):
        return {
            'id': item.get('id'),
            'tipo': item.get('tipo'),
            'senha': item.get('senha'),
            'dataCadastro': item.get('data_cadastro')
        }



def query_all(usuario_id: str):
    query = f"SELECT * from usuario WHERE id = {usuario_id}"
    return database.select_all(query=query)


# def query_one(usuario_id: str, almoxarifado_id: int):
#     query = f"SELECT * from almoxarifado WHERE empresa_fk = {empresa_id} AND id = {almoxarifado_id}"
#     return database.select_one(query=query)


def execute_create(item: dict):
    query = f"INSERT INTO usuario (tipo, senha, data_cadastro) VALUES " \
            f"('{item['tipo']}', '{item['senha']}', '{item['dataCadastro']}');"
    database.execute(query=query)


def execute_update(item: dict):
    query = f"UPDATE usuario SET tipo = '{item['tipo']}', SET senha = '{item['senha']}'" \
            f" WHERE id = '{item['id']}'"
    database.execute(query=query)


def execute_delete(usuario_id):
    query = f"DELETE FROM usuario WHERE id = '{usuario_id}'"
    database.execute(query=query)
