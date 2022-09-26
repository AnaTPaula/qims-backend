from passlib.handlers.pbkdf2 import pbkdf2_sha256
from config import database


class UsuarioHelper:

    @staticmethod
    def serialize(item):
        return {
            'id': item.get('id'),
            'tipo': item.get('tipo'),
            'dataCadastro': item.get('data_cadastro')
        }

    @staticmethod
    def verify_password(item: dict, senha_sem_hash: str):
        try:
            return pbkdf2_sha256.verify(senha_sem_hash, item['senha'])
        except ValueError:
            return False

    @staticmethod
    def set_hash_password(senha_nova: str):
        return pbkdf2_sha256.hash(senha_nova)


# def query_all():
#     query = f" SELECT * from usuario "
#     return database.select_all(query=query)
#
#
# def query_one(usuario_id: str):
#     query = f" SELECT * from usuario WHERE id = {usuario_id} "
#     return database.select_one(query=query)


def execute_create_user(item: dict) -> int:
    query = "INSERT INTO usuario (tipo, senha) VALUES (%s, %s) RETURNING id;"
    return database.execute_returning_id(query=query, params=(item['tipo'], item['senha'],))


def execute_update_user(item: dict):
    query = "UPDATE usuario SET tipo = %s, senha = %s WHERE id = %s;"
    database.execute(query=query, params=(item['tipo'], item['senha'], item['id'],))


def execute_delete_user(usuario_id: int):
    query = f"DELETE FROM usuario WHERE id = %s;"
    database.execute(query=query, params=(usuario_id,))
